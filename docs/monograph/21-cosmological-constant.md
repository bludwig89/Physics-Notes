# Chapter 21 — The Cosmological Constant

*Chapter 21 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md`,
`findings/F190-horizon-entropy-lattice-microstates.md`,
`findings/F192-vacuum-energy-full-tensor.md`,
`findings/F193-ontic-vacuum-gravitates-as-zero.md`,
`findings/F196-dilution-exponent-derived.md`,
`findings/F241-omega-lambda-o1-residual-anthropic.md`,
`findings/F332-cc-dynamics-two-channels-excluded.md`,
`findings/F355-horizon-entanglement-vs-2pi-root3.md`,
`findings/F367-cc-sequestering.md`, and
`findings/F368-cc-sequestering-consistency.md`
(the ten findings `00-plan.md` §2 assigns to this chapter, all read in full), read against
`docs/theory/supersessions.yaml` (grepped for all ten finding numbers: none of the ten appears in
any `superseded:`/`reclassified:` list — this chapter's exclusions are claims-layer adjudications,
not `supersessions.yaml` records), and `claims-index.md` (**CL021** — the headline non-claim,
`not_claimed`, read in full; **CL275** — the uniform-reweighting no-go, `live`, read in full; **CL303**
— sequestering, `contingent`, read in full; **CL261** — the cell-entropy-is-not-a-state-count no-go,
`live`). Notation and results are those of Chapters 1, 18 and 20 — $c_\text{lat}$, $G$,
$K=e^{2GM/rc^2}$, $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, $\rho_\text{crit}$, $\Omega_\Lambda$, $H_0$,
$R_H$ — extended, never redefined.

## 21.0 What this chapter establishes, up front

**This chapter does not resolve the cosmological-constant problem.** Per `claims-index.md`'s CL021
(`status: not_claimed`, read in full, this chapter's central framing card): the model does not
derive $\Lambda$, and no result below should be cited as showing otherwise. What the ten assigned
findings *do* achieve, precisely stated: (1) F164 turns the textbook "120 orders of magnitude"
slogan into a definite, finite, cutoff-free number computed from this model's own lattice —
$\log_{10}(\rho_\text{vac}/\rho_\Lambda)=120.8$, with the wrong sign as well as the wrong
magnitude; (2) one candidate resolution (F193 Part A, "the bare vacuum energy is exactly zero
because gravity couples to the beable, not the template, energy") is examined, found attractive,
and then **excluded** by a later finding (F332, invoking CL275) for a precise, stated reason; (3)
the *surviving* candidate (F193 Part B's holographic capacity ceiling) is sharpened by F196 into a
genuine derivation of one structural number — the dilution exponent $p=2$ — reducing the 120-order
problem to a single $O(1)$ residual; (4) that residual, $\Omega_\Lambda\approx0.685$, is then shown
by F241 to be **not** derivable from the same sector, and is classified, at the level of a
theorem-with-caveats, as the ordinary cosmological "coincidence problem" in this model's own units;
(5) F332 additionally closes two concrete dynamical mechanisms that might have driven the bare sum
down to the ceiling, both in the negative; (6) F367/F368 explore a genuinely non-local
(Kaloper–Padilla sequestering) mechanism of the right *type* to evade the no-go that dooms (5)'s two
channels, find it mathematically compelling on its own narrow claim, and explicitly do not adopt it;
(7) F190/F355, read together, show that the model's *own* two routes to the horizon entropy needed
to make any of this precise — a heat-kernel mode count (F79, Chapter 18) and a direct
vacuum-entanglement computation (F355) — currently disagree with each other by a bracketed factor,
an unresolved internal tension this chapter inherits from Chapter 20's own forward flag and does not
close. The chapter's one clean positive result is the dilution exponent $p=2$ (F196); everything
else is either a sign-correctness check, an honestly-disclosed non-closure, or a closed-off wrong
turn.

## 21.1 Inputs

**Postulates used.** **P1–P4** (discreteness, locality, unitarity) underlie every Brillouin-zone
integral below exactly as in Chapters 6 and 18; nothing new is invoked. **P6/P7** enter only through
inherited results (the fermionic field content that sets $g_*$, and the elegant-design preference
that made F164's candidate (i) — later F193 Part A — the *initially* favoured route, per F164's own
language "elegant-design preferred," before it was excluded; Chapter 1's Gap [G-1] — no independent
argument that elegance tracks truth — is directly relevant to this chapter's own history of
preferring, then having to retract, an elegant-looking answer).

**Prior results used, precisely.** **R18.7–R18.9** (F79's structural
$G=a^2c^3/(8\pi\sqrt3\,\hbar)$, $g_*=48$, $a/\ell_P=6.5978$) is the single most load-bearing prior
result in this chapter: F164's bare vacuum density, F193's beable argument, F196's dilution
exponent, and F355's entropy-coefficient comparison all use the *same* structural $G$ and the *same*
lattice cell $a$. **R18.13** (the full-tensor induced Einstein equation $G_{\mu\nu}=(8\pi
G/c^4)T_{\mu\nu}$, canonical per F178) is what F192 tests the vacuum equation of state against.
**R20.x** (Chapter 20's cosmology: $\dot G/G\equiv0$ on the rigid substrate, F182/F188's flat
$\Lambda$CDM Friedmann pair as the model's adopted cosmological dynamics, and F360's horizon-Clausius
derivation of that same Friedmann pair) is the cosmological setting F192/F196/F241/F332/F367/F368 all
work inside. **Chapter 19's F183** (the Schwarzschild mass–radius law under the full-tensor source)
is F196's Route 1 input.

**Free inputs consumed — this chapter's central honesty point.** $\Omega_\Lambda\approx0.6847$
(Planck 2018) is **not derived anywhere in this chapter's assigned findings**, and F241 shows,
rather than merely asserts, that it cannot be derived from the same sector that supplies the
dilution exponent (§21.3.5 below). It is consumed as an external measured input throughout — most
visibly in F241's own residual, F332's untouched endpoint, and F367/F368's numerical toy comparison.
$H_0\approx67$–$67.4$ km/s/Mpc and $\Omega_m\approx0.3153$ (Planck 2018) are likewise external
inputs, used only for numerical evaluation, never derived. The bare $g_*=2$ (minimal two-branch
count) used for F164's absolute number is a simplification flagged by F164 itself as not affecting
the $10^{121}$-order conclusion; F355 later shows that even the "correct" $g_*=48$ count is itself
contested at the lattice level (§21.3.7).

## 21.2 The derivation

### 21.2.1 F164 — the problem, made quantitative and sharpened rather than softened

F164 (2026-06-29) evaluates the $\Lambda^4$ Sakharov sector F59 (Chapter 18) had identified but left
unevaluated: $\rho_\text{vac}=g_*\int_\text{BZ}\frac{d^3k}{(2\pi)^3}\frac{1}{2}\frac{\hbar\omega(k)}
{\tau}=g_*\sqrt3\,I_\text{CC}\,\hbar c/a^4$, with the dimensionless BCC integral
$I_\text{CC}=4.0810486$ — an **exact algebraic fact** in one respect, $\langle\omega\rangle_\text{BZ}
=\pi/2$ identically (the $\mathbf q\to\mathbf q+\pi\hat x$ pairing $\omega+\omega'=\pi$), confirmed
against `test-results/F164_cosmological_constant.json` (`I_CC_dimensionless: 4.081048569526987`,
`mean_omega_exact_pi_over_2: 1.5707963267948966`). At the F107 canonical cell $a=\sqrt{8\pi}\,3^{1/4}
\ell_P=1.066\times10^{-34}$ m, this gives $\rho_\text{vac}\approx3.46\times10^{111}$ J/m$^3$ against
observed $\rho_\Lambda\approx6.0\times10^{-10}$ J/m$^3$ — ratio $5.8\times10^{120}$,
$\log_{10}=120.76$ (`test-results/F164_cosmological_constant.json` records
`a_over_ellP: 6.597816664747605`, matching R18.9 to the digits shown).

Two features make this the model's *own* statement of the problem rather than a borrowed slogan.
**First**, the cutoff is the physical Brillouin-zone edge, not a chosen regulator: $\rho_\text{vac}$
is a definite prediction of the bare theory, with nothing to renormalise away — the lattice
*sharpens* the standard problem rather than giving it more places to hide. **Second**, the sign is
also wrong: the model has no fundamental bosons (every gauge boson is composite, F67–F69), so the
only zero-point contribution is the all-fermion tower $-\tfrac12\sum\hbar\omega$ — negative, opposite
the observed $+\rho_\Lambda$ — and there is no independent bosonic tower available for a
SUSY-style cancellation. F164 names three candidate resolutions (the CA-native ontic-vacuum route,
dielectric sequestering, and marginal-binding of composite bosons) and derives none of them; it
explicitly states the leading candidate — "the CA-native trivial vacuum" — is "a position, not a
calculation" at this point in the chain.

$$\boxed{\;\rho_\text{vac}/\rho_\Lambda=5.8\times10^{120}\ (\log_{10}=120.76),\text{ cutoff-free, exact BZ integral }I_\text{CC}=4.081049;\ \text{bare sign is negative (all-fermion), opposite observation; no SUSY-style cancellation available}\;}\tag{R21.1}$$

(F164, Parts A–C; no independent claim card — its content is carried forward by CL021/CL275.)

### 21.2.2 F192 — the sign is correct under the full-tensor law; the magnitude is untouched

F192 (2026-06-30) re-examines the vacuum sector under Chapter 18's adopted full-tensor law
(R18.13) rather than the demoted energy-only reduction. For a vacuum equation of state $w=-1$, the
combination that sources the acceleration equation is $\rho+3p=-2\rho<0$ — the full-tensor law makes
a positive vacuum energy density **accelerate** the expansion, the correct sign for dark energy, a
sign the demoted energy-only law (sourced by $\rho$ alone) would have gotten wrong. This is a real,
if narrow, gain from the F178 adoption (Chapter 18): three checks confirm it (V1), reproduce F164's
120.76-order overshoot as a sanity check (V2), and confirm that none of F164's three candidate
cancellations is yet derived (V3). F192's own text is explicit that this "quantifies and reframes; it
does not solve" — the sign is fixed, the magnitude is exactly where F164 left it.

$$\boxed{\;\text{full-tensor vacuum }w=-1\Rightarrow\rho+3p=-2\rho\text{: correct accelerating sign (exact); the }120.76\text{-order magnitude problem (R21.1) is untouched}\;}\tag{R21.2}$$

(F192, checks V1–V3, 3/3 PASS; no independent claim card — subsumed into CL021.)

### 21.2.3 F193 — Part A (excluded) and Part B (the surviving route), read precisely

F193 (2026-06-30) is the chapter's most important single finding to get exactly right, because it
contains **two logically separate results of opposite eventual fate**, and later findings (F332,
citing the headline no-go card CL275) settle which is which. Both must be stated with their correct,
current status — not as F193 itself first presented them, but as the finding chain resolved them.

**Part A — turning candidate (i) into a derivation, and why it is excluded.** F193's Part A argues
that the CA's ontic vacuum (the empty lattice, $\psi\equiv0$) has zero energy identically ($H\,0=0$,
a structural consequence of linearity), that the local field-energy density is a *beable* — a
diagonal, non-negative functional of the **actual** amplitudes with no additive $c$-number per mode
— and that the F64/F178 gravity sector is sourced by exactly this beable quantity, not by the
template expectation $\langle T^{00}\rangle$ that includes the $+\tfrac12\hbar\omega$-per-mode
zero-point offset. On this reading the bare cosmological constant is $0$ in the ontology, removing
both F164's magnitude and its wrong sign at a stroke. **This is excluded.** F332 (2026-08-28, §1,
citing the headline no-go card CL275) states the exclusion in CL275's own words: the "delete the
$\tfrac12$-per-mode $c$-number" step is **uniform** in the heat-kernel expansion — F59 Part C
(Chapter 18) builds $1/(16\pi G)$ out of the *same* $\tfrac12$-per-mode sum that F164 uses for
$\rho_\text{vac}$ (the $a_1$ and $a_0$ coefficients of one heat-kernel expansion over one set of
modes), so deleting the offset uniformly deletes F79's successful structural $G$ along with the CC.
CL275's own $2\times2$ solve makes this quantitative: requiring the model to reproduce both the
measured $G$ and the measured $\rho_\Lambda$ under a *uniform* reweighting $\lambda$ of the zero-point
sum has the unique solution $a^\star=2.559\times10^{26}$ m (a lattice cell $0.58\times$ the comoving
radius of the observable universe) and $\lambda^\star=5.76\times10^{120}$ — absurd on both counts.
Part A's beable-source argument, however physically motivated, is exactly this uniform class, and
CL275 excludes it. **`claims-index.md`'s CL021 records this explicitly**: "F193's Part A route to a
zero bare CC... is a uniform deletion... What survives... is the capacity ceiling."

**Part B — the surviving route, correctly understood as narrower than Part A promised.** F193's
Part B recasts the observed $\rho_\Lambda$ not as a $121$-order cancellation residual but as the
back-reaction of the actual non-vacuum content of the universe, capped by a Cohen–Kaplan–Nelson-style
holographic bound: a region cannot hold more gravitating energy than collapses it into a black hole
of its own size, capping the density at the causal-horizon scale $R_H=c/H_0$,
$\rho_\text{grav}\sim\rho_\text{vac}(a/R_H)^p$. With $p=2$ (imported from Cohen–Kaplan–Nelson, *not*
yet derived from the lattice) this reproduces F164's entire $120.76$-decade overshoot to within a
factor $3.4$ ($\Delta\log_{10}=0.54$) — but F193's own text is explicit that the exponent $p=2$ is
"posited/imported," "the named obstruction," not yet a derivation. **This part is not excluded**:
CL275's own text states plainly, "the tree carries a fourth candidate that F164 §C did not list...
F193 Part B with F196's derived $p=2$... is *not* excluded" — it is order-selective *by construction*
because the capacity bound itself contains $G$, rather than uniformly reweighting the zero-point sum
that produces $G$.

$$\boxed{\;\textbf{F193 Part A (bare CC}=0\textbf{ via beable sourcing) is EXCLUDED}\text{ (CL275: the deletion is uniform in the heat-kernel order and takes }1/16\pi G\text{ with it, per F59 Part C);}\ \textbf{Part B (holographic capacity ceiling) is the surviving, live route}\text{, reproducing }120.66\text{ of }120.76\text{ decades with its exponent }p\text{ imported, not derived}\;}\tag{R21.3}$$

(F193, 4/4 checks PASS as originally reported; Part A's status is superseded in substance, though not
in `supersessions.yaml`, by the CL275 no-go and its adjudication in CL021's 2026-08-18 amendment. No
independent claim card for F193 itself — its two parts are now carried, respectively, as an excluded
leg of CL275 and as unexcluded evidence for CL021/CL212.)

### 21.2.4 F196 — the dilution exponent $p=2$, derived: the chapter's one genuine positive result

F196 (2026-06-30) closes F193 Part B's named obstruction by deriving $p=2$ from the model's own
structure, by two independent routes that converge on the identical closed form.

**Route 1 (bulk):** the model's own Schwarzschild law under the full-tensor source (F183, Chapter
19) gives the maximal mass a region of radius $L$ can hold before it lies inside its own horizon,
$M_\text{max}(L)=Lc^2/2G$ (linear in $L$), so the maximal gravitating density such a region can
support is $\rho_\text{grav}(L)=M_\text{max}(L)c^2/V(L)=3c^4/(8\pi GL^2)\propto L^{-2}$ —
structurally $p=3-1=2$: the "$3$" is the dimensionality of space (volume $\propto L^3$), the "$1$" is
the model's own mass–radius law, and neither is imported. The slope is exact to the finite-difference
floor ($\mathrm d\ln\rho/\mathrm d\ln L=-2.0$; `test-results/F196_dilution_exponent_test.json`
confirms `E1_exponent_is_2: p=2.0, slope=-2.0`).

**Route 2 (surface):** using only F190's per-cell horizon entropy ($a^2/4\ell_P^2=2\pi\sqrt3$ nats,
§21.2.6 below) and Gibbons–Hawking de Sitter horizon thermodynamics, the cosmic horizon carries
$N_\text{dof}=A/4\ell_P^2\propto R_H^2$ degrees of freedom each at temperature $\propto1/R_H$, giving
$\rho_\text{holo}=N_\text{dof}\cdot(\hbar c/2\pi R_H)/V(R_H)=3c^4/(8\pi GR_H^2)$ — the *identical*
formula, agreeing with Route 1 to $3\times10^{-8}$ (the identity $\hbar c/\ell_P^2=c^4/G$).

Both routes evaluate, at $L=R_H$, to exactly $\rho_\text{crit}=3H_0^2c^2/(8\pi G)$ — the critical
density. A competing statistical hypothesis (mode-counting fluctuation, $\Delta E\sim
E_\text{vac}/\sqrt N$, giving $p=3/2$) is excluded by more than 30 decades, confirming the effect is
gravitational/holographic, not a fluctuation statement. With $p=2$ fixed, F164's once-unknown
121-order problem collapses to a single order-unity residual: the ratio of the saturation value
($\rho_\text{crit}$) to the observed $\rho_\Lambda=\Omega_\Lambda\rho_\text{crit}$, i.e. the
coincidence factor $\Omega_\Lambda\approx0.685$ itself, $0.10$ dex from unity.

$$\boxed{\;p=2\text{ derived exactly, two independent model-native routes (F183 Schwarzschild bulk capacity; F190 area-entropy}+\text{Gibbons--Hawking surface count) agreeing to }3\times10^{-8}\text{; both saturate at }\rho_\text{crit};\ \sqrt N\text{ statistical route (}p=3/2\text{) excluded by }30.6\text{ decades; residual collapses from }121\text{ orders to the single factor }\Omega_\Lambda\;}\tag{R21.4}$$

(F196, 5/5 checks PASS; no independent claim card — the derivation is carried directly by CL021 and
CL275.)

### 21.2.5 F241 — the last $O(1)$ factor is honestly not derivable from this sector

F241 (2026-07-03) asks whether the *same* holographic/black-hole sector that supplied $p=2$ can also
supply $\Omega_\Lambda\approx0.6847$, and answers, at the level of a theorem-with-caveats, no —
delivering a genuinely rigorous negative result rather than an unexamined shrug. Six checks
(`test-results/F241_omega_lambda_residual.json`, 6/6 PASS) establish, in order:

- **The ceiling theorem.** F183's capacity and F190's area count are both *saturation* statements —
  the *most* energy a horizon-sized region can hold. Read as a bound they give $\rho_\Lambda\le
  \rho_\text{crit}$, i.e. $\Omega_\Lambda\le1$ — an inequality with no second scale to fix *how far
  below* saturation the present universe sits. The exponent $p$ is the *slope*; the sub-unity offset
  is a boundary condition the same one-parameter sector cannot also supply.
- **The event-horizon route is circular.** The most principled attempt to pin the offset — holographic
  dark energy with the IR cutoff set to the *future* event horizon (Li 2004) — is shown to be a
  self-consistency identity satisfied for *any* $\Omega_\Lambda$, not a prediction, and its true
  asymptotic fixed point is $\Omega=1$ (the ceiling again), reached only in the infinite future; the
  same route's predicted $w_0=-0.885$ is also in tension with the model's own $w=-1$ (F192).
- **The residual is identically the coincidence problem.** Flat geometry gives
  $\Omega_\Lambda=1-\Omega_m$ exactly, so deriving $0.685$ is *identically* deriving the present
  matter fraction $\Omega_m=0.3153$ — a quantity that requires the dark-sector abundance, which is
  itself open/no-go territory in this model (F197–F199, outside this chapter). Equivalently, the
  present epoch sits at $\log_{10}(a/a_\text{eq})\approx0.14$ past matter–$\Lambda$ equality — a
  "why observed now" statement, not a dynamical one.
- **The near-hits are numerology.** Several clean constants ($2/3$, $\ln2$, $e/4$, $1/\sqrt2$) sit
  within $0.02$ dex of $0.6847$, but a density argument shows this window is wide enough ($\sim9\%$)
  that $O(5)$ simple constants are expected to land there by chance, and — decisively — none of them
  is actually produced by any step of the F190/F183 algebra.

$$\boxed{\;\Omega_\Lambda\approx0.685\text{ is }\textbf{not}\text{ derivable from the F190/F183 holographic sector: that sector fixes only the ceiling }\Omega\le1\text{; the residual is identically }1-\Omega_m\text{ (the standard coincidence problem), blocked by this model's own open dark-sector abundance; near-hits are numerology by an explicit density count}\;}\tag{R21.5}$$

(F241, checks C1–C6, 6/6 PASS; carried by CL212 and cited throughout CL021/CL275/CL303.)

### 21.2.6 F190/F355 — the horizon-cell entropy machinery, and its own internal tension

F190 (2026-06-30) is the source of the $2\pi\sqrt3$-nats-per-cell figure F196's Route 2 uses. Tiling
a horizon of area $A$ with $N=A/a^2$ lattice cells and demanding $S=A/4\ell_P^2$ (Bekenstein–Hawking)
fixes the required per-cell entropy in closed form: $s_\text{cell}=a^2/(4\ell_P^2)=8\pi\sqrt3/4=
2\pi\sqrt3\approx10.883$ nats, matched to $10^{-9}$. F190's own status line is explicit that this is
a **consistency relation, not a derivation**: "the *derivation* of $2\pi\sqrt3$ nats/cell from
lattice degrees of freedom is open" — it converts a debt into a sharp, falsifiable target, nothing
more, and it is marked `speculative` in `findings-index.md`.

**Two later findings bear on whether that target can be hit, and both report negative or unresolved
results — a pattern this chapter states plainly rather than reads as corroboration.** `claims-index.md`'s
CL261 (`status: live`, `kind: no_go`) shows the naive microstate-counting reading is
arithmetically closed off with no model input at all: $2\pi\sqrt3$ is irrational, so it cannot equal
$\ln W$ for an integer $W$ or $n\ln2$ for an integer $n$ — $e^{2\pi\sqrt3}=53252.295$ sits $0.295$
from the nearest integer, and $2\pi\sqrt3/\ln2=15.7006$ sits $0.299$ from one. The required object
must be an entanglement entropy (continuous spectrum, no integrality constraint), not a state count.

F355 (2026-09-03) is exactly that computation, and it is where **the tension Chapter 20 flagged
forward to this chapter** becomes precise. F355 computes the vacuum entanglement entropy of a region
of the BCC lattice directly, using the exact one-particle correlation matrix built from the F26
rotation-rule spin projector (Peschel's formula for a Gaussian/free-fermion vacuum) — a genuinely
independent, from-first-principles route to a horizon-adjacent quantity, checked 14/14 (two declared
controls verified red). F355's central finding is **not**, on close reading, a test of F190 or of
Bekenstein–Hawking directly: because F79's $G$ is itself *induced* (Sakharov, no bare kinetic term,
Chapter 18), the comparison is between **two of the model's own computations of the same induced
$1/G$** — F79's heat-kernel mode sum ($\eta g_*$) and F355's vacuum-entanglement coefficient
($c_\text{walk}$) — which induced gravity says must be the same object. They disagree. The
required-versus-computed ratio is independent of the field count $g_*$ (both sides scale with it
identically, verified to $4.4\times10^{-16}$), so the mismatch is not a matter of "the wrong number of
fields." What it *is* a matter of is an **undecided lattice question**, named already by Chapter 2/18's
own F278: the BCC quantum walk carries four gapless (zero-mode) points per zone, and whether the two
at $\omega=\pi$ (the walk's own momentum-doubler pair) should be counted once, twice, or discounted
entirely is, in F278's own words, "not decided here." Depending on that undecided convention, F355's
computed-to-required ratio runs from $0.79$ to $3.18$ — an $8\times$ bracket that contains no counting
giving exact agreement (the closest, discounting all doubler pairs, still misses by $21\%$).

**This is the live F79/F355 entropy-coefficient tension Chapter 20 flagged forward (its own §20.2.19,
R20.19: "K1 stays QUANT, entropy coefficient hostage to the live F79/F355 tension").** This chapter
does not close it — no source read for this chapter resolves the doubler-counting question — and,
following Chapter 20's own precedent for a forward-flagged tension it could not itself resolve
(Gap [G-12]), states plainly why no gap entry is added here: F355 *itself* discloses this tension in
full, at the length its own §7 ("Scope limits — the load-bearing section") and §8 ("Next steps")
devote to it, including the exact bracket, the exact mechanism (the doubler question), and the exact
next experiment that would decide it (rebuilding the walk on an explicit two-sublattice site set and
measuring $\langle\cot\omega\rangle$). `docs/monograph/GAPS.md`'s own logging policy reserves gap
entries for holes a *source* leaves undisclosed; this is not that — it is an honestly-disclosed open
finding this chapter carries forward rather than resolves, exactly as Chapter 20 asked it to.

$$\boxed{\;\text{F190: per-cell entropy target }2\pi\sqrt3\text{ nats fixed to }10^{-9}\text{, but the derivation of that number from lattice content is }\textbf{open}\text{ (F190's own words); CL261: no integer microstate count can equal }2\pi\sqrt3\text{ (exact arithmetic no-go); F355: the model's own entanglement computation of the same induced }1/G\text{ disagrees with F79's heat-kernel computation by a bracketed factor }[0.79,3.18]\text{, hostage to an undecided lattice doubler-counting convention (F278) -- unresolved, inherited from Ch.20, not closed here}\;}\tag{R21.6}$$

(F190, checks E1–E3, 3/3 PASS, `speculative`; F355, checks E9-1–E9-14, 14/14 PASS at `scale: full`,
two controls verified red; CL261, `live`, `no_go`, `falsifier: none`; claim card `CL296` for F355.)

### 21.2.7 F332 — two dynamical channels tested and closed, both negative

F332 (2026-08-28) takes up Amendment 4's own named next step — "show that the F164 zero-point sum
is made to respect the F183/F190 capacity ceiling, or show that it is not" — and runs two concrete,
computed checks. Both close **negative**.

**Channel (ii) — $AB\equiv1$ dielectric sequestering (F164's own second candidate).** Closed for two
independent reasons. First, the static sourcing law $\nabla^2u=-S$ (F106, Chapter 18) is *exactly*
Fredholm-blind to a homogeneous source on a periodic domain: the $k=0$ Fourier mode has zero freedom,
so a constant vacuum-energy density has literally nowhere in the equation to go — checked by direct
FFT (`DC residual/S₀ = 1.000000` for a uniform source, `0.0` for the same source with its mean
subtracted, an exact control). Second, and independently, F178's own already-adopted decision
(Chapter 18) restricts $AB\equiv1$ to vacuum regions ($T_{\mu\nu}=0$); a homogeneous cosmological
vacuum energy is, by definition, never that case — it is always the "interior" case F178 hands to
the full two-function tensor treatment. Channel (ii) needs a representation that is definitionally
not in play for a homogeneous source.

**A literal block-spin (F130) recomputation of the two Sakharov moments.** Applying F130's proven
blocking transform to F59/F164's $I_g$ and $I_\text{cc}$ integrals gives clean power laws
($a_0\propto b^{-4}$, $1/G\propto b^{-1}$, exponents machine-exact to $<1.1\times10^{-5}$) — but
$G$ *grows* with the block size, and closing F319's required $120.76$-decade suppression on $a_0$
this way needs $\Delta G/G=3.1\times10^{30}$, **$35.15$ orders of magnitude beyond CODATA's
$2.2\times10^{-5}$ budget on $G$** — worse than the already-excluded uniform-reweighting channel,
because the two moments move in *opposite* directions as the block size grows rather than merely at
different rates.

F332 also makes one clarifying, non-suppressing observation: F196's ceiling formula is not an
independent import at all — it is algebraically identical (residual $0.0$) to the model's own adopted
Friedmann-I constraint (F182) evaluated at $H=c/R_H$. This sharpens what the surviving route actually
*is* (the model's own cosmological dynamical law, read as a capacity), but supplies no new dynamics.
Both tested channels are **local** constructions in the technical sense of Weinberg's 1989 no-go
theorem (any local, Lorentz-invariant adjustment mechanism cannot relax a large bare CC without
reintroducing the same fine-tuning); their failure is the theorem's expected outcome, and it points
directly at the one channel *type* — non-local, tied to a global quantity like $R_H$ — that could in
principle evade it.

$$\boxed{\;\textbf{Two dynamical channels closed, both negative}\text{: (a) }AB\equiv1\text{ sequestering has no hook into a homogeneous source at all (Fredholm-blind DC mode, and F178 restricts it to }T_{\mu\nu}=0\text{); (b) a literal F130 block-spin recount fails by }35.15\text{ decades beyond the CODATA }G\text{ budget, with the two moments moving in opposite directions. F196's ceiling }=\text{ the model's own Friedmann-I law, exactly. The surviving F193§B/F196/F241 route is left untouched and still undynamicised}\;}\tag{R21.7}$$

(F332, checks K1–K4, 5/5 PASS, 2/2 controls verified red; no independent claim card, per F332's own
disclosure — an internal-mechanism check, not itself an extension/contradiction of established
physics.)

### 21.2.8 F367/F368 — sequestering: a compelling identity, explored honestly, not adopted

F332 named, and explicitly declined to build, the one surviving channel *type*: a genuinely
non-local/global mechanism. F367 (2026-09-04) builds it, against this model's own numbers, using
Kaloper–Padilla vacuum-energy sequestering (a global, non-propagating Lagrange-multiplier sector
added to the gravitational action, sourcing $G_{\mu\nu}$ from the matter trace minus its
*spacetime-averaged* value rather than its local value).

**The core result, proven rather than merely cited.** If the matter trace carries an arbitrary
spacetime-constant piece $C$ (exactly F164's $\rho_\text{vac}$, by construction — it is built from
the fixed lattice cell $a$ alone, with nothing in the model's adopted cosmology making $a$ evolve),
then $C$ cancels *exactly* under the sequestering subtraction, for **any** finite total spacetime
4-volume, any power-law expansion history, and any measure power — a symbolic (sympy) identity, not
a fitted number, independently spot-checked numerically at $C/\rho_{m0}\in\{0,1,10^{60},10^{120}\}$
with bit-identical output. This gives *formally unbounded* selectivity between a constant source and
a time-varying one, trivially exceeding F319's own required selectivity of $\ge1.27\times10^{116}$
(Chapter 18/CL275) — qualitatively different from F332's two closed channels, neither of which
offered *any* selectivity of the right kind. F367 also shows this is not blocked by the model's own
Sakharov origin for $G$ and $\rho_\text{vac}$ sharing "the same modes, same measure, same factor of
$\tfrac12$" (the fact CL275 used to exclude F193 Part A): the model's own IR effective-action operator
ledger (F319 §7, Chapter 18) already treats the cosmological-constant operator and the
Einstein–Hilbert operator as two *separable* Wilson coefficients regardless of their shared
microscopic origin, and sequestering acts only on the former. A surviving matter-history residual has
an exact closed form ($3n\,\rho_m(t_0)$ for $a(t)\sim t^n$ domination), landing $0.036$ dex from the
observed value at matter domination ($n=2/3$) — flagged explicitly, using F241's own numerology-caution
standard, as a crude single-fluid toy, not a tightened derivation of $\Omega_\Lambda$.

**F368 (2026-09-05) checks the mechanism's own falsifier and finds two new, undischarged costs.**
Run against Kaloper–Padilla's actual base action (not F367's abridged local consequence): the
vacuum-region reduction gives ordinary GR plus a genuinely constant $\Lambda_\text{eff}$ term
(Schwarzschild–de Sitter, PPN-negligible) — falsifier 4's three named legs (PPN, F178's vacuum-scope
restriction, induced-$G$) are checked directly and do **not** fire, so CL303 is not withdrawn. But
the *base* mechanism (not only its "why now" extension) independently requires **spatial closure**
($k>0$, from the mechanism's own global integral constraint — verified here by an independent finite-
spacetime-4-volume argument: only a closed recollapsing history gives finite $V_4$, while eternal de
Sitter and ordinary flat/open matter-only expansion both diverge) and **non-eternal ("transient")
dark energy** (eternal $w=-1$ gives infinite $V_4$, "incompatible with the sequestering proposal" per
the cited literature). Neither is excluded by current data — Planck's own CMB-alone curvature
preference is live but disputed, and DESI DR2's $w_0>-1,w_a<0$ preference is directionally, not
quantitatively, aligned with the transience requirement — but both are genuine, previously unnamed
adoption costs.

**Not adopted, and stated as such.** F367/F368's own honest-scope sections are explicit: adopting
sequestering would graft new global, non-propagating fields onto the CLAUDE.md decision-4 action —
a decision of the scope of Chapter 18's own eight prior gravity-sector decisions, not something a
single finding (or this documentation chapter) is positioned to make. CL303's `status` is
`contingent`, not `live` or `adopted`, and stays that way through both findings.

$$\boxed{\;\text{Sequestering's constant-cancellation identity is }\textbf{exact}\text{ (sympy-verified, unbounded selectivity, dwarfing the required }1.27\times10^{116}\text{); it is well-matched to F164's specific residual (a genuine spacetime constant) and not blocked by the model's shared Sakharov origin for }G/\rho_\text{vac}\text{ (F319's own separable operator ledger); falsifier 4 checked and }\textbf{not met}\text{ (PPN/vacuum-scope/induced-}G\text{ unaffected); but the base mechanism newly requires spatial closure and transient dark energy (neither excluded, neither confirmed); }\textbf{not adopted}\text{, }\Omega_\Lambda\text{ untouched}\;}\tag{R21.8}$$

(F367, checks 3/3 PASS, 2/2 controls verified red, reviewed CONFIRMED-NARROWER; F368, checks 5/5
PASS, 3/3 controls verified red, reviewed CONFIRMED-NARROWER; both carried by CL303, `contingent`.)

## 21.3 Results table

| # | Statement | Class | Exactness | Test record |
|---|---|---|---|---|
| R21.1 | Bare $\rho_\text{vac}$ overshoots $\rho_\Lambda$ by $\log_{10}=120.76$, cutoff-free; sign wrong (all-fermion, negative) | genuine derivation (problem statement) | exact BZ integral ($I_\text{CC}=4.081049$); computed overshoot | F164; `test-results/F164_cosmological_constant.json` |
| R21.2 | Full-tensor vacuum $w=-1\Rightarrow\rho+3p=-2\rho$: correct accelerating sign; magnitude untouched | genuine derivation (sign only) | exact | F192; `test-results/F192_vacuum_energy.json` (3/3) |
| R21.3 | **F193 Part A EXCLUDED** (uniform reweighting, CL275); **Part B is the surviving route** (order-selective by construction, imported exponent) | exclusion (Part A) / disclosed non-closure (Part B) | Part A: exact no-go (CL275 $2\times2$ solve); Part B: computed to $0.54$ dex | F193 (4/4); CL275 |
| R21.4 | Dilution exponent $p=2$ **derived** from two independent model-native routes (F183 bulk, F190+GH surface), agreeing to $3\times10^{-8}$; $\sqrt N$ route excluded by 30.6 dex | **genuine derivation — the chapter's positive result** | exact (slope $-2.0$); statistical alternative excluded $30.6$ dex | F196; `test-results/F196_dilution_exponent_test.json` (5/5) |
| R21.5 | $\Omega_\Lambda\approx0.685$ **not derivable** from the F190/F183 sector — fixes only ceiling $\Omega\le1$; residual $\equiv1-\Omega_m$, blocked by open dark-sector abundance; near-hits are numerology | honestly-disclosed non-closure (rigorous negative) | exact (C1,C2,C4,C5) / machine (C3) / quantitative (C6) | F241; `test-results/F241_omega_lambda_residual.json` (6/6) |
| R21.6 | F190's per-cell target $2\pi\sqrt3$ nats fixed exactly, but its lattice derivation is open; CL261: no integer microstate count can equal it; F355: model's own entanglement route disagrees with F79's heat-kernel route by bracketed $[0.79,3.18]$, hostage to an undecided doubler convention | disclosed non-closure / internal no-go (CL261) / disclosed internal tension (F79 vs. F355) | F190: $10^{-9}$; CL261: exact arithmetic; F355: `quantitative`/`bracketed` | F190 (3/3, `speculative`); F355 (14/14, gate); CL261 (`live`, `no_go`) |
| R21.7 | Two dynamical channels **closed, both negative**: $AB\equiv1$ sequestering has no hook (Fredholm-blind, F178-restricted); block-spin recount fails by 35.15 dex beyond the CODATA $G$ budget | no-go (double) | exact (K1, K2); machine (K3, exponents); quantitative (K4, 35.15 dex) | F332; `test-results/F332_cc_dynamics.json` (5/5, 2 controls red) |
| R21.8 | Kaloper–Padilla sequestering: exact unbounded-selectivity identity, well-matched to F164's residual, **not blocked** by shared Sakharov origin; falsifier 4 checked and not met; **new** base-mechanism costs (spatial closure, transient DE) named, neither excluded; **not adopted** | contingent exploration (positive on mechanism, negative on adoption) | exact (identity); quantitative (0.036 dex toy; costs vs. data) | F367 (3/3, 2 controls red); F368 (5/5, 3 controls red); CL303 (`contingent`) |

## 21.4 Comparison with measurement

**$\rho_\text{vac}/\rho_\Lambda$.** The bare model overshoots the Planck 2018 value of
$\rho_\Lambda\approx6.0\times10^{-10}$ J/m$^3$ by $5.8\times10^{120}$ — worse, in the sense of being a
sharper and more definite prediction with no regulator freedom to absorb it, than the generic
continuum "$10^{120}$" slogan. This is not a comparison this chapter passes; it is the comparison
this chapter's entire content exists to characterise honestly.

**$\Omega_\Lambda\approx0.685$.** F196 reduces the target to matching the critical density
$\rho_\text{crit}$ at $L=R_H$, landing $0.10$ dex ($26\%$) below the observed $\rho_\Lambda$ — the
model's holographic sector predicts $\Omega\le1$ (saturated only asymptotically), and the observed
$0.685$ sits inside that bound with no further prediction of *where*. **This chapter does not claim
to reproduce $\Omega_\Lambda\approx0.685$**; F241 shows explicitly, not by omission, why the same
sector cannot supply it. F367's sequestering toy lands at $0.036$ dex, closer numerically, but is
explicitly flagged (by F367's own text, applying F241's own numerology-caution standard) as a
single-fluid toy sensitive to modelling choices the finding does not claim to have made
correctly — it is not offered, and must not be read, as a tighter measurement of the same quantity.

**Sign of the equation of state.** F192's $w=-1\Rightarrow\rho+3p=-2\rho<0$ correctly reproduces the
observed accelerating sign; this is a genuine, if narrow, quantitative success under the full-tensor
law and is the one place in this chapter where a comparison with measurement is unambiguously passed.

**Horizon entropy coefficient.** F190's target $2\pi\sqrt3\approx10.883$ nats/cell is fixed to
$10^{-9}$ against Bekenstein–Hawking, but no independent measurement tests this value directly (it is
an internal consistency target, not a measured quantity) — the comparison that *is* available, F355's
entanglement computation against F79's heat-kernel prediction, currently disagrees by up to a
factor of $\sim3$ depending on an unresolved lattice convention.

## 21.5 What was excluded, and why

- **F193 Part A — the CA-native ontic vacuum gravitates as exactly zero.** Excluded by CL275
  (§21.2.3, R21.3): the beable-sourcing argument deletes the $\tfrac12$-per-mode zero-point offset
  uniformly across the heat-kernel expansion, which takes F79's successful structural $G$ down with
  it. This is a genuine exclusion of a specific, previously favoured mechanism, not a supersession of
  F193 as a whole — Part B survives.
- **F332's two dynamical channels** ($AB\equiv1$ sequestering as a literal homogeneous-source
  mechanism; a naive block-spin recomputation of the Sakharov moments) — both closed negative for
  computed, structural reasons (§21.2.7, R21.7): the first has no hook into a homogeneous source at
  all, and the second fails by 35 decades with the wrong relative sign of movement between $a_0$ and
  $a_1$. Both are examples of the *local* mechanisms Weinberg's 1989 no-go theorem forbids from
  working, and their failure is that theorem's expected outcome.
- **The event-horizon (future) holographic dark-energy route.** Excluded within F241 itself (§21.2.5,
  R21.5) as circular — a self-consistency identity satisfied for any $\Omega_\Lambda$, not a
  prediction — and as quantitatively disfavoured on its own $w_0$ prediction.
- **The parameter-free numerological near-hits for $\Omega_\Lambda$** ($2/3$, $\ln2$, $e/4$,
  $1/\sqrt2$). Shown by F241's density argument to carry no evidential weight and, decisively, to
  arise from no step of the actual F190/F183 algebra.
- **Kaloper–Padilla sequestering as an adopted mechanism.** Not excluded on its own mathematical
  merits (its core identity is exact and its falsifier 4 is checked and not met, §21.2.8, R21.8) but
  explicitly **not adopted**: it requires new global field content beyond the CLAUDE.md decision-4
  action, carries two additional, currently-undischarged costs (spatial closure, transient dark
  energy), and a decision of that scope is outside a single finding's (or this chapter's) remit.
  `docs/claims/CL303.md`'s `status: contingent` records this precisely.
- **Microstate counting for the horizon-cell entropy.** Excluded outright, and for a reason needing no
  model input, by CL261 (§21.2.6, R21.6): $2\pi\sqrt3$ is irrational and cannot equal $\ln W$ for an
  integer $W$. The required object is an entanglement entropy, not a state count — which is exactly
  what F355 goes on to compute, with the result described in §21.2.6/§21.6.

## 21.6 What is still open

This section is deliberately the chapter's longest, per CL021's own instruction that absence must not
be read as a prediction.

1. **The dilution exponent's own dynamics remain unfound.** F196 derives $p=2$ as a *structural*
   fact about the model's Schwarzschild law and area-entropy count, and F332 shows this is
   algebraically identical to the model's own Friedmann-I constraint — but no finding shows the bare
   zero-point sum is *dynamically driven* to respect this ceiling. F332's own honest scope states
   this plainly: "the F193§B/F196/F241 ceiling route is untouched, still a consistency requirement
   rather than a demonstrated dynamical outcome."
2. **The $\Omega_\Lambda\approx0.685$ residual is the chapter's largest, and best-characterised, open
   item.** F241 shows it is *identically* the present matter fraction $\Omega_m$, which this model
   does not currently derive — the dark-sector abundance (Chapters 22's F197–F199 line) is itself
   open/no-go territory. Absent that, or a first-principles temporal-selection/observer measure, the
   honest ledger entry (F241's own words) is: "the last $O(1)$ factor is the coincidence-problem
   residual, coincidental/anthropic given the present model." "Anthropic" here means specifically the
   Weinberg-1987/Martel–Shapiro–Weinberg-1998 "why observed now, on the shoulder of the
   matter–$\Lambda$ transition" selection argument, external to this model and not itself computed
   here (Martel–Shapiro–Weinberg's own median is $0.12$ dex high, "consistent within the anthropic
   spread but not a lattice derivation") — it is not a claim that no deeper dynamical principle could
   ever exist, and F241 is explicit about that scope limit.
3. **The F79/F355 horizon-entropy-coefficient tension is unresolved and unresolvable from this
   chapter's sources alone.** As detailed in §21.2.6/R21.6, the model's own two routes to the induced
   $1/G$ — a heat-kernel mode sum (F79) and a direct vacuum-entanglement computation (F355) —
   disagree by a factor bracketed $[0.79,3.18]$, contingent on an undecided lattice doubler-counting
   convention F278 explicitly left open. This is a live tension inherited from Chapter 20's own
   forward flag (its §20.2.19/R20.19), not created here, and F355's own §8 names the specific next
   experiment (an explicit two-sublattice BCC rebuild, measuring $\langle\cot\omega\rangle$) that
   would decide it. Chapter 22 (dark sector), if it touches horizon thermodynamics or any $g_*$-
   dependent entropy count, should be aware of this same unresolved bracket.
4. **Sequestering's adoption question is deliberately left open by its own findings.** F367/F368
   establish that the mechanism is mathematically well-matched to this model's specific residual and
   survives its own stated falsifier, but adopting it would be a decision-level change to the
   gravity sector (new global fields beyond CLAUDE.md decision 4), and two genuine new costs (spatial
   closure, transient dark energy) are named but not adjudicated against data one way or the other.
5. **The interacting/finite-density correction to the horizon-entanglement coefficient is unmeasured.**
   F355 §7 notes explicitly that "interactions do not move the coefficient by a factor $\sim3$" is an
   expectation, not a measurement — the free-field entanglement calculation is what this chapter's
   F355 result rests on.
6. **No genuinely dynamical mechanism has yet been shown to work.** Net honest state of the finding
   chain, in one sentence: F164 (definite $121$-order problem, wrong sign) → F193 Part A excluded,
   Part B survives → F196 ($p=2$ derived, lands at $\rho_\text{crit}$) → F241 (the sole remaining
   unknown, $\Omega_\Lambda=1-\Omega_m$, is provably outside the reach of the holographic/BH sector)
   → F332 (two attempted dynamical closures fail) → F367/F368 (a third, non-local candidate is
   mathematically viable but not adopted). No finding in this chapter's assigned set, nor any cited
   forward, closes the loop.

## 21.7 Falsifiers

From the relevant claim cards, reported at their actual status:

1. **CL021 (the headline non-claim) carries `falsifier: none`** — a non-claim has nothing to falsify
   by design; what *can* move are its component results. `status: not_claimed` is itself the
   assertion that the project does not claim the cosmological constant is derived.
2. **CL275 (the uniform-reweighting no-go) carries `falsifier: stated`, `status: live`**: (i) an
   exhibited uniform-$\lambda$ mechanism fixing the CC without moving $G$ would falsify it outright
   (shown here to be impossible as stated, given F59's $\Lambda^2$/F164's $\Lambda^4$ sector
   assignments); (ii) showing $1/G$ is *not* sourced by the same zero-point sum (superseding
   F59/F79's induced route) would free F193 Part A and withdraw the card; (iii) an order-selective
   mechanism delivering $\ge1.27\times10^{116}$ would close K9 (partially met by F193§B/F196, which
   supplies $120.66$ of the required $120.76$ decades but lacks dynamics) and by F367's exact identity
   (which meets the selectivity requirement but is not adopted).
3. **CL303 (sequestering) carries `falsifier: stated`, `status: contingent`**: falsifier 4 (a
   demonstrated inconsistency between sequestering's global field content and decision 4's other
   content) is checked by F368 and does **not** fire — the card stays `contingent`, not `withdrawn`.
   Falsifiers 1–3 (the constant-cancellation identity failing for some finite $V_4$; F164's
   $\rho_\text{vac}$ turning out not to be a genuine spacetime constant; F319's operator ledger being
   wrong to treat $\Lambda$ and $1/G$ as separable) remain live, unattempted attack routes on this
   chapter's most speculative result.
4. **CL212 (F241's residual, cited throughout but not one of this chapter's own ten findings) is the
   card carrying the $\Omega_\Lambda$ falsifier**: a future derivation of $\Omega_m$ from a completed
   dark-sector sector (Chapter 22), or a first-principles observer measure, would convert the
   residual from "coincidental" to "derived" — named explicitly by F241 as the two routes that would
   close it.
5. **CL261 (cell-entropy-is-not-a-state-count) carries `falsifier: none`**, and states why: it is an
   arithmetic fact about the irrationality of $2\pi\sqrt3$, not a physical claim contingent on
   observation. What *can* change is the target itself, if F107's canonical cell $a$ is ever revised.
6. **F332's own declared controls are the sharpest structural falsifiers in this chapter for its two
   closed channels**: a demonstration that the Laplacian's DC mode is *not* Fredholm-blind to a
   constant source, or that F178's $AB\equiv1$ scope restriction does not in fact exclude homogeneous
   sources, would reopen channel (ii); a recomputed block-spin exponent pair differing from
   $(-1,+1)$ would reopen the block-spin channel.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\rho_\text{vac}$ | The model's bare lattice zero-point energy density, $g_*\sqrt3\,I_\text{CC}\,\hbar c/a^4$ | §21.2.1 |
| $I_\text{CC}$ | The dimensionless BCC Brillouin-zone integral $\int_\text{BZ}d^3k/(2\pi)^3\,\omega(k)/2=4.081049$ | §21.2.1 |
| $p$ | The holographic dilution exponent in $\rho_\text{grav}(L)\propto L^{-p}$; derived $=2$ | §21.2.3, §21.2.4 |
| $\rho_\text{crit}$ | The critical density $3H_0^2c^2/(8\pi G)$; the saturation value both F196 routes converge on | §21.2.4 |
| $\Omega_\Lambda$ | $\rho_\Lambda/\rho_\text{crit}\approx0.6847$; this chapter's central undischarged residual | §21.2.5 |
| $s_\text{cell}$ | The per-F107-cell horizon entropy required by $S=A/4$, $=2\pi\sqrt3$ nats exactly | §21.2.6 |
| $c_\text{walk}$ | F355's directly-computed vacuum-entanglement coefficient per BCC walk per unit horizon area | §21.2.6 |
| $C$ | A spacetime-constant piece of the matter trace $T(t)$, the object Kaloper–Padilla sequestering annihilates exactly under spacetime averaging | §21.2.8 |

---

*This chapter logs no new gap: the one genuine internal tension it inherits and does not close
(the F79/F355 horizon-entropy-coefficient bracket, §21.2.6/§21.6 item 3) is already fully disclosed
by its own source finding (F355 §7–§8) and by Chapter 20's forward flag, so no undisclosed hole is
being papered over — per `docs/monograph/GAPS.md`'s own stated scope, this is carried forward in
prose rather than given a new `[G-N]` entry. No finding, claim card, module, or test record was
created or modified in the writing of this chapter.*
