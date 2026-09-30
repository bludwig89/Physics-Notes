# Chapter 18 — Gravity

*Chapter 18 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F56-einstein-coupling-from-lattice-phase-matching.md`,
`findings/F57-induced-eh-term-from-leg-field-backreaction.md`,
`findings/F58-clockrate-coupling-from-neighbour-rule.md`,
`findings/F59-induced-eh-prefactor-and-f10-selection.md`,
`findings/F60-induced-G-channel-reconciliation.md`,
`findings/F61-weyl-eta-and-gstar-prefactor.md`,
`findings/F63-spin-torsion-magnitude-estimate.md`,
`findings/F64-em-connection-gravity.md`,
`findings/F79-structural-newton-constant.md`,
`findings/F106-psi-K-sourcing-derivation.md`,
`findings/F173-pressure-tolman-discriminator.md`,
`findings/F178-gravity-full-tensor-adoption.md`,
`findings/F243-f3-lowdensity-lensing-not-falsified.md`,
`findings/F244-emqg-1overb-3d-lensing.md`,
`findings/F345-field-equation-uniqueness-lovelock.md`, and
`findings/F383-locality-generates-not-forbids-four-derivative-term.md`
(the sixteen findings `00-plan.md` §2 assigns to this chapter, all read in full), read against
`docs/theory/key-decisions.md` (Core Design Decision 4, the canonical statement of this chapter's
hierarchy), `docs/theory/supersessions.yaml` (record **S4-F178-full-stress-energy**, read in full:
F114 superseded, F64/F106/F173/F174 reclassified — none of this chapter's sixteen findings is
itself superseded), and `claims-index.md` (**CL008** — the headline card, `live`/`exact`; **CL015**
— Mercury/PPN, `narrowed`; **CL153** — the Tolman discriminator, `live`/`unreviewed-seed`;
**CL023** — the withdrawn dielectric black hole, confirming S4). Notation and results are those of
Chapters 1, 6 and 11 — $c_\text{lat}$, $\Omega(\mathbf k)$, $\Omega_\text{rest}(m)=\arcsin m$,
$\Omega_\text{Dirac}(\mathbf k,m)$ — extended, never redefined.

## 18.0 What this chapter establishes, and the hierarchy up front

**The fundamental gravitational law of this model is the induced Einstein equation**
$G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, sourced by the *full* stress-energy tensor, with a
structural/induced Newton constant $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79). **The single
impedance-matched lattice dielectric** $K=e^{2GM/rc^2}$ **is not a competing fundamental law — it
is that same equation's exact vacuum solution and weak-field representation** (F64), valid
wherever $T_{\mu\nu}\to0$ or $p\ll\rho c^2$, and demoted from candidate-fundamental to
representation by a named decision (F178, 2026-06-29) for three independent reasons: a source
built from $T^{00}$ alone is not Lorentz covariant, F106 itself already named the induced Einstein
equation as the energy-only law's parent, and the energy-only law has no neutron-star maximum mass
(excluded by PSR J0740+6620). This chapter presents both halves in full — F56–F61 and F79 derive
the coupling $G$ genuinely from the lattice (not the dielectric route: an induced-gravity argument
that has nothing to do with $K$), F64 derives the dielectric's *placement* and its PPN content in
full, and F173/F178/F345/F383 carry the argument for, and the content of, the hierarchy between
them. A reader who came only for "is $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$ or $K=e^{2u}$ the model's
gravity" has the answer in this paragraph; the rest of the chapter is the case for it.

## 18.1 Inputs

**Postulates used.** **P1–P4** (discreteness, locality/homogeneity/isotropy, linearity/unitarity)
carry through every Brillouin-zone integral below exactly as they did in Chapter 6; nothing new is
invoked. **P5/P6** enter through the rest-leg/mass mechanism (Chapter 11): F58's WEP proof (§18.2.3
below) uses the *same* renormalised rest-frequency $\Omega_\text{rest}(x)=\sqrt{A(x)}\arcsin m$ that
Chapter 11 derived as $\Omega_\text{Dirac}(0,m)$ (R11.12), now evaluated on a background with a
position-dependent lapse $A(x)$ rather than at $A\equiv1$ — this chapter's first use of R11.12/R11.13
outside Chapter 11 itself. **P7** (elegant design) is invoked explicitly and repeatedly in this
sector — the "elegant-design endpoint" language in F106's own derivation, the preference for one
dielectric field over two independently-sourced metric legs in F64 — and inherits Chapter 1's Gap
[G-1] (no independent argument that elegance tracks truth) without adding new content to it.

**Prior results used, precisely.** **R6.4/R6.5** ($c_\text{lat}=d\Omega/d|\mathbf k||_0=1/\sqrt3$,
the rotation-rate reading) is the speed every Brillouin-zone integral in F56–F61/F79 is built from —
"the same F25/F26 phase-matching" is this chapter's own recurring phrase for R6.3–R6.5. **R6.6/R6.7**
(Maxwell's curl law as the linearisation of the exact real $(\mathbf E,\mathbf B)$ rotation, and the
EM sector's origin in that rotation rather than in a separately-postulated field) underlies F79's
key step (§18.2.7): the electromagnetic stress tensor's tracelessness in $3{+}1$D, which this
chapter uses to show the dielectric $K$ carries no *fundamental* kinetic term of its own. **R11.11–
R11.13** (mass as the unique $\mathbf k=0$ rest covariant, $\Omega_\text{rest}(m)=\arcsin m$, and
$c_\text{lat}$/rest-mass as slope/intercept of one generator $\Omega_\text{Dirac}(\mathbf k,m)$) is
the identity F58's weak-equivalence-principle proof (Q0, §18.2.3) rests on: the *same* generator
that fixes $c_\text{lat}$ also fixes the mass-independence of gravitational clock-slowing.

**Free inputs consumed — stated precisely, because this is the chapter's own accounting question.**
Two registers, kept separate throughout:

1. **The structural/lattice-unit form of $G$ is derived here, in closed form, with zero new fitted
   parameters.** F79's result $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (§18.2.7, R18.7) expresses $G$ entirely
   in terms of $c$, $\hbar$, and the one length $a$ — the lattice cell — with the pure number
   $8\pi\sqrt3$ assembled from three separately-derived structural inputs ($\eta_\text{Weyl}=1/12$
   exact, F61; the channel exponent $-1$, forced as a theorem by F79's own tracelessness argument;
   $g_*=48$, the anomaly-free field count times the three-generation count). **No numerical SI
   value of $G$ is fixed by this chapter.** What is fixed is the *dimensionless* ratio $a/\ell_P=
   \sqrt{8\pi}\,3^{1/4}=6.5978$ — a structural prediction about the lattice cell relative to the
   Planck length, not yet a statement in metres. Anchoring $a$ to an SI length (either the Planck
   length directly, which is circular if $G$ is the thing being derived, or the genuinely
   independent mass-anchor route through a measured fermion mass) is **Chapter 17's job**,
   forward-cited here exactly as Chapter 6 forward-cited it for $c_\text{lat}$.
2. **A new, undisclosed forward dependency, flagged as this chapter's own contribution to the
   monograph's dependency ledger.** F79's $g_*=48$ requires the exact fermionic field count *per
   generation* (16, from F38's anomaly-free Higgs-free content, Chapter 12) *times* the exact
   *number of generations* (3, from F75's $O_h$-representation-theory theorem, **Chapter 15**) —
   neither of which `00-plan.md`'s dependency table lists as an input to Chapter 18 (it lists only
   Ch.6, Ch.11). This is a genuine, previously unrecorded cross-chapter dependency, not merely a
   citation convenience: F79's own closed-form coefficient $8\pi\sqrt3$ is not assembled without
   it. Logged as a new gap below (§18.6, Gap [G-8]) rather than silently patched by pretending
   `00-plan.md`'s dependency column already listed Ch.15.
3. **Symbol note, not a gap.** Chapter 2's $a$ (R2.10, $a=2/\sqrt3=2c_\text{lat}$) is a
   *dimensionless* ratio in lattice-native units (hop length set to 1) — a pure geometric fact
   about the BCC cell. This chapter's $a$ (F56 onward) is the *dimensionful* physical size of that
   same cell, to be anchored in SI units only in Chapter 17. Both are called "$a$" by their source
   findings; this chapter keeps the distinction explicit in prose wherever both could appear, since
   conflating "the BCC cell edge is $2/\sqrt3$ hop-lengths" with "the BCC cell edge is $6.60\,\ell_P$"
   would be a unit error, not a restatement.

## 18.2 The derivation

### 18.2.1 F56 — the geometric factor $16\pi$ is exact; the dimensionful $G$ is reduced to the lattice spacing

F56 (2026-05-29) factors $16\pi G/c^4$ into a geometric piece and a dimensionful piece and derives
the first exactly. The bare 6-neighbour lattice Laplacian, with **no $4\pi$ inserted by hand**, has
a point-source far field $G(r)\to-1/(4\pi r)$ — measured $4\pi C=1.0002$ — so Newton's $4\pi$ is the
solid angle of 3-D space as the lattice's long-wavelength modes resolve it, the same isotropy that
makes $c_\text{lat}$ direction-independent (R6.2/R2.13). Given Newton's $4\pi$, the weak-field
relation $h_{00}=-2\phi/c^2$, and the static-dust trace reversal, the tensor coupling is forced
**exactly** to $16\pi G/c^4$ (Einstein-tensor coupling $8\pi G/c^4$), residual $0.0$, bit-for-bit
(F56 check C1). The *dimensionful* $G$, by contrast, is reduced — not derived — to a Sakharov-type
induced Einstein–Hilbert coefficient, a Brillouin-zone integral over the F26/R6.2 dispersion scaling
as $G_\text{ind}\propto\ell^2$ (measured exponent $2.0008$), i.e. $G$ is locked to the square of the
lattice spacing with no absolute prefactor yet supplied.

$$\boxed{\;16\pi G/c^4\text{'s geometric factor }16\pi\text{ (equiv. }8\pi\text{ for }G_{\mu\nu}\text{) is forced exactly by lattice isotropy + trace reversal, residual }0.0;\quad G\propto\ell^2\text{ (Sakharov scaling), absolute prefactor open}\;}\tag{R18.1}$$

(F56, checks C1–C3; CL059, `open`, `falsifier: unset`.)

### 18.2.2 F57 — the induced Einstein–Hilbert term is *generated*, not assumed, by the matter back-reaction

F56 Part B *assumed* the Sakharov mechanism; F57 (2026-05-29) exhibits it as an explicit, finite
lattice calculation. Coupling the Newtonian potential $\Phi$ to the matter density and integrating
out the F26/R6.2 propagating modes gives a one-loop vacuum polarization
$\Pi(q)=\Pi(0)-\Pi_2q^2+\dots$; in position space $\tfrac12\Pi_2(\nabla\Phi)^2$ is exactly the
induced graviton **kinetic** term. The result: $\Pi_2=+0.061>0$ — a positive gradient stiffness,
i.e. propagating, attractive gravity, generated by the back-reaction rather than posited (check K2).
Because the Brillouin zone is compact, $\Pi(q)$ is UV-finite with **no regulator freedom** (check
K1) — the lattice removes the scheme-dependence F56 flagged as an open cost. F57 also (correctly,
for its own scalar-density channel, though F59 later shows the *sector identification* needs a
dimensional correction — §18.2.4) finds this particular coefficient $\Pi_2$ runs only
**logarithmically** with the cutoff (Adler–Zee running gravity), distinct from the $\Lambda^2$ scaling
of the $q=0$ (vacuum-energy) piece of the same integral.

$$\boxed{\;\text{the graviton kinetic term is generated by the matter back-reaction, not assumed: }\Pi_2=+0.061>0\text{, UV-finite on the compact BZ, no regulator freedom}\;}\tag{R18.2}$$

(F57, checks K1–K3; CL060, `open`, `falsifier: unset`.)

### 18.2.3 F58 — the clock-rate$\leftrightarrow$rest-mass coupling: universality is exact, the $4\pi$ and the Poisson *form* are forced, the magnitude is irreducible

F58 (2026-05-30) isolates the clock-rate channel specifically (as opposed to F56's generic
factorisation) and answers, piece by piece, whether the posited coupling
$\nabla^2_\text{lat}\Phi=4\pi G\rho$ follows from the neighbour rule. Four results, in increasing
order of what they leave open:

- **Q0 — universality (the weak equivalence principle) is exact.** Using exactly Chapter 11's
  renormalised rest frequency $\Omega_\text{rest}(x)=\sqrt{A(x)}\arcsin m$ (R11.12, extended here to
  a position-dependent lapse), the fractional clock-rate deficit $1-\sqrt A$ is **mass-independent**
  because $\sqrt A$ multiplies $\arcsin m$ as a common factor — residual $2.2\times10^{-16}$ across
  $m\in[0.01,0.9]$, bit-for-bit. Without this identity the question "does a single coupling $G$
  exist for all clocks" would be ill-posed; it is a structural consequence of the R11.12 rest-leg
  identity, not an assumption.
- **Q1 — the $4\pi$ is again lattice solid angle**, re-confirming F56's C2 in the clock-rate channel
  specifically (measured $4\pi C=1.0004$).
- **Q2 — the Poisson *form* is forced.** The neighbour-coupling symbol's leading small-$k$ term is
  the isotropic $\text{stiffness}\cdot|\mathbf k|^2$ (anisotropy spread $5.6\times10^{-8}$), and the
  unique local isotropic second-order operator with that symbol is $\nabla^2$ — so the field
  equation's *shape* is not a modelling choice.
- **Q3a/Q3b — the $c_\text{lat}$-dependence is locked exactly, but the absolute magnitude is not
  derivable at all.** Both $c_\text{lat}$ and the coupling's gradient stiffness descend from the
  single hopping amplitude $J$; sweeping $J$, $\text{stiffness}/c_\text{lat}^2$ is hopping-independent
  to $1.1\times10^{-16}$ — but this is the **tree-level** wave-operator stiffness (a kinematic
  identity, $S_\text{bare}=c_\text{lat}^2$, carrying no loop information), a point F58's own text
  mis-states as "$1/G\propto c_\text{lat}^2\propto\sqrt d$" (internally inconsistent, since
  $c_\text{lat}^2=1/d\ne\sqrt d$) and which F60 (§18.2.5) corrects. The *dimensionful* magnitude of
  $G$ — as opposed to its form — is irreducible: $G\propto\ell^2$ (Sakharov scaling, re-confirmed
  here with exponent $p=2.014$), and the lattice spacing in metres is not something a dimensionless
  rule can supply.

$$\boxed{\;\text{WEP exact }(2.2\times10^{-16})\text{; the }4\pi\text{ and the Poisson form are forced by the neighbour rule; the tree-level stiffness}/c_\text{lat}^2\text{ lock is exact }(1.1\times10^{-16})\text{ but is the wrong (tree) channel for the physical coupling; the dimensionful magnitude of }G\text{ is irreducible}\;}\tag{R18.3}$$

(F58, checks Q0–Q3b; CL061, `live`, `exact`, `falsifier: unset`.)

### 18.2.4 F59 — resolving the Sakharov sector, and the $(a,\tau)$ selection

F59 (2026-05-30) settles a tension left implicit in F56/F57: which Brillouin-zone integral *is*
$1/G$? Distinguishing the two Sakharov sectors by their dimension ($1/G\propto[\text{mass/length}]
\propto\Lambda^2$; vacuum energy $\propto[\text{energy/volume}]\propto\Lambda^4$), the integral
$\int d^3k/(2\omega)$ — F56/F57's object, measured $\Lambda^{2.085}$ — **is** the Newton sector; F57's
reassignment of this same integral's $q{=}0$ value to "the cosmological-constant sector" is corrected
here on dimensional grounds (F57's genuinely new content, the $q^2$-coefficient $\Pi_2$'s log
running, survives as a real but subleading correction on top of this leading $\Lambda^2$ piece, not
a replacement for it). For the relativistic sector $\omega=c_\text{lat}|\mathbf k|$ the integral is
analytic and exact: $\int_{|k|<\Lambda}d^3k/(2\pi)^3\,1/(2\omega)=\Lambda^2/(8\pi^2c_\text{lat})=
\sqrt d\,\Lambda^2/(8\pi^2)$ — confirmed $c$-independent to all digits under a hopping sweep,
locking $1/G\propto1/c_\text{lat}=\sqrt d$ **exactly**, the *opposite* $c_\text{lat}$-power from
F58's tree-level Q3a lock. Assembling the dimensionless lattice inverse-coupling
$I_\text{lat}=\eta\,g_*\int_\text{BZ}d^3k/(2\pi)^3\,1/(2\omega)$ with the lattice cell as the only
length and the Chapter-6-consistent constraint $a/\tau=c\sqrt d$ gives the **forced** scaling
(exact-algebraic given the $\Lambda^2$ exponent and the $\sqrt d$ factor):

$$a=\sqrt{2\pi\,\eta\,g_*}\;d^{1/4}\,\ell_P,\qquad \tau=\sqrt{2\pi\,\eta\,g_*}\;d^{-1/4}\,t_P.$$

With the placeholder values $\eta=1/12$ (minimal scalar) and $g_*=2$ (minimal Weyl content), the
prefactor $P_\text{pre}=\sqrt{2\pi\eta g_*}=\sqrt{\pi/3}=1.0233\approx1$ — suggestive of the clean
convention $a\approx d^{1/4}\ell_P$, but F59's own status line is explicit that this is
**"suggestive, not proven"**: $\eta$ is imported (not yet re-derived for a genuine Weyl spinor) and
$g_*$ is assumed (not yet counted from actual field content). F59 also names, without resolving, the
"channel fork" this leaves open: F58's tree channel and F59's loop channel give opposite signs of
the $d$-exponent, and reconciling them is F60's job.

$$\boxed{\;1/G\propto1/c_\text{lat}=\sqrt d\text{ (loop channel), exact under a hopping sweep; }a=\sqrt{2\pi\eta g_*}\,d^{1/4}\ell_P\text{ forced algebraically given the exponent; }P_\text{pre}\approx1\text{ for minimal content -- suggestive, not proven (}\eta,g_*\text{ both placeholders)}\;}\tag{R18.4}$$

(F59, Parts A–C; no independent claim card — subsumed into CL063/CL064/CL008.)

### 18.2.5 F60 — the channel fork: gap $=c_\text{lat}^3$ exactly, resolved (at this stage) by premise

F60 (2026-05-30) confirms the fork is real, not a bookkeeping slip: the tree-level bare wave-operator
stiffness $S_\text{bare}=c_\text{lat}^2$ and the loop-induced stiffness $B\propto1/c_\text{lat}$ scale
with exponents measured to $2.0000$ and $-1.0000$ respectively, and the gap $B/S_\text{bare}\propto
c_\text{lat}^{-3.0000}$ is exact — the universal difference between a *tree-level* operator's
stiffness and a *one-loop induced* stiffness over the relativistic phase space. Both computations
are correct; they answer different questions. F60's own resolution, at this point in the finding
chain, is explicitly an **argued premise, not a theorem**: the project has already committed to
*emergent* gravity (F52's rest-leg sourcing with no fundamental graviton kinetic term; F57's own
demonstration that the metric kinetic term is *generated*, not assumed) — in that ontology there is
no tree-level graviton stiffness to measure, so the physical coupling must be the loop channel $B$,
and F58's tree-level lock is reread as deriving the field equation's *form* (the $4\pi$, the
$\nabla^2$, the $c_\text{lat}$-structure of the bare operator used in the solver) rather than the
coupling's *magnitude*. F60 states its own limitation candidly: "if gravity instead had a fundamental
kinetic term, F58's $c_\text{lat}^2$ would be physical and the selection power would flip" — the
choice of channel is, at this stage, a *stated premise*, not yet derived.

$$\boxed{\;S_\text{bare}\propto c_\text{lat}^{2.0000}\text{ (tree)},\ B\propto c_\text{lat}^{-1.0000}\text{ (loop)},\ \text{gap}=c_\text{lat}^{-3.0000}\text{ exactly; loop channel selected by the project's emergent-gravity }\textbf{premise}\text{ (argued, not yet proved)}\;}\tag{R18.5}$$

(F60, checks tabulated in the finding; CL063, `live`, `machine`, `falsifier: unset`.)

### 18.2.6 F61 — the per-Weyl heat-kernel coefficient $\eta=1/12$, exactly, and the first field-content count

F61 (2026-05-30) turns F59's two placeholder inputs into numbers, starting with $\eta$. The flat
phase-space integral $\int d^3k/(2\pi)^3\,1/(2\omega)$ is **spin-independent** — verified on the
lattice to $4.4\times10^{-16}$, because the BCC Weyl unitary's two eigenphases have equal magnitude
— so all spin-dependence sits in the Seeley–DeWitt heat-kernel coefficient $a_1=\tfrac16R\,\text{tr}
\,\mathbb1-\text{tr}\,E$. Evaluated for a 2-component Weyl field (half a Dirac fermion, with the
Lichnerowicz curvature coupling and the fermionic statistics sign), the result is **exact**:

$$\boxed{\;\eta_\text{Weyl}=\tfrac1{12}\;}\tag{R18.6}$$

— confirming F59's placeholder was the correct value, not merely a convenient guess (rational
arithmetic, Seeley–DeWitt + Lichnerowicz + statistics, no fitting). Counting 2-component Weyl fields
in the model's then-known first-generation content ($L=2$, $e_R=1$, $Q=6$, $u_R=3$, $d_R=3$, plus the
sterile $\nu_R$) gives $g_*=16$ **per generation** — the count available to F61 at the time, before
Chapter 15's own three-generation theorem (F75) existed to multiply it by three. With $\eta=1/12$ and
$g_*=16$, $P_\text{pre}=\sqrt{\pi\cdot16/6}=2.894$, giving $a\approx3.81\,\ell_P$, $\tau\approx2.20\,
t_P$ — the clean $a\approx\ell_P$ of the minimal-content guess does **not** survive realistic field
content; the cell is several Planck lengths.

$$\boxed{\;\eta_\text{Weyl}=1/12\text{ exact (Seeley--DeWitt, rational); }g_*=16\text{ per generation (fermionic content known at the time); }a\approx3.81\,\ell_P,\ \tau\approx2.20\,t_P\;}\tag{R18.7}$$

(F61, Parts A–C; CL064, `live`, `exact`, `falsifier: unset`.)

### 18.2.7 F79 — the closure: the channel choice becomes a theorem, and $G$ is assembled in closed form

F79 (2026-06-02) is the chapter's central derivation of $G$, closing three separate open items from
F56–F61 with one observation. **The dielectric field $K$ is not a fundamental field on the lattice —
it is a reparametrization of the $(\mathbf E,\mathbf B)$ rotation rule (F64 §18.2.8 below), so it
carries no bare kinetic term, and its entire stiffness is forced to be the induced response.** The
argument that makes this precise, rather than merely asserted, is that the **source-free
electromagnetic stress tensor is exactly traceless in $3{+}1$D** — verified on 4000 random
$(\mathbf E,\mathbf B)$ configurations to $|T^\mu{}_\mu|_\text{max}=3.6\times10^{-15}$ (contrast: a
massive scalar has $T^\mu{}_\mu=m^2\phi^2\ne0$, control mean $0.49>0$, and *does* source $K$ — this
is precisely F52's rest-leg mass coupling). A traceless stress tensor couples to no conformal
degree of freedom at tree level (a Weyl rescaling couples through $T^\mu{}_\mu\,\delta\sigma$), so
the dominant lattice sector hands $K$ **zero tree stiffness**. There is nothing for F58's tree
channel to measure: the loop channel of F59/F60 is therefore *forced*, not chosen — F60's stated
premise becomes a theorem, without appeal to a general "emergent gravity" ontology.

**Every remaining input is now structural.** $c_\text{lat}=1/\sqrt d$ (F26/R6.5), $\eta_\text{Weyl}=
1/12$ (F61/R18.6, re-confirmed here), and — the decisive upgrade over F59–F61 — $g_*$ is no longer
"assumed three generations" but the **product of two independent structural counts**: 16 Weyl fields
per generation (anomaly-free, Higgs-free content, F38) times exactly 3 generations (F75's theorem
that $O_h$ has a unique odd cubic triplet $T_{1u}$ and no admissible 4-dimensional irrep — Chapter
15's result, forward-cited here; see Gap [G-8] below), giving $g_*=16\times3=48$ as an integer fixed
by representation theory rather than an input assumption. Assembling
$1/(16\pi G)=\eta\,g_*\int_\text{BZ}d^3k/(2\pi)^3\,1/(2\omega)/a^2$ with the lattice cell as the only
length and the R6.5-consistent constraint $a/\tau=c\sqrt d$:

$$\boxed{\;\frac1G=2\pi\,\eta\,g_*\sqrt d\;\frac{\hbar}{a^2c^3}\iff G=\frac{a^2c^3}{2\pi\,\eta\,g_*\sqrt d\;\hbar}\;}\tag{18.1}$$

with the **parameter-free coefficient** $2\pi\eta g_*\sqrt d=2\pi\cdot\tfrac1{12}\cdot48\cdot\sqrt3=
8\pi\sqrt3$, giving

$$\boxed{\;G=\frac{a^2c^3}{8\pi\sqrt3\,\hbar}\;,\qquad \frac{a}{\ell_P}=\sqrt{8\pi}\,3^{1/4}=6.59782\;}\tag{R18.8}$$

— this is exactly CLAUDE.md's own decision-4 closed form, re-derived here from the finding chain
rather than merely quoted. Anchoring $a=\ell_P$ for a self-consistency check (not the physical
anchor — see §18.4) reproduces $G=6.6743\times10^{-11}\,\text{m}^3\text{kg}^{-1}\text{s}^{-2}$ to
$3\times10^{-8}$ (CODATA round-off), confirming the algebra rather than fitting anything. F79's own
honest limit: only the *dimensionless* $a/\ell_P$ is predicted; the one length $a$ still needs an
independent SI anchor (Chapter 17), and the gauge-sector (spin-1) contribution to $g_*$ is not yet
included — a mild $\sqrt{\cdot}$ correction, since the *massless photon itself* is also conformally
invariant by the identical §18.2.7 argument and contributes zero tree stiffness of its own, leaving
only its subleading conformal-anomaly piece uncounted.

$$\boxed{\;\text{loop channel forced as a theorem (EM }T^\mu{}_\mu=0\text{, tree stiffness zero, }3.6\times10^{-15}\text{); }g_*=48\text{ structural (}16\times3\text{, F38}\times\text{F75); }G=a^2c^3/(8\pi\sqrt3\hbar)\text{, }a/\ell_P=6.5978\text{, self-consistent to }3\times10^{-8}\;}\tag{R18.9}$$

(F79, checks S1–S6; the structural half of CL008, `live`, `exact`.)

### 18.2.8 F64 — the dielectric construction, derived in full, as the vacuum/weak-field representation

F64 (2026-05-30, updated 2026-05-31) is the second derivation this chapter carries — not a route to
$G$'s magnitude, but to the *placement* of the metric's position-dependence. The starting fork:
factor-2 (Einstein) light bending needs the equivalent of two independently-sourced metric legs, and
a single dielectric $K(x)$ renormalising the $(\mathbf E,\mathbf B)$ rotation rule can supply both
from one field, because mass **is** confined rotation (F26) — there is no separate "mass substance"
to source a second leg from. Three results carry the full weight of this section:

**D-EM1 (exact, algebraic): only the dielectric placement passes both tests.** Of three
single-scalar metric placements — dielectric ($A=1/K,B=K$), clock-only (the F52 rest leg alone), and
refractive-only (Gordon) — only the dielectric gives redshift slope $Z=1$ **and** bend coefficient
$K_\text{bend}=4$ simultaneously, and it does so because the reciprocal lock $AB\equiv1$ keeps the
impedance $\sqrt{\mu/\varepsilon}=1$ exactly $u$-independent: the $(\mathbf E,\mathbf B)$ rotation
stays a *proper* rotation with no scalar contamination, exactly the BCC no-contamination criterion
Chapter 6 §6.2.5 (R6.9) already flagged as belonging to this sector.

**D-EM5 (derived, not posited): the placement $\varepsilon=\mu=K$ follows from conformal invariance
+ impedance matching.** The equivalent medium of a static isotropic metric is $\varepsilon=\mu=
\sqrt{B/A}$ (Plebanski); source-free Maxwell is conformally invariant in $3{+}1$D (the same
tracelessness §18.2.7 leans on), so the EM sector fixes only the *conformal class*, never the
conformal factor, and is blind precisely to the redshift/clock-rate scalar F52 already carries on
the rest leg. Demanding zero reflection (proper rotation, no impedance mismatch) forces
$\varepsilon=\mu=K$ uniquely — confirmed on a 1-D Yee FDTD step, where the impedance-matched form is
reflectionless to the grid floor ($R=0.009$) while the clock-only and refractive-only placements
reflect at Fresnel-scale $R\approx0.06$–$0.14$; **the reflected wave is exactly the scalar
contamination a proper rotation forbids.**

**D-EM9 (quantitative, the strong-field selector): the nonlinear completion is fixed by Mercury, not
by the EM-sector derivation alone.** D-EM5 fixes $K$ only to *linear* order in $u=GM/rc^2$ (through
the measured factor-1 redshift $\sqrt A=1-u$); the linear completion $K=(1-u)^{-2}$ gives $\beta=
\tfrac12$ and Mercury $50.1''$/cy — excluded by the MESSENGER bound. The impedance-matched
**exponential** completion $K=e^{2GM/rc^2}$ restores $\beta=\gamma=1$ exactly (GR-identical:
Mercury $42.98''$/cy, light bending $4GM/bc^2$), agreeing with the linear form at $O(u)$ and
correcting only $O(u^2)$: $(1-u)^{-2}=1+2u+3u^2+\dots$ vs. $e^{2u}=1+2u+2u^2+\dots$. This is the
canonical form CLAUDE.md decision 4 quotes.

Additional results from the same finding, stated for completeness: D-EM2/D-EM3 show a single
field-energy source (zero rest mass) deflects light by the same factor-2 as a rest-mass blob of
equal energy (ratio $1.00002$), where the rest-leg-only coupling gives zero — a real, dynamically
confirmed discriminator (D-EM6, dynamical light-bends-light on a propagating Maxwell pulse); D-EM7
gives the absolute 3-D ray-trace coefficient ($K_\text{bend}\to4$ from above); D-EM8 promotes $\Phi$
to a genuine dynamical field with a finite propagation speed $c_g$, energy-conserving.

$$\boxed{\;\text{only the impedance-matched dielectric passes }Z=1\text{ and }K_\text{bend}=4\text{ (D-EM1); }\varepsilon=\mu=K\text{ is derived, not posited, from conformal invariance + impedance (D-EM5, reflectionless to }0.009\text{); Mercury selects the exponential completion }K=e^{2u}\text{, }\beta=\gamma=1\text{ exactly (D-EM9)}\;}\tag{R18.10}$$

(F64, D-EM1–D-EM11; the representational half of CL008/CL015, `live`/`narrowed`, `exact`/`quantitative`.)

### 18.2.9 F106 — the sourcing law: the static weak-field reduction, coefficient exact, no free coupling

F106 (2026-06-06) closes F64's one remaining posited input — *how* the matter field $\psi$ sources
$K$ — by assembling three legs already established elsewhere in the tree: (1) the source is
$\psi$'s **energy density** $T^{00}[\psi]$, not bare probability $|\Psi|^2$, because mass *is*
confined rotation (F26) and radiation/rest-mass with equal $T^{00}$ source equally (F64 D-EM3, ratio
$1.00002$); (2) the coupling is F79's structural $G$ (§18.2.7), whose coefficient is now free of any
fitted constant because $K$'s stiffness is the induced response, not a bare kinetic term; (3) F64's
impedance lock converts $\Phi\to\ln K$ with the factor 2 that $AB\equiv1$ requires. Assembling:

$$\boxed{\;\nabla^2\ln K(\mathbf x)=-\frac{8\pi G}{c^4}\,T^{00}[\psi](\mathbf x)=-\frac{a^2c_\text{lat}}{\hbar c}\,T^{00}[\psi](\mathbf x)\;}\tag{R18.11}$$

— the coefficient collapsing to pure lattice quantities (no $G$, no $4\pi$, no free coupling),
verified exactly (E1, sympy zero residual) and confirmed on a Gaussian energy lump reproducing the
canonical $K=e^{2GM/rc^2}$ to $6\times10^{-4}$ (E3). **This is the sourcing law's honest scope,
stated precisely per the chapter's own hierarchy: it is the static / slow-matter Poisson reduction of
the full induced Einstein equation, sourced by energy density alone because the impedance lock
$AB\equiv1$ already forces the single scalar $K$ to carry both metric legs — not a competing
fundamental law.** F106 itself already names $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$ as this equation's
parent (a fact F178, §18.2.11, later promotes from a remark to the reason for a decision).

(F106, checks E1–E5; the sourcing half of CL008, `exact` coefficient.)

### 18.2.10 F173 — the pressure/Tolman discriminator: the argument *for* the full-tensor adoption

F173 (2026-06-29) asks the sharp question a single scalar cannot avoid: general relativity sources
the time potential by the trace-reversed stress-energy $\rho+3p/c^2$ (the Tolman term — pressure
gravitates); does the F64/F106 dielectric reproduce it, or omit it? The exact Einstein tensor of the
isotropic dielectric metric $ds^2=-K^{-1}dt^2+K(dr^2+r^2d\Omega^2)$ answers this with sympy-exact
algebra (zero residual): the single scalar's effective stress is $p_r=-p_t=-e^{-2u}u'^2/(8\pi)$ —
**anisotropic** field stress, present even in vacuum, with **no isotropic matter-pressure component
at all**. A perfect fluid has $p_r=p_t$; the dielectric forces $p_r=-p_t$ identically. So for an
equation of state $p=w\rho c^2$ the model omits the fraction $3w/(1+3w)$ of GR's time-potential
source — null for dust ($w=0$, exactly the solar-system regime, which is why every classical test
passes), but $23\%$ for a representative neutron-star equation of state and up to $50\%$ for
radiation. The leading strong-field coefficient is exact: $g_{tt}^\text{model}(0)-g_{tt}^\text{GR}(0)
=-\tfrac{15}4 s^2+O(s^3)$ ($s=GM/Rc^2$), giving illustrative (uniform-sphere) departures of $2$–$42\%$
inside neutron-star interiors while the exterior fields — and hence every solar-system test — remain
untouched.

$$\boxed{\;\text{a single impedance-locked scalar forces anisotropic effective stress }p_r=-p_t\text{ (sympy-exact) and carries no isotropic matter-pressure source; omitted GR source fraction }=3w/(1+3w)\text{; leading strong-field coefficient }-15/4\text{ exact}\;}\tag{R18.12}$$

**This is presented here precisely as `00-plan.md`'s own instruction requires: as the argument that
forces the full-tensor decision, not as a surviving strong-field prediction of the dielectric.**
F173's own supersession banner (S4) states this outright — the departure is reclassified as "an
artifact of the weak-field reduction, not a prediction" the moment the full-tensor source is adopted
(§18.2.11); what survives unconditionally is the *exact tensor algebra itself*, which is what
motivated the decision in the first place.

(F173, checks P1–P4; CL153, `live`, `exact`, `unreviewed-seed`, `falsifier: unset`.)

### 18.2.11 F178 — the decision: the induced Einstein equation is canonical; the dielectric is demoted

F178 (2026-06-29) is the chapter's central act, and it is explicitly a **decision**, not a new
computation — it reclassifies the canonical status of results already derived elsewhere in the tree,
for three independent reasons stated in full:

1. **Lorentz covariance.** A source built from $T^{00}$ alone is not a tensor equation — $T^{00}$ is
   frame-dependent and mixes with momentum density and stress under a boost — so the energy-only law
   can only ever be a *static, preferred-frame* approximation, never the fundamental dynamical law.
2. **The model already named the parent.** F106 itself derived $\nabla^2\ln K=-8\pi T^{00}$
   explicitly as "the static weak-field reduction of the induced Einstein equation
   $G_{\mu\nu}=8\pi G\,T_{\mu\nu}$" (§18.2.9 above) — this decision promotes that stated parent from
   "the thing we reduce" to "the law."
3. **Neutron stars.** The literal energy-only law has no maximum mass and predicts $R\approx20$ km at
   $2\,M_\odot$ — excluded by PSR J0740+6620 (F174, outside this chapter's assigned set but named in
   F178's own text).

**What it entails.** By F173 (exact, §18.2.10), the impedance-locked single scalar forces anisotropic
stress and cannot satisfy an isotropic-perfect-fluid source under the full tensor equation. Therefore:
**inside matter** the metric must carry its second independent function, and the dynamics are general
relativity (TOV) — the single scalar is no longer the field equation there. **In vacuum**
($T_{\mu\nu}=0$) the impedance lock $AB\equiv1$ and the dielectric/rotation-rate picture survive
exactly as the weak-field representation — but the *exact* vacuum solution is **Schwarzschild**, not
the exponential $K=e^{2u}$, which agrees only to PPN order and differs at $O(u^2)$.

**The supersession map, reproduced precisely because it is the chapter's headline reclassification
table.** Preserved: factor-2 light bending, $\beta=\gamma=1$, Mercury $42.98''$/cy, Shapiro,
gravitational redshift (F64 D-EM9); the structural/induced $G=a^2c^3/(8\pi\sqrt3\hbar)$ (F79); the
emergent-origin picture itself. F64 is demoted to "vacuum/weak-field representation." F106 is
reclassified as "the static weak-field reduction," as it already named itself. **F114 (the
horizon-free dielectric black hole, not one of this chapter's sixteen findings — full treatment in
§18.6) is superseded**: the exact vacuum solution is Schwarzschild, with a horizon. F173/F174's
energy-only departures become the diagnosis that forced this decision, not a model prediction.

$$\boxed{\;\text{induced Einstein equation }G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}\text{ canonical, full stress-energy source; single-scalar dielectric demoted to vacuum/weak-field representation; interior dynamics are GR/TOV; exact vacuum solution is Schwarzschild, not }K=e^{2u}\;}\tag{R18.13}$$

(F178, decision + cross-checks against F173/F174/F176; the reclassification half of CL008/CL015/CL023.)

### 18.2.12 F345 — field-equation uniqueness: the two-derivative left-hand side is inherited from the model's own derived dimension

F345 (2026-09-01, reviewed CONFIRMED-NARROWER after a full cold-agent attack) asks a question F178's
decision note never addressed: given that the source is the full stress-energy tensor (F178) and
that the theory is a local, diffeomorphism-invariant metric theory, *is the left-hand side
$aG_{\mu\nu}+bg_{\mu\nu}$ forced, or merely chosen?* The argument runs in five legs. **L1** (the
Bianchi identity, checked as a guard against a coding error rather than claimed as new mathematics):
any local field equation $E_{\mu\nu}=aG_{\mu\nu}+bg_{\mu\nu}$ forces $\nabla^\mu S_{\mu\nu}=0$ on its
source. **L2/L2b** (exact, sympy): the metric variation of a matter action *is* a symmetric
10-component tensor with $\nabla^\mu T_{\mu\nu}$ identically equal to the matter field equation — the
full-tensor source is not a choice, it is what a variational principle returns. **L3, the load-bearing
new step**: Lovelock's theorem says that in $d=4$ (and *only* $d=4$, among dimension-dependent
routes) the unique symmetric divergence-free rank-2 tensor built to second order from the metric is
$aG_{\mu\nu}+bg_{\mu\nu}$ — verified here on a generic algebraic curvature tensor (24 random rational
Kulkarni–Nomizu combinations, later strengthened by the cold reviewer to a full 20-symbol symbolic
proof): the Lanczos–Lovelock tensor $H_{\mu\nu}$ vanishes identically in $d=4$ and is generically
nonzero (25 components) in $d=5$. **Because this model derives $d_\text{space}=3$ from two
independent selectors (F291) with the residual "+1" closed against no second candidate generator
(F326) — Chapter 2's R2.x results — Einstein uniqueness here is not an extra postulate about
gravity; it is inherited from the already-derived spacetime dimension.** (The finding's own honest
pincer, disclosed in full: uniqueness *linear in $\partial^2g$* is dimension-independent (Vermeil/
Weyl/Cartan); it is only the stronger, *not-linear-in-$\partial^2g$* reading — the honest choice for
a derivative expansion — that makes the dimension do real work, and that reading in turn needs
"at-most-second-order" to hold as more than a formal truncation.)

**L4** — the two-derivative truncation is a **decade estimate, not a bound** (the finding's own
correction of its first version, after the cold review): the leading four-derivative correction is
$\sim10^{-76}\times$ an **uncomputed** $O(1)$ gravitational Wilson coefficient — nowhere in the tree
is that coefficient actually computed; only the order of magnitude is defensible, and the review
found three separate numerical errors (wrong finding cited for the coefficient, wrong curvature
invariant at a horizon, wrong extremal mass) in the finding's first pass, all corrected in the
version read for this chapter. **L5/L6** — Brans–Dicke and metric $f(R)$ are shown **absent for want
of a parameter**, not refuted: the model's PPN $\gamma=1$ exactly, its structure-formation slip
$\Sigma-1$ and $\partial\mu/\partial k$ both literal sympy zeros, and $\dot G/G\equiv0$ (a rigid
substrate) together match no finite Brans–Dicke $\omega$ nor an unscreened $f(R)$'s $\gamma=1/2$ —
but the finding's own honest concession is that three of these four signatures share one premise
($AB\equiv1$/F106), itself downstream of the very law under question, so as an *exclusion of a rival
theory* the argument is partly circular; what it establishes cleanly is only the model's own
*parameter content* (it has none to build a Brans–Dicke or chameleon $f(R)$ from), not an independent
refutation. Vainshtein-screened Horndeski, vector-tensor, and bimetric theories are explicitly named
as untouched by this argument.

$$\boxed{\;\text{given a local, diff-invariant metric-only theory, the two-derivative field equation }aG_{\mu\nu}+bg_{\mu\nu}\text{ is forced by Lanczos--Bach/Lovelock at the model's own derived }d=4\text{; the full-tensor source is forced by the metric variation itself; the two-derivative truncation holds to }\sim10^{-76}\times\text{an }\textbf{uncomputed}\text{ }O(1)\text{; Brans--Dicke/}f(R)\text{ are absent for want of a parameter, not refuted}\;}\tag{R18.14}$$

**The one residual posit, stated by F345 itself and carried here without softening**: that the
long-wavelength lattice description is a local, diffeomorphism-invariant *metric* theory *at all* —
Lorentzian signature, torsion-free, metric-compatible, at most second order, metric-only on the
left-hand side. F345 names two of those five conditions as genuinely open (at-most-second-order per
L4; metric-only-LHS closed only against Brans–Dicke/$f(R)$, not the wider zoo), and cites the
literature (Sindoni, arXiv:1110.0686) that the emergence of an effective Lorentzian metric from a
discrete substrate is "not generic" — the honest statement that this residual posit is not a
formality.

(F345, legs L1–L7, three controls verified RED — `lovelock_dim=5`, `gb_ricci_coeff=-3`,
`model_gamma=0.999999`; CL292, `contingent`, `quantitative`, `falsifier: stated`.)

### 18.2.13 F383 — the negative sub-result: locality generates, not forbids, the four-derivative term

F383 (2026-09-10, reviewed CONFIRMED-NARROWER) attacks F345's own "at-most-second-order" sub-item
directly, extending F57's own $\Pi(q)$ machinery (§18.2.2) one order further in the small-$q$
expansion: $\Pi(\mathbf q)=\Pi_0-\Pi_2q^2+\Pi_4q^4-\dots$, where $\Pi_2$ is the already-accepted
induced Einstein–Hilbert coefficient and $\Pi_4$ is the scalar-channel analogue of a
curvature-squared operator. **The question is whether the lattice's own locality can forbid this
term outright (which would promote the truncation from posit to derivation), or only ever suppress
it (ordinary Wilsonian EFT, with a generically nonzero coefficient).** The answer, computed rather
than assumed: $\Pi_4$ is robustly **nonzero and of consistent sign** across four independent
perturbations (finer grid, wider $q$-window, a different lattice direction, and — added after the
cold review flagged a fit-order artifact — an explicit $q^6$-augmented fit that shifts the *magnitude*
by $2.6$–$3\times$ but never the sign), and converges under grid refinement (a genuine finite
integral, not a quadrature artifact). The mechanism that would exclude a four-derivative term — the
$d=4$-specific vanishing of the Gauss–Bonnet variation, F345's L3 — is a property of the *full
nonlinear curvature-squared invariant under a metric variation*; it has no analogue in a scalar
matter-density polarization, and nothing in the model's construction gives $\Pi_2,\Pi_4,\Pi_6,\dots$
a reason to vanish at any order. Locality is why every term in the tower is UV-finite (the compact
Brillouin zone removes the regulator ambiguity, exactly as F57 showed for $\Pi_2$) — **it is not why
the tower stops.**

$$\boxed{\;\Pi_4\text{ is robustly nonzero, same sign across five independent perturbations (M2/M2b), converges under grid refinement (M3); locality forbids nothing -- it UV-finitises every order of an ordinary EFT derivative tower; F345's at-most-second-order sub-item closes }\textbf{negative}\;}\tag{R18.15}$$

**This is an honest, disclosed exclusion within F345's own uniqueness argument, not a result to be
smoothed over.** F383's own text is explicit about what this does and does not do: it does not
compute the actual gravitational $R^2$/Ricci$^2$ Wilson coefficient F345's L4 left uncomputed (that
remains open, in the kinetic-leg $T_{ij}T_{kl}$ channel F57 already flagged); it closes only the
narrower, logically prior question of whether locality *forbids* the term outright, and the answer
is that it does not — the "at-most-second-order" premise stays a decade-scale empirical suppression,
never promoted to an exact symmetry statement. F383 carries no separate claim card, per its own
disclosure: it closes a candidate promotion route with a negative result but does not itself extend,
derive, or contradict Standard Model/GR content beyond what F345 already established.

(F383, legs M1–M5, L, M2b; test record `F383-four-derivative-locality`, `result_dump`, battery tier,
7/7 PASS. No independent claim card.)

### 18.2.14 F63 — the cost of the torsion-free assumption: a bounded residual, not a clean closed result

F63 (2026-05-30) is the chapter's one honest caveat rather than a settled derivation. The project
works torsion-free throughout (F50/F52/F62), dropping the Einstein–Cartan spin-torsion four-fermion
contact term a first-order (Palatini) variation would generate. F63 asks whether that omission costs
anything measurable at the densities the model actually runs. Using a **conservative, polarised
upper bound** on the axial bilinear (never numerically contracting $\gamma_5\gamma^\mu$, per the
CLAUDE.md chiral-transform caveat — the bound is deliberately worst-case), the closed-form ratio of
the Einstein–Cartan four-fermion density to the Dirac density scales linearly in occupation:
$r_\text{cutoff}(f)=3f/(4\eta g_*\sqrt d)$, using F61's pinned cell $a=3.81\,\ell_P$ ($g_*=16$, the
one-generation count available at the time — not F79's later $g_*=48$, a minor internal
inconsistency this chapter does not resolve since F63 itself never revisits the cell size). At the
model's actual dynamical-fermion test densities (F62's Gaussian wavepackets, peak occupation
$f\sim10^{-3}$–$10^{-2}$ quanta/cell), the ratio is $\le2.9\times10^{-3}$ — **≲0.3%, well below every
quantitative tolerance those tests already carry.** Torsion becomes order-unity only at
$f^*\approx3.08$ quanta per cell — essentially Planck-scale packing, several fermions crammed into
one $\sim3.8\,\ell_P$ cell.

$$\boxed{\;\text{Einstein--Cartan spin-torsion is}\lesssim0.3\%\text{ at the model's actual test densities (conservative bound); reaches }O(1)\text{ only at }f^*\approx3\text{ quanta/cell, essentially Planck-scale packing}\;}\tag{R18.16}$$

**This vindicates, but does not derive, the torsion-free choice.** F63 is explicit that it is a
*pre-check*, not a dynamical torsion simulation: "an actual dynamical torsion field co-evolved with
the Dirac CA" is named as open work (plan item D3b) that this finding screens as safely ignorable at
current densities, not one it performs.

(F63, checks EC-coefficient/cell/densities/Cartan-density; CL066, `live`, `exact`, `falsifier: unset`.)

### 18.2.15 F243/F244 — observational checks: two falsification attempts fail

F243 (2026-07-03) attempts to falsify the F3 lensing prediction at low fermion density — the
standing worry that the depression sourcing gravitational lensing might reverse sign, vanish
discontinuously, or break its linear source law as density drops. Scaling the fermion density from
$\rho=1$ down to $\rho=10^{-3}$ (nine orders above machine epsilon), the depression **stays
correct-sign, positive-definite, and scales linearly** (weak-field log-log slope $1.012$ against an
ideal $1.000$) at every density tested — the mild super-linearity at $\rho=1$ is ordinary strong-field
saturation, not a low-density pathology. **NOT FALSIFIED.**

F244 (2026-07-03) closes a related open item: the earlier lensing scan (F3b) confirmed only the
*sign* of deflection, using a phenomenological metric with a free fit exponent $\alpha=1.5$. Re-run
on the genuine 3-D EMQG Newtonian potential (a true $1/r$ Green's function, not the dimensionally
inconsistent 2-D logarithmic potential of an earlier test) with the parameter-free GR-Shapiro
coupling, the deflection obeys $\Delta\theta\propto1/b$ with **no free exponent**: the exact
continuum thin-lens closed form gives slope $-0.9959$ (machine $1/b$), the lattice isolated-slice
line integral gives $-1.074$, the periodic-FFT slice gives $-1.062$ (both residuals from $-1$ named
as finite-grid/periodic-image artifacts, not physics), and a dynamical Cayley-stepper wave-packet
probe reproduces the deflection toward the mass with norm conserved to $\sim3\times10^{-15}$ at
every impact parameter tested.

$$\boxed{\;\text{F243: low-density lensing NOT FALSIFIED -- correct sign, linear scaling (slope }1.012\text{) to }\rho=10^{-3}\text{. F244: 3-D EMQG lensing obeys }\Delta\theta\propto1/b\text{ with no free exponent, continuum slope }-0.9959\;}\tag{R18.17}$$

(F243, 6/6 checks; F244, 5/5 checks; both cross-referenced from CL008's evidence chain via F64/F106.)

## 18.3 Results table

Exactness class and test record for each result; **[FUND]** marks a result belonging to the
fundamental full-tensor law (F178/F345), **[REP]** marks a result belonging to the vacuum/weak-field
*representation* (F64/F106), and **[STRUCT]** marks the structural derivation of $G$ itself, which is
prior to and independent of the FUND/REP split.

| # | Statement | Class | Exactness | Test record |
|---|---|---|---|---|
| R18.1 | **[STRUCT]** $16\pi$ (Newton's solid angle + trace reversal) exact; $G\propto\ell^2$ Sakharov scaling | exact (geometric) / scaling (magnitude) | residual $0.0$; exponent $2.0008$ | F56; `test_F56_einstein_coupling_derivation.py` (3/3) |
| R18.2 | **[STRUCT]** Induced EH kinetic term is generated ($\Pi_2=+0.061>0$), UV-finite, no regulator freedom | quantitative | K1/K2/K3 | F57; `test_F57_induced_eh_from_backreaction.py` (3/3) |
| R18.3 | **[STRUCT]** WEP exact; $4\pi$/Poisson form forced; magnitude irreducible without a ruler | exact (Q0, Q3a) / derived (Q1, Q2) / open (Q3b) | $2.2\times10^{-16}$ (Q0); $1.1\times10^{-16}$ (Q3a) | F58; `test_F58_clockrate_coupling_derivation.py` (5/5) |
| R18.4 | **[STRUCT]** $1/G\propto1/c_\text{lat}=\sqrt d$ (loop, exact); $a\propto d^{1/4}\ell_P$ forced given the exponent; $P_\text{pre}\approx1$ suggestive | exact (scaling) / suggestive (prefactor) | $c$-flat to all digits | F59; `test_F59_induced_eh_prefactor.py` |
| R18.5 | **[STRUCT]** Tree/loop channel gap $=c_\text{lat}^3$ exactly; loop selected by premise (pre-F79) | exact (gap) / argued (selection) | exponents $2.0000,-1.0000,-3.0000$ | F60; `test_F60_channel_reconciliation.py` (4/4) |
| R18.6 | **[STRUCT]** $\eta_\text{Weyl}=1/12$ exact; $g_*=16$/generation (content known at the time) | exact ($\eta$) / fixed-from-content ($g_*$) | rational; $4.4\times10^{-16}$ (spin-independence) | F61; `test_F61_weyl_eta_gstar.py` (3/3) |
| R18.7 | **[STRUCT]** EM $T^\mu{}_\mu=0\Rightarrow$ zero tree stiffness $\Rightarrow$ loop channel forced (theorem); $g_*=48=16\times3$ structural; $G=a^2c^3/(8\pi\sqrt3\hbar)$, $a/\ell_P=6.5978$ | exact | $3.6\times10^{-15}$ (S3); $3.0\times10^{-8}$ (S6, CODATA) | F79; `test_F79_structural_G.py` (6/6) |
| R18.8 | **[REP]** Only the impedance-matched dielectric passes $Z{=}1$ and $K_\text{bend}{=}4$; $\varepsilon=\mu=K$ derived (D-EM5); Mercury selects $K=e^{2u}$, $\beta=\gamma=1$ | exact (D-EM1, D-EM5) / quantitative (D-EM9) | $R=0.009$ (D-EM5); $42.98''$/cy (D-EM9) | F64; `test_F64_em_connection.py` (16/16) |
| R18.9 | **[REP]** $\nabla^2\ln K=-(8\pi G/c^4)T^{00}[\psi]$, coefficient exact, no free coupling | exact (E1, coefficient) / lattice (E2/E3, $\le2\%$) | $0$ (E1); $6\times10^{-4}$ (E3) | F106; `test_F106_psi_K_sourcing.py` (5/5) |
| R18.10 | The single scalar forces anisotropic stress $p_r=-p_t$, omits GR's $3p$ source — **the argument for** F178, not a surviving prediction | exact (tensor algebra) / illustrative (NS magnitude) | sympy zero residual; $-15/4$ exact leading coeff. | F173; `test_F173_tolman_pressure.py` (4/4) |
| R18.11 | **[FUND]** $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ adopted canonical (three reasons); interior = GR/TOV; exact vacuum = Schwarzschild | decision (reclassification) | — | F178; decision note, `docs/theory/key-decisions.md` |
| R18.12 | **[FUND]** Two-derivative LHS forced by Lanczos–Bach/Lovelock at the model's derived $d=4$; full-tensor source forced by variation; truncation $\sim10^{-76}\times$ uncomputed $O(1)$ (decade, not bound); BD/$f(R)$ absent for want of a parameter | exact (L1–L3) / order-of-magnitude (L4) / narrowed (L5/L6) | 3 controls RED | F345; `F345-field-equation-uniqueness` (8/8, gate) |
| R18.13 | **[FUND]** Locality generates, does not forbid, the four-derivative term; $\Pi_4$ robustly nonzero — L4's premise closes **negative** | quantitative (sign/order robust, magnitude fit-order-dependent) | 5/5 legs + M2b regression | F383; `F383-four-derivative-locality` (7/7, battery) |
| R18.14 | Einstein–Cartan spin-torsion $\lesssim0.3\%$ at model densities, $O(1)$ only at $f^*\approx3$ quanta/cell | exact (coefficient, scaling law) / conservative bound (magnitude) | $3/16$ exact; $f^*=3.08$ | F63; `test_F63_spin_torsion_estimate.py` (5/5) |
| R18.15 | Low-density lensing NOT FALSIFIED, slope $1.012$ to $\rho=10^{-3}$; 3-D $1/b$ lensing, no free exponent, slope $-0.9959$ | quantitative | see §18.2.15 | F243 (6/6); F244 (5/5) |

## 18.4 Comparison with measurement

**PPN parameters and Mercury.** $\beta=\gamma=1$ exactly (F64 D-EM9, R18.10), giving Mercury's
perihelion advance $42.98''$/century against the observed $42.98''\pm0.04$. Under F178 this is
reported precisely at its post-decision status: **not a distinctive prediction, but a consistency
requirement** — in vacuum the model *is* general relativity, so a confirmed PPN deviation would
falsify it exactly as it would falsify GR. The genuinely discriminating content that survives is the
*exclusion* of the naive linear dielectric ($\beta=\tfrac12$, $50.1''$/cy), which was a live internal
alternative and is now dead (CL015, `narrowed`).

**Newton's constant.** $G=a^2c^3/(8\pi\sqrt3\hbar)$ (R18.9) is a genuinely structural derivation, but
this chapter fixes only the *dimensionless* content $a/\ell_P=6.5978$ — **no SI value of $G$ is
produced here.** The self-consistency check anchoring $a=\ell_P$ reproduces CODATA's $G$ to
$3\times10^{-8}$, but that anchor is circular if $G$ is the output being derived; the genuinely
independent route (anchoring $a$ through a measured fermion mass via the lattice-mass map) is
Chapter 17's derivation, forward-cited rather than performed here.

**Lensing.** F243/F244 (R18.17) survive two dedicated falsification attempts: the lensing depression
stays correct-sign and linear down to $\rho=10^{-3}$, and the 3-D EMQG deflection obeys
$\Delta\theta\propto1/b$ with the free fit exponent of an earlier test eliminated. Neither result
fixes the *absolute* normalisation against a specific lensing survey; both are internal
consistency/shape checks on the model's own weak-field machinery.

**Neutron stars.** The 2–42% interior departure F173 computed (R18.10) is explicitly **not** compared
to NICER or PSR J0740+6620 data as a model prediction in this chapter's assigned findings — F178
reports the literal energy-only law's *absence* of a maximum mass as excluded by PSR J0740+6620 (a
different finding, F174, outside this chapter's set), and F173's own tensor result is carried here
as the argument that motivated the decision, per `00-plan.md`'s explicit instruction, not as a
surviving quantitative prediction to be scored against data.

## 18.5 What was excluded, and why

- **F114 — the horizon-free dielectric black hole — superseded by F178 (`docs/theory/
  supersessions.yaml` record S4-F178-full-stress-energy).** F114 is **not** one of this chapter's
  sixteen assigned findings (it is routed to Appendix A2), but its retirement is this chapter's
  direct consequence and belongs here in full. Before F178, treating the exponential metric
  $K=e^{2GM/rc^2}$ as the *exact* (not merely PPN-order) vacuum metric gave a throat rather than a
  horizon — a $+4.6\%$ larger photon-ring shadow, no maximum compactness, and consequences that
  propagated into a withdrawn claim series (CL023–CL027: the horizon-free condensate itself, the
  $+4.63\%$ shadow prediction, ringdown echoes, an absent thermal Hawking spectrum, a $4\pi$
  second-order bending coefficient — all `withdrawn`, confirmed by CL023 read in full). **Under
  F178, the exact vacuum solution is Schwarzschild, with a horizon**, because the exponential $K$ is
  now understood to be only the PPN-order approximation to the true vacuum solution, differing at
  $O(u^2)$. This is inverted, not merely narrowed: an observation of a horizon, which the pre-F178
  reading would have scored as a falsification, is now the model's own prediction. **The exact
  Schwarzschild/Kerr treatment that replaces F114 is Chapter 19's, forward-cited here rather than
  performed.**
- **The rest-leg two-metric-legs route (F50/F52/F55/F62).** Not one of this chapter's findings, but
  named throughout §18.2 as the construction F64 superseded (`supersessions.yaml` record S3): where
  the rest-leg route needs two independently-sourced metric legs for factor-2 bending, F64's single
  impedance-matched dielectric gets both from one field. `supersessions.yaml` records nothing of
  F50/F52/F55/F62 survives independently — full retirement, not a partial one.
- **The naive linear dielectric $K=(1-u)^{-2}$.** Derived and then excluded within F64 itself
  (D-EM9, R18.10): it satisfies the EM-sector derivation to linear order but gives $\beta=\tfrac12$,
  Mercury $50.1''$/cy, excluded by MESSENGER. Retained only for the D-EM1/D-EM9 form comparison, not
  as a live alternative.
- **Brans–Dicke and metric $f(R)$ gravity.** Not refuted, per F345's own careful language (§18.2.12,
  R18.14): the model's exact $\gamma=1$, zero structural slip, and $\dot G/G\equiv0$ leave no finite
  Brans–Dicke $\omega$ or unscreened $f(R)$ consistent with the model's own numbers, but this is
  reported as **absence of a parameter to build one from**, not as an independent theoretical
  exclusion — three of the four signatures share the $AB\equiv1$/F106 premise, itself downstream of
  the law under test.
- **The energy-only sourcing law read as fundamental.** F106's own $\nabla^2\ln K=-(8\pi G/c^4)T^{00}$
  is retained in full (its coefficient is exact, R18.11) but explicitly demoted to the static
  weak-field reduction — this is the chapter's central hierarchy statement, not a separate exclusion.

## 18.6 What is still open

1. **F63's torsion-free residual is a bounded estimate, not a dynamical result.** ≲0.3% at the
   model's actual test densities, order-unity only at Planck-scale packing (R18.16) — but no
   dynamical torsion field has been co-evolved with the Dirac CA (plan item D3b, explicitly named as
   open by F63 itself). F63's own cell-size input ($a=3.81\,\ell_P$, $g_*=16$) also predates F79's
   later $g_*=48$; this chapter does not resolve that internal inconsistency, only discloses it.
2. **F383's negative sub-result leaves the actual gravitational $R^2$/Ricci$^2$ Wilson coefficient
   uncomputed.** F345's L4 already disclosed this as an order-of-magnitude estimate rather than a
   bound; F383 forecloses one route (locality-forced vanishing) to sharpening it, but does not itself
   supply the coefficient — that computation lives in the kinetic-leg $T_{ij}T_{kl}$ channel F57
   first flagged as open and F79/F106 never revisited.
3. **F345's own residual posit — that a local, diffeomorphism-invariant metric description emerges
   at all — is not derived, and the literature it cites (Sindoni, arXiv:1110.0686) is explicit that
   this emergence is "not generic" for a discrete substrate with a preferred frame.** What would
   close it is a derivation that the model's block-spin/coarse-graining flow (F130, outside this
   chapter) *drives* the long-wavelength effective action to a metric functional, rather than that
   form being assumed — named by F345 as the actual substantive open problem, not a technicality.
4. **The gauge-sector contribution to $g_*$ is not yet included.** F79's own honest limit: the
   massless photon is itself conformally invariant (zero tree stiffness by the identical §18.2.7
   argument) and contributes only its subleading conformal-anomaly piece, not yet computed; $W$/$Z$/
   gluon contributions carry their own spin-1 heat-kernel coefficients (with ghosts) and are not
   computed anywhere in this chapter's findings. Flagged as a mild $\sqrt{\cdot}$ correction to
   $a/\ell_P$, not expected to change the qualitative picture.
5. **F345's L5/L6 exclusion of Brans–Dicke/$f(R)$ does not extend to Vainshtein-screened Horndeski,
   vector-tensor (Einstein-aether, TeVeS), or bimetric theories** — named explicitly as untouched.

> **Gap [G-8].** F79's assembly of $g_*=48$ (§18.2.7, R18.9) — the structural fermion-content count
> that is the single largest numerical input to the closed-form coefficient $8\pi\sqrt3$ — depends
> on two findings this chapter does not itself derive: F38 (the anomaly-free, Higgs-free 16-Weyl
> content per generation, Chapter 12) and, more sharply, **F75** (the theorem that $O_h$ point-group
> representation theory forces exactly three generations, assigned to **Chapter 15**). Neither
> dependency appears in `00-plan.md`'s stated dependency table for Chapter 18, which lists only
> Chapter 6 and Chapter 11 as inputs. This is not a circularity — F75 is a purely group-theoretic
> result about the BCC point group, independent of anything in this chapter — but it is a genuine,
> previously unrecorded cross-chapter dependency: a reader checking "what does Chapter 18 assume"
> against the plan's dependency column alone would miss that its own headline numerical coefficient
> ($8\pi\sqrt3$, and hence $a/\ell_P=6.5978$) is not assembled without a result Chapter 15 supplies.
> Flagged here rather than silently building the coefficient as if $g_*=48$ were this chapter's own
> input; whoever assembles Appendix A5's final dependency ledger should add Ch.15 (and, more weakly,
> Ch.12 for F38) as inputs to Ch.18, mirroring how Chapter 6 resolved its own analogous Gap [G-2].

## 18.7 Falsifiers

From the relevant claim cards, reported at their actual status:

1. **CL008 (the headline structural claim) carries `falsifier: stated`**: PPN $\beta=\gamma=1$
   (Mercury $42.98''$/cy); the naive linear dielectric is excluded. Under F178 this is explicitly a
   **consistency requirement rather than a distinctive prediction** — the model reproducing GR
   exactly in vacuum means a confirmed PPN deviation falsifies it exactly as it would falsify GR,
   no more and no less.
2. **CL015 (Mercury/PPN specifically) carries `falsifier: stated`, `status: narrowed`** — the same
   threshold as CL008, explicitly demoted from "a distinctive prediction of the exponential metric"
   to "a consistency requirement," with the genuinely discriminating content narrowed to the
   internal exclusion of $\beta=\tfrac12$.
3. **CL153 (F173's Tolman discriminator) carries `falsifier: unset`** — declared debt in the claims
   layer (D12), not a claim that no falsifier exists. Its own status line records that the finding is
   `unreviewed-seed`, extracted mechanically and not yet independently confirmed; a genuinely
   quantitative neutron-star falsifier would require the self-consistent stellar-structure solve
   F173 itself names as open (a comparison against NICER mass–radius data on each theory's own
   hydrostatic equation), not performed by this chapter's findings.
4. **CL292 (F345's uniqueness argument) carries `falsifier: stated`, `status: contingent`** — the
   argument's own dependency structure (on F178's decision, on F79/F107's structural $G$, on
   F291/F326's derived dimension) means its status moves if any of those move; it is not an
   independently standing falsifier.
5. **F345's own three declared controls provide the sharpest structural falsifiers available in this
   chapter**: the code's `lovelock_dim=5` perturbation must (and does) turn L3 red; `gb_ricci_coeff=
   -3` must (and does) break the Lanczos–Bach identity; `model_gamma=0.999999` must (and does) admit
   a finite Brans–Dicke $\omega$, closing L5 only by exactness rather than by the wider Cassini bound.
   A recomputation returning any of these three green would falsify the corresponding leg outright,
   as a closed-form algebraic claim rather than an observational one.
6. **CL023 (the withdrawn dielectric black hole) is `withdrawn`, and its falsifier is explicitly
   inverted**, per §18.6: an observation of a horizon, which the pre-F178 model would have scored as
   a falsification, no longer is one.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $K(x)$ | The single lattice dielectric index, $A=1/K,\ B=K$, canonical form $K=e^{2GM/rc^2}$ — the vacuum/weak-field **representation** of the fundamental law, not the law itself | §18.2.8 |
| $G$ | The structural/induced Newton constant, $G=a^2c^3/(8\pi\sqrt3\,\hbar)$; dimensionless content $a/\ell_P=\sqrt{8\pi}\,3^{1/4}=6.5978$, no SI value fixed here | §18.2.7 |
| $a$ (this chapter's usage) | The physical (dimensionful) BCC lattice cell size, distinct from Chapter 2's dimensionless $a=2/\sqrt3$ in lattice-native units (R2.10) — see §18.1 note 3 | §18.2.1 onward |
| $\eta_\text{Weyl}$ | The per-Weyl-field Seeley–DeWitt heat-kernel coefficient, $=1/12$ exactly | §18.2.6 |
| $g_*$ | The count of gravitating Weyl polarizations sourcing the induced $1/G$; $=48=16\times3$ (F38 content $\times$ F75 generation count) | §18.2.7 |
| $T^{00}[\psi]$ | The fermion energy density (not bare probability $\lvert\Psi\rvert^2$) that sources $\ln K$ in the weak-field reduction | §18.2.9 |
| $H_{\mu\nu}$ | The Lanczos–Lovelock tensor, identically zero in the model's derived $d=4$ (Lanczos–Bach identity), nonzero in $d=5$ | §18.2.12 |
| $\Pi(\mathbf q)=\Pi_0-\Pi_2q^2+\Pi_4q^4-\dots$ | The scalar-channel vacuum polarization whose successive coefficients are the induced cosmological-constant, Einstein–Hilbert, and curvature-squared terms | §18.2.2, §18.2.13 |

---

*This chapter logs one new gap, [G-8] (§18.6): F79's $g_*=48$ depends on Chapter 15's F75, an
undeclared cross-chapter dependency in `00-plan.md`'s dependency table. No finding, claim card,
module, or test record was created or modified in the writing of this chapter.*
