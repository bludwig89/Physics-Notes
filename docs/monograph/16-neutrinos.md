# Chapter 16 — Neutrinos

*Chapter 16 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F47-majorana-seesaw-higgs-free.md`, `findings/F341-majorana-forced-by-hypercharge-closure.md`,
`findings/F236-three-generation-seesaw-pmns.md`, `findings/F201-kev-sterile-from-eg-texture.md`,
`findings/F254-t2g-pmns-selector-nogo.md`, `findings/F353-delta-cp-t2g-inheritance.md`,
`findings/F343-majorana-scale-no-link-found.md`, `findings/F266-sterile-neutrino-dark-matter.md`
(the eight findings `00-plan.md` §2 assigns to this chapter, all read in full). Checked against
`docs/theory/supersessions.yaml` (grep of all eight finding numbers against every `superseded:`
list in all 23 records: zero hits — none of this chapter's findings is itself superseded; F165,
which this chapter's own material corrects the attribution of, is **not** one of this chapter's
assigned findings and is not re-litigated here beyond the handoff in §16.2.1). Checked against
`claims-index.md`: **CL018** (F47, `non_claim`/`not_claimed`, "no absolute neutrino mass is
predicted"), **CL290** (F341/F47/F165/F202/F266/F279, `reinterpretation`/`contingent`, "Majorana
is the required completion... conditional on..."), **CL207** (F236, `no_go`/`open`,
`review_state: unreviewed-seed`), **CL223** (F254, `no_go`/`open`, `unreviewed-seed`), **CL294**
(F353, `no_go`/`open`, rolls up to CL223), **CL175** (F201, `no_go`/`open`, `unreviewed-seed`),
**CL232** (F266, `derivation`/`live`, `quantitative`, `unreviewed-seed`), **CL291** (F343,
`no_go`/`live`, `exact`). Four of these eight cards (CL207, CL223, CL175, CL232) carry
`review_state: unreviewed-seed` — mechanically extracted from their finding's own title/status
line, never independently confirmed by a reviewer; this chapter treats their *content* as
established (the underlying findings are gate-tier tested, several independently reviewed — F341
and F353 both carry cold-subagent or inline adversarial reviews) but flags the card
`review_state` itself as unpromoted bookkeeping, not a physics qualification. Notation and results
are those of Chapters 1, 12 and 15 (`01-postulates-and-ontology.md`,
`12-hypercharge-and-electroweak.md`, `15-generations-and-lepton-spectrum.md`) — $\psi$, $U(x)$,
$U(1)_Y$, $y_\nu$, $T_{1u}$, $E_g$, $T_{2g}$, $D_{2h}$ — extended, never redefined.*

## 16.0 What this chapter establishes

Chapter 12 built the model's Higgs-free hypercharge sector and, at its capstone (§12.2.13, R12.13),
reached a point it could not close without borrowing a result from this chapter: the six-constraint
system that quantises hypercharge to a single overall normalisation — reproducing the observed
quark-charge fractions $\tfrac23,-\tfrac13$ — closes only once a sixth row, $2y_\nu=0$, is added to
the five anomaly/mass-step rows Chapter 11/12 already had. That sixth row is not an anomaly; it is
the statement that the right-handed neutrino's Majorana mass bilinear $\nu_R^{\mathsf T}C\nu_R$
must be gauge-invariant under $U(1)_Y$, which forces $y_\nu=0$ exactly. Chapter 12 stated this
precisely and explicitly deferred the construction: "F279's closing constraint is the Majorana
mass step, which belongs structurally to Chapter 16 (Neutrinos, F47 assigned there)... Chapter 16
is where F47 is built in full" (`12-hypercharge-and-electroweak.md` §12.2.13). This chapter delivers
that construction (§16.2.1), and then completes it one step further than Chapter 12 asked for:
not merely that a Majorana term is *available* to $\nu_R$, but that nothing in the model's own
structure protects against it, so that removing it would reopen the very hypercharge-closure result
Chapter 12 relies on (§16.2.2, F341) — the Majorana step is not an optional extra sitting next to
the hypercharge derivation; it is one of that derivation's own load-bearing rows.

With that handoff closed, the chapter's remaining business is the full accounting of what a
Higgs-free see-saw does and does not give the model: the 3×3 extension to three generations and its
sharp internal no-go for lepton mixing (§16.2.3–16.2.4, F236/F254), the formal extension of that
no-go to the Dirac CP phase (§16.2.5, F353), an honest negative on the absolute Majorana scale
itself (§16.2.6, F343), and the dark-sector-adjacent material this chapter owns but does not
duplicate — the keV-sterile node mechanism (§16.2.7, F201) and the sterile neutrino as the model's
own dark-matter candidate (§16.2.8, F266), both forward-cited to Chapter 22 for what belongs there
instead.

## 16.1 Inputs

**Postulates used.** **P6** (mass and hypercharge from the postulated chiral $SU(2)$ connection
$U(x)$, `01-postulates-and-ontology.md` §1.2) is the postulate this entire chapter operates under —
every mass step below, Dirac or Majorana, is a further consequence of P6's Higgs-free gauging, not
a departure from it. **P5** (the massless Weyl-spinor primitive) is what $\nu_R$ itself is, before
any mass step acts on it. **P4** (exact unitarity) underwrites the R-unitarity check on the Majorana
step (F47 M1) in the same sense it underwrites every mass/kinetic step in Chapters 11–12.

**Prior results used, precisely.** **R12.10–R12.13** (Ch.12, F41/F42/F279) are the hypercharge
machinery this chapter's Majorana step must be — and is shown to be — compatible with: $U(x)$
carries $U(1)_Y$ as a diagonal phase factor, $\nu_R$ is assigned $Y_{\nu_R}=0$ as part of that
system, and R12.13 is the specific result (F279/S13) this chapter's §16.2.1 supplies the
construction for. This chapter does not re-derive R12.13's linear-algebra closure (five anomaly/
mass-step rows plus the Majorana row, rank 6, nullspace 1, ratios $4:-2:-3:-6:0:3$) — that is
Chapter 12's own content — it supplies the physical mechanism (the Majorana bilinear's gauge
transformation) that *makes* $2y_\nu=0$ a genuine constraint rather than an assumption. **R15.1**
(Ch.15, F75: exactly three generations, $O_h$ has no 4-dimensional single-valued irrep) is what
makes a 3×3 (not $N\times N$) see-saw the correct generalisation in §16.2.3. **R15.13/R15.15**
(Ch.15, F93/F175: the unique non-mixing splitting channel is $E_g$, on the BCC second-neighbour
shell; the charged-lepton condensate angle $\delta^*=2/9$ rad by weight-as-phase) are the specific
representation-theoretic objects §16.2.3's $E_g/Z_3$ neutrino texture and §16.2.4's PMNS no-go both
build on — cited, not re-derived; this chapter does not repeat Chapter 15's own derivation of why
$E_g$ is the unique diagonal-non-mixing channel or why $T_{2g}$ is the unique off-diagonal one.

**Free inputs consumed — the chapter's central honesty point.** Per **CL018** and **F343**, this
chapter's mechanism is a genuine mechanism with **two absolute scales left explicitly undetermined**,
and stating this plainly, rather than letting a mechanism read as a prediction, is this chapter's
first job:

1. **The absolute active-neutrino mass scale is not predicted.** F47 supplies the see-saw
   *operator* and shows gauge invariance forces $y_\nu=0$, but "the operator's coefficient $M_R$ is
   not constrained by any lattice quantity. A measured absolute neutrino mass therefore fixes $M_R$
   rather than testing the model" (CL018). KATRIN, $0\nu\beta\beta$, and cosmological
   sum-of-masses bounds are all silent on this chapter's claims for exactly this reason.
2. **The absolute Majorana scale $M_{R0}$ is not predicted either, and F343 checks this rather than
   merely asserting it** (§16.2.6 below): neither of the model's two existing scale-anchoring
   structures — the F183/F107 Planck-derived lattice cutoff, or the $E_g/Z_3$ condensate already
   used for the neutrino mass *texture* — supplies a link to $M_{R0}$, on three independently
   checked grounds. $M_{R0}$ joins $v$ (Ch.12), the quark masses, and $m_{E_g}$ (Ch.15) as a fifth
   member of the same open cluster: the model derives dimensionless mass *shapes* to high precision
   and has, so far, no mechanism for any absolute mass scale relative to the cutoff.
3. **The three PMNS mixing angles and the Dirac CP phase are free inputs**, proven so rather than
   merely unfitted (§16.2.4–16.2.5, F254/F353) — three independent $T_{2g}$ magnitude order
   parameters plus their phases, none pinned by any residual lattice symmetry.
4. **The overall Dirac-mass hierarchy $M_D$ and the neutrino condensate angle $\delta_\nu$** are
   likewise free, in the same sense the charged-lepton condensate angle $\delta^* $ is fixed by
   weight-as-phase (Ch.15) but the *neutrino* sector's own condensate angle is not asserted to be
   the same number — F201/F236 treat $\delta_\nu$ as the neutrino sector's own free parameter,
   argued (not derived) to share the charged-lepton sector's *texture form* because both are
   $A_{1g}+E_g$ objects on the same BCC second shell, but explicitly not required to share its
   *value*.

## 16.2 The derivation

### 16.2.1 The Higgs-free Majorana step and the see-saw mechanism (F47)

Chapter 12 established (F41) that $U(x)$ carries hypercharge as a diagonal phase, with $\nu_R$
assigned $Y_{\nu_R}=0$ — the Standard-Model assignment, but here consumed only through a Dirac mass
step $M_D$ coupling $\eta_L$ to $\chi_R\equiv\nu_R$. The standard see-saw mechanism additionally
allows a **bare Majorana mass** on the gauge-singlet $\nu_R$,
$$\mathcal L_M=-\tfrac12M_R\bigl(\nu_R^{\mathsf T}\varepsilon\,\nu_R+\text{h.c.}\bigr),\qquad
\varepsilon=i\sigma^2,$$
which in the Standard Model is the *only* gauge-invariant mass term available to a singlet, because
$\nu_R^{\mathsf T}\varepsilon\nu_R$ carries hypercharge $2Y_{\nu_R}=0$. F47 (2026-05-28) asks
whether the Higgs-free CA construction can carry this term at all, and answers yes on both counts
it checks.

**The QCA Majorana step is R-unitary.** Writing the bare Majorana step as the closed-form
integration of the Bogoliubov–de Gennes-form equation of motion $i\partial_t\chi_u=+M_R\chi_d^*$,
$i\partial_t\chi_d=-M_R\chi_u^*$ gives
$$\chi_u'=c_M\chi_u-is_M\chi_d^*,\qquad \chi_d'=c_M\chi_d+is_M\chi_u^*,\qquad
c_M=\cos(M_Rdt),\ s_M=\sin(M_Rdt),$$
an **anti-linear** step (it couples $\chi$ to $\chi^*$ — the source of lepton-number violation) that
a direct algebraic expansion shows is exactly norm-conserving on the four real degrees of freedom:
$$\boxed{\;|\chi_u'|^2+|\chi_d'|^2=|\chi_u|^2+|\chi_d|^2\text{ exactly; verified over }M_R\in\{0,\ldots,10^6\},\ dt\in\{0.05,\ldots,1.27\},\text{ 200-step compose}\;}\tag{R16.1}$$
(F47 M1, residual $2.25\times10^{-11}$, target $10^{-9}$, PASS.)

**The $U(1)_Y$ selection rule is the Higgs-free realisation of the Standard-Model rule.** Under
$V_Y[\beta]$, the singlet rotates as $\chi\to e^{i\beta Y_{\nu_R}/2}\chi$, so the Majorana bilinear
$\chi^{\mathsf T}\varepsilon\chi$ picks up phase $e^{i\beta Y_{\nu_R}}$: the step is invariant iff
$Y_{\nu_R}\equiv0$. F47's tests M2/M3 verify both halves directly — residual exactly $0.0$ at
$Y_{\nu_R}=0$, and a genuine, non-zero, correctly-bounded residual at $Y\in\{-2,+\tfrac43\}$:
$$\boxed{\;\text{the bare Majorana step is }U(1)_Y\text{-invariant iff }Y_{\nu_R}=0\text{ exactly — the identical rule the Standard Model imposes, here enforced by the same gauge constraint Chapter 12 built, with no Higgs field anywhere}\;}\tag{R16.2}$$
This is the mechanism, not merely the conclusion, that Chapter 12 §12.2.13 forward-cited: it is
what makes "$2y_\nu=0$" a physical gauge-invariance requirement on a concrete lattice operator,
rather than an algebraic constraint imposed by fiat.

**The see-saw scaling is exact, then asymptotic, and is verified against the lattice operator
itself, not only the textbook $2\times2$ matrix.** Combined with the F27/F41 Dirac step, the
$(\nu_L,\nu_R)$ mass matrix is the canonical see-saw form
$M=\bigl(\begin{smallmatrix}0&M_D\\M_D&M_R\end{smallmatrix}\bigr)$, with eigenvalues
$\lambda_\pm=\tfrac12\bigl(M_R\pm\sqrt{M_R^2+4M_D^2}\bigr)$. In the hierarchical limit $M_R\gg M_D$:
$$\boxed{\;|\lambda_-|=\frac{M_D^2}{M_R}\Bigl(1-\frac{M_D^2}{M_R^2}+O\bigl((M_D/M_R)^4\bigr)\Bigr)\;}\tag{R16.3}$$
verified against `numpy.linalg.eigvalsh` over 64 random samples (F47 M5, residual
$1.82\times10^{-12}$) and against the sampled ratio $M_R/M_D\in\{3,\ldots,10^5\}$, where the
deviation from $M_D^2/M_R$ tracks the predicted $(M_D/M_R)^2$ bound at every point (F47 M6). A
separate, independently-constructed $8\times8$ Bogoliubov–de Gennes Hamiltonian — the exact
$dt\to0$ Jacobian of the lattice mass step itself, not a hand-written continuum matrix — reproduces
the same light eigenvalue to $\le10^{-12}\,M_R$ at every sampled ratio (F47 M4/M6), connecting the
CA realisation and the textbook see-saw spectrum at machine precision rather than by analogy.

**What this buys the model.** With $M_D\sim m_e$ and $M_R\sim10^{12}$–$10^{15}$ GeV, the see-saw
produces $m_\nu\sim10^{-2}$–$10^{-5}$ eV automatically — the observed range — from a single large
scale rather than an unnaturally tiny Yukawa coupling. This is a genuine structural gain (a
mechanism where the Standard Model, with $\nu_R$ added by hand, has none), and it is the mechanism
whose absolute normalisation §16.1 item 2 and §16.2.6 below establish is not itself derived.

### 16.2.2 Majorana is the structurally required completion, not merely a permitted option (F341)

F47 shows the Majorana term is *available*; it does not show it is *forced*. A $\nu_R$ carrying only
the ordinary Dirac mass step (no Majorana bilinear) is, considered in isolation, an equally
gauge-invariant construction — permitted, not excluded. F341 (2026-08-31, cold-subagent reviewed,
CONFIRMED-NARROWER) closes this gap with two convergent, independently mechanised arguments,
completing the Chapter 12 handoff one step further than R16.2 alone does.

**Argument S1 — no protecting symmetry exists in the model.** A Majorana term is forbidden only by
a symmetry under which the bilinear is charged. Colour and $SU(2)_L$ are irrelevant ($\nu_R$ is a
singlet under both); $U(1)_Y$ *permits* the term (R16.2) rather than forbidding it. The only
remaining candidate is a separate global charge — lepton number, or gauged $B\!-\!L$ — under which
$\nu_R$ would be charged independently of $Y$. A direct inspection of `casim.constants`,
`casim.constants.electroweak`, and `casim.engine.gauge.hypercharge` finds **no such generator
registered anywhere** in the model, and this is not merely an omission: the model's own leptogenesis
account (F202, not itself a Chapter 16 finding) treats the Majorana step's lepton-number violation
as **load-bearing** — the Sakharov condition the resonant keV-sterile production mechanism (§16.2.8)
needs. Forbidding the term would require inventing a global symmetry with no other role in the
model's structure, in direct tension with a result the model already depends on elsewhere.

**Argument S2 — removing the term reopens the F165/F279 hypercharge closure, mechanically.** F341
re-derives Chapter 12's R12.13 system independently (not by importing F279's own code) and adds the
form F279 itself stopped short of stating. Carrying $\nu_R$ with a general hypercharge $y_\nu$ and
only a Dirac-type mass step, the anomaly/mass-step system
$$3y_Q+y_L=0,\quad2y_Q-y_u-y_d=0,\quad y_d=y_Q-y_\phi,\quad y_e=y_L-y_\phi,\quad y_\nu=y_L+y_\phi$$
has **rank 5 over 7 unknowns** — a genuine 2-dimensional nullspace in which $y_\phi$ (the parameter
fixing the quark-charge fractions $\tfrac23,-\tfrac13$) appears as a **free symbol** in the general
solution. Adding the Majorana row $2y_\nu=0$ raises the rank to 6, collapsing the nullspace to one
dimension and reproducing exactly the certified F165/F279 line
$y_u{:}y_d{:}y_L{:}y_e{:}y_\nu{:}y_\phi=4{:}{-2}{:}{-3}{:}{-6}{:}0{:}3$. A control check confirms
that with the Majorana row dropped, alternative values ($y_\phi=y_Q$ or $\tfrac12y_Q$) solve the
remaining system equally well and give the **wrong** quark charges — nothing else in the model's
existing structure singles out the observationally correct ratio:
$$\boxed{\;\text{dropping the Majorana row leaves the hypercharge system rank 5 (nullspace dim 2), with }y_\phi\text{ genuinely free; restoring it uniquely closes the certified rank-6, nullspace-1 line — no other existing row can substitute}\;}\tag{R16.4}$$
(F341, 5/5 checks PASS, exact over $\mathbb{Q}$.)

**What this does and does not establish.** F341 is explicit that this is a structural-consistency
and genericity argument (the field-theory "totalitarian principle": absent a symmetry forbidding a
term, it is not technically natural to omit it, and this is standard vocabulary in exactly this
context in the neutrino-mass literature), **not a gauge-invariance no-go that makes a Dirac-only
$\nu_R$ logically impossible.** A Dirac-only completion remains constructible — but only by (a)
adding a global lepton-number symmetry found nowhere else in the model, in tension with F202's own
use of $L$-violation, and (b) accepting that the certified F165/F279 result no longer closes,
reintroducing $y_\phi$ as a second free input the project's own elegant-design stance (CLAUDE.md
decision 6) exists to avoid. This is the completion of Chapter 12's handoff: **within this model's
own structure — not the generic Standard Model, which carries no analogous dependency — keeping
the already-certified hypercharge closure requires keeping the Majorana term.** The claim (CL290)
is accordingly `status: contingent`, explicitly tied to F165/F279 continuing to stand and to no
protecting symmetry being added.

An external, model-independent anchor is worth naming precisely because it does *not* depend on
this argument: the Schechter–Valle "black-box" theorem (1982) states that an observation of
neutrinoless double-beta decay implies a nonzero Majorana mass for at least one neutrino species
regardless of mechanism; current non-observation (KamLAND-Zen 2024, $T_{1/2}^{0\nu}>3.8\times10^{26}$
yr, $m_{\beta\beta}<28$–$122$ meV) leaves this the open empirical test, separate from and
unaffected by F341's internal structural argument.

### 16.2.3 The 3×3 extension: masses derived exactly, PMNS forced to the identity (F236)

F47's single-flavour block generalises directly once three generations are on the table (R15.1,
Ch.15, F75). The full $6\times6$ see-saw matrix is
$$M_6=\begin{pmatrix}0&M_D\\M_D^{\mathsf T}&M_R\end{pmatrix},$$
with $M_R$ textured by the same $E_g/Z_3$ crystal-field mechanism Chapter 15 built for the
charged-lepton masses (R15.13, F93): $\sqrt{M_a}=M_{R0}\bigl[1+\sqrt2\cos(\delta_\nu+\tfrac{2\pi
a}3)\bigr]$, $a=0,1,2$, with $M_R=\mathrm{diag}(M_a)$ in the cube-axis basis — argued, not derived,
to carry the same texture *form* as the charged-lepton condensate because both are $A_{1g}+E_g$
objects on the same BCC second-neighbour shell, with its own independent angle $\delta_\nu$.

**The three-generation see-saw reduces exactly to three copies of F47.** Because $M_D$ (assumed to
sit in the same cube-axis basis) and $M_R$ are simultaneously diagonal, the type-I light block
$m_\nu=-M_DM_R^{-1}M_D^{\mathsf T}=-\mathrm{diag}(M_{D,a}^2/M_{R,a})$ is diagonal, and:
$$\boxed{\;\text{the 3\ensuremath{\times}3 light-neutrino spectrum is three independent copies of F47's }M_D^2/M_R\text{, matching the module's own diagonalisation to relative residual}<10^{-9}\;}\tag{R16.5}$$
(F236 test S1.) A direct cross-check between the full complex $6\times6$ eigenproblem and the exact
type-I block confirms agreement to $\sim10^{-9}M_{R0}$ relative in the hierarchical regime, and
every spectrum is validated by a hand-rolled residual $\max_j\|Mv_j-\lambda_jv_j\|$ rather than a
library eigensolver alone (F236 test S5) — the numerics House Rule this monograph has followed
since Chapter 5's warning about chiral-transform hazards.

**PMNS $=\mathbb 1$ — an exact structural no-go, not a fit failure.** Because the charged-lepton
mass matrix is also $E_g$-diagonal in the same cube-axis basis (Chapter 15's own construction), the
charged-lepton rotation is $U_e=\mathbb 1$ there, so $\mathrm{PMNS}=U_e^\dagger U_\nu=U_\nu$; and
because $m_\nu$ above is diagonal, its eigenvectors are the coordinate axes themselves:
$$\boxed{\;E_g\text{ texture on both }M_D\text{ and }M_R\ \Longrightarrow\ \mathrm{PMNS}=\mathbb 1,\ \theta_{12}=\theta_{13}=\theta_{23}=0\text{ to }<10^{-9}\ \text{degrees, for every choice of the }E_g\text{ inputs}\;}\tag{R16.6}$$
(F236 test S2.) This is not an artefact of a particular numerical choice — changing the condensate
angles or overall scale only rescales the *eigenvalues*, never the *eigenvectors*, which stay
pinned to the cube axes by representation theory alone (F93 O1, Ch.15). The observed $O(1)$ PMNS
angles ($\theta_{12}\approx33°$, $\theta_{23}\approx49°$) are therefore **impossible** from the
$E_g$ texture under any parameter choice — a sharp contrast with the near-diagonal CKM matrix,
where small mixing would be a near-success of the identical diagonal picture.

**Mixing is localised to the orthogonal $T_{2g}$ channel — a fit, honestly counted.** F93's
falsifiable commitment that inter-generation mixing must live in the second-shell, off-diagonal
$T_{2g}$ channel is made quantitative here: adding a symmetric perturbation
$T=\bigl(\begin{smallmatrix}0&t_{xy}&t_{zx}\\t_{xy}&0&t_{yz}\\t_{zx}&t_{yz}&0\end{smallmatrix}\bigr)$
to $M_R$ switches mixing on, and a six-parameter fit
$(\delta_D,\delta_\nu,M_{R0},t_{xy},t_{yz},t_{zx})$ reproduces all five NuFIT-5.2 (normal-ordering)
oscillation observables — $\theta_{12}=33.4°$, $\theta_{13}=8.6°$, $\theta_{23}=49.0°$,
$\Delta m^2_{21}=7.42\times10^{-5}$ eV$^2$, $\Delta m^2_{31}=2.51\times10^{-3}$ eV$^2$ — to final
cost $\approx0$ (F236 test S4). **This is stated as a fit, not a prediction, in the finding's own
language: six inputs for five observables, with zero predictive slack.** The chapter's honest
ledger after F236: the light masses and their hierarchy are derived; the mixing angles are a fit
whose free-parameter count Chapter 16's next result (F254) shows is not an artefact of a
particular ansatz but forced by group theory.

### 16.2.4 No lattice selector exists for the PMNS mixing channel — a stabilizer theorem (F254)

F236 leaves an open question: is the "six inputs for five observables" merely today's best fit, or
could a smarter symmetry argument eventually pin the three $T_{2g}$ amplitudes the way weight-as-
phase (Ch.15, R15.15) pins the charged-lepton condensate angle? F254 (2026-07-16) answers this as a
theorem, not a further numerical search.

**The residual symmetry acts on the three mixing amplitudes as three inequivalent irreducible
representations.** Chapter 15's own O3 result (F93) established that a generic-angle $E_g$
condensate leaves the stabilizer $D_{2h}=\{\mathrm{diag}(s_x,s_y,s_z):s_a=\pm1\}$ (order 8), with
**no** residual axis permutation — the generation $S_3$ is completely broken by the very condensate
that fixes the charged-lepton masses. Under this residual $D_{2h}$, the $T_{2g}$ perturbation
transforms as $T\mapsto STS^{\mathsf T}$, so each off-diagonal entry picks up a pure sign
$t_{ab}\mapsto s_as_b\,t_{ab}$. Computing the character of each amplitude over the 8 group elements
gives three **distinct**, zero-sum sign patterns:
$$\boxed{\;(t_{xy},t_{yz},t_{zx})\ \text{transform as three INEQUIVALENT 1-d irreps }B_{1g}\oplus B_{2g}\oplus B_{3g}\ \text{of }D_{2h}\;}\tag{R16.7}$$
(F254 test T1, exact.) Because the three irreps are inequivalent, **no element of the residual
symmetry group maps one amplitude to another** — they are three genuinely independent order
parameters, each condensing in its own symmetry channel, and this is the exact group-theoretic root
of F236's "free inputs" result.

**The one candidate mechanism that could have rescued a selector — F92 equipartition — is
structurally inapplicable.** Chapter 15's weight-as-phase construction leans on an equipartition
argument (F92, R15.9: two independently derived mass laws force $t=45°$, unique) for the
charged-lepton amplitude; the same mechanism *cannot* apply here, because equipartition is defined
**within a single degenerate multiplet**, and R16.7 shows the $E_g$-broken vacuum has already split
the $T_{2g}$ triplet into three *inequivalent* channels — there is no surviving degenerate multiplet
to equipartition across. Concretely, the democratic point $t_{xy}=t_{yz}=t_{zx}$ is invariant under
only $\{+\mathbb1,-\mathbb1\}$ of $D_{2h}$ (order 2 of 8, not symmetry-protected):
$$\boxed{\;\text{the F92 equipartition selector — the mechanism that fixed the charged-lepton condensate's }\sqrt2\text{ amplitude — has no }T_{2g}\text{ analogue: there is no degenerate multiplet for it to act on}\;}\tag{R16.8}$$
(F254 test T2.)

**Numerical confirmation that no one-parameter symmetric ansatz reaches the data.** Scanning
democratic and single-channel one-parameter forms of $T_{2g}$ against the same NuFIT-5.2 targets:
the democratic ansatz misses by $462\,\mathrm{deg}^2$, and each single-amplitude ansatz drives
essentially one angle only (misses of $1190$–$2475\,\mathrm{deg}^2$); only the full,
independently-parametrised three-amplitude form reaches the data, at $\sim10^{-11}$ deg residual —
with **exactly three inputs for three angles, zero predictive slack** (F254 test T3). Turning the
selector search on does not disturb the derived mass sector: with $T_{2g}=0$, PMNS $=\mathbb1$ is
reproduced to $<10^{-6}$ deg exactly as F236 found (F254 test T4).

**Verdict.** The PMNS mixing angles are **genuinely free** — not an unfitted residual but a proven
absence of any residual-symmetry or equipartition selector, parallel in kind (though independent in
content) to the model's other genuinely free order parameters elsewhere in the tree (e.g. the
geon-abundance parameter $\beta$ of the dark sector, forward-cited from Chapter 22). A lattice
derivation of PMNS would require an explicit *dynamical* computation of three independent
$T_{2g}$ condensation gaps — the direct analogue of how the charged-lepton masses reduced to the
$E_g$ Landau ratio (Ch.15, F234) — and no such computation exists.

### 16.2.5 The Dirac CP phase inherits the same no-go, formally (F353)

F236's own table flagged the Dirac CP phase $\delta_{CP}$ as needing complex $T_{2g}$ amplitudes —
"a 4th input; unchanged" — without checking whether F254's group-theoretic argument actually
transfers to the phase sector. F353 (2026-09-03, internally reviewed) checks this formally rather
than leaving it as a plausible inheritance.

**The group-theoretic argument transfers verbatim.** F254's whole argument for the *magnitude*
sector rests on $D_{2h}$ acting on $T_{2g}$ by the real sign $s_as_b$. That action is identical
whether $t_{ab}$ is real or complex: a real orthogonal similarity transform can only flip a complex
number's overall sign (a phase shift of exactly $0$ or $\pi$), never rotate it to an intermediate
value. Direct verification over 200 random complex amplitudes and all 8 group elements confirms
this to machine precision (phase-shift deviation from $\{0,\pi\}$ at most $8\times10^{-17}$):
$$\boxed{\;D_{2h}\text{ transports a complex }T_{2g}\text{ amplitude by the identical real sign }s_as_b\text{ — the phase content is exactly as un-related by the residual symmetry as the magnitude is}\;}\tag{R16.9}$$
(F353 test T1.) F254's T1 (three inequivalent irreps) and T2 (equipartition inapplicable, no
degenerate multiplet) therefore hold for the phase of each amplitude with **no new group-theoretic
argument needed** — the residual symmetry group never sees the phase at all.

**The phase content is generic and unprotected, confirmed numerically.** Writing $\delta_{CP}$ via
the standard rephasing-invariant Jarlskog combination
$J=\mathrm{Im}(U_{e1}U_{\mu2}U_{e2}^*U_{\mu1}^*)$ built from the F236/F254 pipeline: F254's own
real NuFIT-fit magnitudes give $J=0$ **exactly** — but this is shown to be a direct consequence of
choosing real inputs (any real symmetric matrix has a real orthogonal eigenbasis), not a protected
value. Holding those same magnitudes fixed and drawing 1000 independent random phase triples
populates a continuous, generic range $J\in[-0.049,0.049]$ with **zero** draws returning to
$J\approx0$; the phase-analogue of magnitude-democracy is equally unprotected
($\max|J|=0.059$ over 300 draws):
$$\boxed{\;\delta_{CP}\text{ is genuinely free by the identical mechanism F254 proved for the mixing angles — no new symmetry, no additional structure the angles didn't already need}\;}\tag{R16.10}$$
(F353 tests T2–T4.) This closes ledger row D4's second half: `docs/status/open-derivations.md`
grades parameter #26 $\mathrm{ABSENT}\to\mathrm{EXCLUDED}$, matching the grading already given to
the PMNS angles themselves.

> Building this check surfaced and fixed two independent, pre-existing defects in the model's
> Takagi-factorisation code path (`casim.engine.particles.majorana.takagi_light_masses`'s
> complex-symmetric branch) — an unreachable-dead-code tolerance bug that would have silently
> forced $J=0$ for *any* complex input at the model's actual mass scale, and a sign-convention-only
> defect in the eigenvector construction. Neither affects F236 or F254, both of which are
> exclusively real and never exercise that branch; both are recorded here because F353's own
> positive result (R16.9–R16.10) depended on having fixed them first, and a naive attempt at this
> exact check before the fix would have "confirmed" $\delta_{CP}=0$ for the wrong reason.

### 16.2.6 The absolute Majorana scale $M_R$ is not fixed by anything in the model — checked, not merely asserted (F343)

Chapters 12 and 15's own precedents raise an obvious question before accepting $M_{R0}$ as a bare
free input: does either of the model's two existing scale-anchoring structures — the F183/F107
Planck-derived lattice cutoff, or the $E_g/Z_3$ condensate already used for the neutrino mass
*texture* — offer any link, even approximate? F343 (2026-08-31) runs this check explicitly on both
named candidates and adds a third the ledger did not anticipate, rather than leaving the absence
unexamined.

**Leg 1 — the lattice cutoff: a genuine ~19-decade gap, with no motivated ratio close to it.** The
canonical cell fixes $\Lambda=3^{-1/4}M_\text{Pl}=9.277\times10^{18}$ GeV (F107, Ch.17's own
territory, cited here). At F201's own $M_{R0}\sim1$ GeV benchmark, $\Lambda/M_{R0}\approx
9.28\times10^{18}$ ($\log_{10}\approx18.97$, $\approx19$ decades). An exhaustive scan of small
integer powers ($\le12$) of every dimensionless ratio already registered in `casim.constants` —
$\delta^*=2/9$, $1/(72\pi)$, $\sqrt2$, $6\lambda_6$, $8\pi\sqrt3$, $1/(a/\ell_P)$ — against this
target finds a closest approach of $(1/(72\pi))^8=10^{-18.836}$, **0.132 dex (a factor of $1.35$)
away**:
$$\boxed{\;\text{no lattice-registered dimensionless ratio, raised to any small integer power, lands within a small fraction of a decade of the required }\sim10^{-19}\text{ suppression — the closest hit is flagged as an unclaimed numerical coincidence, not adopted}\;}\tag{R16.11}$$
(F343 tests C1–C2.) The disanalogy with $G=a^2c^3/(8\pi\sqrt3\hbar)$ (Ch.18, F79) is made explicit
and checked (test C3): $G$'s cutoff-derivation carries **zero hierarchy** ($1/(8\pi\sqrt3)=0.023$,
$O(1)$) — it is the same scale $a$ re-expressed in SI units, not a second, independent scale
roughly $10^{-19}$ of it. Citing F79 as a precedent for "the cutoff fixes scales" would be a
category error; $M_R$ is exactly the class of problem ($v/\Lambda$, quark masses$/\Lambda$,
$m_{E_g}/\Lambda$) the model has never yet solved for any fermion or condensate.

**Leg 2 — the $E_g$ condensate provably factors the overall scale out.** The texture's own defining
relation $\sqrt{M_a}=M_{R0}[1+\sqrt2\cos(\delta_\nu+\tfrac{2\pi a}3)]$ factors $M_{R0}$ out of the
bracket **identically** — verified symbolically (`sympy`, exact, test C4) for every generation and
every $\delta_\nu$ — and rescaling $M_{R0}\to\lambda M_{R0}$ over six decades leaves every mass
ratio, every mixing angle, and the F201 cancellation-node location invariant to better than
$10^{-10}$ (test C5): the condensate mechanism is provably **blind** to $M_{R0}$, not merely silent
about it. This generalises Chapter 15's own POSIT-N no-go (F253: the $E_g$ representation-theoretic
machinery supplies a dimensionless weight or a $2\pi/3$-quantised angle, never an independent
absolute scale) one further dimensional category — from a radian to a mass.

**Leg 3 — $\nu_R$'s own total gauge-singlet status forecloses the model's only dynamical
scale-generating mechanism.** The model has exactly one mechanism anywhere in its tree for turning
the Planck-scale cutoff into a hierarchically *small* physical scale without fine-tuning:
asymptotic-freedom running of a confining, non-Abelian gauge coupling — how $\Lambda_\text{QCD}$
arises from $\Lambda$ (Ch.13's territory). $\nu_R$ is a total SM singlet (no colour, no $SU(2)_L$,
$Y=0$ structurally forced by F47 and reaffirmed by F341) and therefore couples to **none** of the
model's running or confining sectors — a direct source-code check confirms
`casim.engine.particles.majorana` imports nothing beyond `numpy` (test C6):
$$\boxed{\;\text{the same total-singlet property that makes the Majorana term gauge-invariant and therefore possible at all (F47, F341) is exactly the property that removes every dynamical mechanism the model has elsewhere for setting a fermion's mass scale relative to the cutoff}\;}\tag{R16.12}$$
(F343 test C6.)

**Verdict.** Ledger row D4 does not close. $M_R$ is reclassified from an isolated, unexamined
residual into the fifth named member of an existing cluster — alongside $v$ (Ch.12), the quark
masses, and $m_{E_g}$ (Ch.15) — of "the model derives dimensionless mass *shapes* exactly and has,
so far, no mechanism for any absolute mass scale relative to $\Lambda$." Named routes that would
change this verdict (F343 §8): a future gauge coupling attached to $\nu_R$ (voids leg 3); a general
solution to the $v$/quark-mass/$m_{E_g}$ cluster (would need re-checking against $M_R$); or a
dedicated $M_D$/$M_R$ prefactor-sharing argument (not attempted).

> **Note on the two different $M_{R0}$ benchmarks used across this chapter's sources, stated
> explicitly to avoid the appearance of an unstated inconsistency.** F236's illustrative fit
> (§16.2.3) uses $M_{R0}=10^{12}$ GeV purely to demonstrate the PMNS mechanism against a canonical
> heavy see-saw scale; F201/F266 (§16.2.7–16.2.8) use $M_{R0}\sim1$ GeV, the $\nu$MSM heavy-sterile
> benchmark, to land a keV dark-matter candidate. Both are legitimate illustrative choices of the
> same genuinely free parameter F343 shows is unfixed by anything in the model — there is no single
> "the" value of $M_{R0}$ this chapter or its sources assert, and the two benchmarks answer two
> different questions (mixing-mechanism demonstration vs. dark-matter phenomenology), not one.

### 16.2.7 A structural (not derived) route to a light sterile eigenvalue (F201)

Separately from the absolute-scale question, F201 (2026-06-30) asks a narrower one: given that the
$E_g/Z_3$ texture is applied to $M_R$ at all, does the texture's own *shape* — independent of its
overall scale — ever prefer one eigenvalue to sit far below the others? The answer is a genuine,
if partial, structural mechanism.

**The texture has cancellation nodes.** The defining relation $\sqrt{M_a}=M_{R0}[1+\sqrt2\cos(
\delta_\nu+\tfrac{2\pi a}3)]$ vanishes identically whenever $\delta_\nu+\tfrac{2\pi a}3=135°$ —
an exact algebraic zero, not a numerical coincidence ($1+\sqrt2\cos135°=0$ identically). A
generation sitting near such a node has a parametrically light $M_a$, for the same structural
reason the electron — the generation nearest the charged-lepton texture's own analogous minimum —
is the lightest charged lepton:
$$\boxed{\;\text{one eigenvalue of }M_R\text{ can be made parametrically light by proximity to a }Z_3\text{ cancellation node — a structural mechanism, not an arbitrary small parameter}\;}\tag{R16.13}$$
Scanning the node-proximity angle shows the lightest-to-heaviest ratio collapses smoothly and
rapidly: from $5.9\times10^{-2}$ at $\delta_\nu=60°$ (anti-node) to $5.4\times10^{-9}$ at
$\delta_\nu=134.99°$. Reproducing the $\nu$MSM's own $M_1/M_3\sim10^{-6}$ split requires
$\delta_\nu=134.86°$ — a proximity of only $\approx0.14°$ to the node — landing, at the $\nu$MSM's
own overall scale $M_{R0}\sim1$ GeV, $M_1\approx5.6$ keV (the dark-matter candidate, §16.2.8) and
$M_3\approx5.6$ GeV (the heavier steriles).

**What this is and is not.** The node itself, and the fact that a node-proximate generation is
light, is exact algebra. That $M_R$ carries the same texture *form* as the charged leptons is
argued structurally (same field type, same lattice shell — F201's own words: "structural; not a
new posit") rather than derived from the QCA rule directly. The specific keV value is
**accommodated, not derived**: it requires both the overall scale $M_{R0}\sim1$ GeV (itself the
$\nu$MSM's own phenomenological choice, and per F343 unfixed by anything in this model either) and
the $\approx0.14°$ node-proximity, treated as a free angle. F201's own honest framing is that the
*smallness* of a $10^{-6}$ hierarchy is no longer mysterious — it reduces to a modest
$\sim10^{-3}$-radian angular proximity, because the suppression acts on $\sqrt M$ — not that the
keV scale itself is pinned.

> This mechanism is the model's own structural link between the neutrino-mass texture (this
> chapter's own §16.2.3 territory) and the dark-sector sterile-neutrino candidate that Chapter 22
> treats in full (relic abundance, resonant-production window, observational status). This chapter
> states the mechanism and its honest scope; Chapter 22 is where the cosmological consequences are
> worked out.

### 16.2.8 The sterile right-handed neutrino as the model's own dark-matter candidate (F266)

F266 (originally F200, renumbered 2026-07-31 per a documented finding-number collision — see the
banner in the finding file itself; not a physics withdrawal) identifies the F47 sterile $\nu_R$ as
the model's own dark-matter candidate, closing a requirement an earlier finding (F199, not a
Chapter 16 finding) had named but not filled: a state with no Standard-Model gauge charge, coupled
only super-weakly, so that it is cosmologically long-lived where the model's other candidate (an
$E_g$ amplitude mode) decayed in $\sim10^{-21}$ s.

**Existence is derived, not assumed.** $\nu_R$ is a genuine total SM singlet with $Y_{\nu_R}=0$
**structurally forced** — the same result §16.2.1/§16.2.2 (F47/F341) establish for entirely
different reasons (gauge invariance of the Majorana term, and the hypercharge-closure dependency).
The model did not need to add a dark-matter candidate; the electroweak/Majorana sector it built for
other reasons already contains one.

**Stability is computed, and the contrast with the excluded alternative is the point.** A sterile
neutrino decays only through its small active-sterile mixing $\theta\sim M_D/M_R$, dominantly via
$\nu_s\to3\nu$ (neutral current) and the radiative $\nu_s\to\nu\gamma$ channel. At a benchmark
$m_s=7.1$ keV, $\sin^22\theta=5\times10^{-12}$:
$$\boxed{\;\tau/t_0\approx2.9\times10^9\ (\text{stable on cosmological timescales}) - \text{contrasted directly against the }E_g\text{ amplitude mode's own }\tau/t_0\sim10^{-38}\ (\text{F199})\;}\tag{R16.14}$$
The physical point is structural, not merely numerical: a sterile state's decay is
mixing-suppressed by construction, while a lepton-mass condensate's is not — the two candidates
fail or pass this bar for a reason tied to their own gauge content, not by tuning.

**The abundance window is accommodated, using the real observational constraints, not idealised
ones.** F266 reports the calibrated literature bounds directly: a naive single-flavour see-saw
mixing ($\sin^22\theta=2.8\times10^{-5}$) and non-resonant Dodelson–Widrow production for the full
dark-matter abundance are both X-ray excluded; **resonant production** (Shi–Fuller, driven by a
primordial lepton asymmetry — precisely the leptogenesis mechanism F341's argument S1 already
identified as load-bearing elsewhere in the model) reaches $\Omega_\text{DM}$ at a smaller,
X-ray-allowed mixing ($\sin^22\theta\sim5\times10^{-12}$) — the surviving $\nu$MSM window.

**What is and is not claimed, stated with the same discipline as F343.** The keV mass scale is a
free eigenvalue of $M_R$ (§16.2.7's node mechanism makes its *smallness* structural but does not
pin its *value*, and §16.2.6/F343 shows nothing in the model fixes $M_{R0}$ at all); the primordial
lepton asymmetry resonant production needs is likewise an input, not derived. **What the model
contributes beyond adopting the $\nu$MSM wholesale is that its dark-matter candidate costs no new
sector**: it is the same $\nu_R$ the hypercharge closure (F341) and the see-saw mechanism (F47)
already require to exist, with the same properties (total singlet, structurally forced $Y=0$)
doing double duty.

> **Scope boundary, stated explicitly per this chapter's assignment.** This chapter's job is the
> *identity* argument — why the model's own sterile neutrino is structurally suited to be the dark
> matter, and why it passes where the alternative failed. The relic-abundance calculation in full
> (the Boltzmann treatment beyond the order-of-magnitude parametrisation used here, the
> observational status of the X-ray and Lyman-$\alpha$ bounds, and this candidate's place among the
> model's other dark-sector findings) is Chapter 22's territory (`00-plan.md` lists "sterile
> neutrinos, the spin-2 mode, geons, relic abundances, falsifiers" as Ch.22's core question); this
> chapter does not duplicate that treatment.

## 16.3 Results table

| # | Result | Status | Source |
|---|---|---|---|
| R16.1 | Bare QCA Majorana step is exactly R-unitary (anti-linear, couples $\chi$ to $\chi^*$) | exact/machine ($2.25\times10^{-11}$) | F47 |
| R16.2 | Majorana step is $U(1)_Y$-invariant iff $Y_{\nu_R}=0$ — the Higgs-free realisation of the SM rule; completes the Ch.12 handoff's *mechanism* | exact (residual $0.0$) | F47 |
| R16.3 | See-saw scaling $\lvert\lambda_-\rvert=M_D^2/M_R(1+O((M_D/M_R)^2))$, verified against the lattice operator's own $8\times8$ Jacobian | exact/machine ($\le1.82\times10^{-12}$) | F47 |
| R16.4 | Dropping the Majorana row leaves the hypercharge system rank 5 (nullspace 2, $y_\phi$ free); restoring it uniquely closes the certified rank-6 line — **no-go for a symmetry-forbidden Dirac-only $\nu_R$; structural-consistency argument for Majorana** | exact ($\mathbb Q$) | F341 |
| R16.5 | 3×3 see-saw reduces exactly to three F47 copies | exact/machine ($<10^{-9}$) | F236 |
| R16.6 | **No-go:** $E_g$ texture on $M_D,M_R$ forces PMNS $=\mathbb1$ for every choice of inputs | exact ($<10^{-9}$ deg) | F236 |
| R16.7 | **No-go (group theory):** $(t_{xy},t_{yz},t_{zx})$ transform as three inequivalent 1-d irreps of $D_{2h}$ — no residual symmetry relates them | exact | F254 |
| R16.8 | **No-go:** F92 equipartition cannot select the $T_{2g}$ amplitudes — no degenerate multiplet | exact | F254 |
| R16.9 | **No-go, extended:** $D_{2h}$ transports a complex $T_{2g}$ amplitude by the identical real sign — the phase content is as unrelated as the magnitude | exact ($<10^{-10}$) | F353 |
| R16.10 | **No-go:** $\delta_{CP}$ is genuinely free by the identical mechanism as the PMNS angles | numerical (generic, unprotected) | F353 |
| R16.11 | **No-go:** no lattice-registered ratio's small integer power lands near the required $\sim10^{19}$ $M_R$ suppression | numerical (exhaustive scan) | F343 |
| R16.12 | **No-go:** $\nu_R$'s total-singlet status forecloses the model's only dynamical scale-generation mechanism (asymptotic freedom) | exact (source inspection) | F343 |
| R16.13 | Structural (not derived): a $Z_3$ cancellation node makes proximate eigenvalues parametrically light | exact algebra (node) / accommodated (value) | F201 |
| R16.14 | The F47 sterile $\nu_R$ is cosmologically stable at viable mixing, contrasted against the excluded $E_g$-mode alternative | computed | F266 |

## 16.4 Comparison with measurement

The see-saw mechanism (R16.1–R16.3) reproduces, qualitatively and by construction, the observed
smallness of the active-neutrino mass relative to the charged-fermion spectrum: a single large
scale $M_R$ (rather than an unnaturally tiny Yukawa coupling) is enough, and this is a genuine
structural improvement over simply asserting a small Yukawa, since the Standard Model with $\nu_R$
added by hand offers no comparable argument. **No absolute neutrino mass is predicted** (CL018):
KATRIN's direct kinematic mass bound, neutrinoless double-beta-decay half-life measurements
(current: KamLAND-Zen 2024, $T_{1/2}^{0\nu}>3.8\times10^{26}$ yr, $m_{\beta\beta}<28$–$122$ meV),
and cosmological sum-of-masses bounds are all measurements this chapter's mechanism is silent on —
a measured value fixes the model's free $M_R$, rather than testing it.

The 3×3 extension's mass-sector fit (§16.2.3) reproduces the observed light-neutrino mass-squared
splittings when six free parameters are allowed for five observables — a fit, not a prediction, by
the finding's own accounting, and F254 proves this parameter count is forced rather than an
artefact of a weak ansatz. The PMNS angles themselves (F236/F254 fit) numerically match NuFIT-5.2
to the fit's own tolerance ($\sim10^{-11}$ deg) precisely because they are fit parameters at that
precision — this is not evidence for the model beyond confirming the fit converges.

## 16.5 What was excluded, and why

**No lattice selector exists for the PMNS mixing angles (F254).** The argument is genuinely
group-theoretic, not merely an unsuccessful numerical search, and its structure is worth restating
in full since it is the sharpest no-go this chapter carries. The charged-lepton and neutrino mass
*textures* both live in the $E_g$ representation of the residual point-group action on the BCC
second-neighbour shell — the unique channel, per Chapter 15's own F93 O1 decomposition
$\mathrm{sym}(T_{1u}\otimes T_{1u})=A_{1g}\oplus E_g\oplus T_{2g}$, that splits the three generation
axes *without mixing them*. Any inter-generation mixing must therefore live in the orthogonal
$T_{2g}$ channel — the unique off-diagonal piece of the same decomposition. But the very act of
condensing in the $E_g$ channel at a generic angle (which the model's data require — $\delta^*$ is
not a special, high-symmetry point) breaks the point group's residual symmetry down to
$D_{2h}=\{\mathrm{diag}(\pm1,\pm1,\pm1)\}$, an abelian group with **no element that permutes the
three coordinate axes at all**. Under this residual group, each of the three $T_{2g}$ off-diagonal
amplitudes transforms in its own one-dimensional representation ($B_{1g}$, $B_{2g}$, $B_{3g}$ —
distinct because the three axis-pairs $\{xy,yz,zx\}$ pick up distinct sign patterns under the eight
group elements), and because one-dimensional irreducible representations of an abelian group are,
definitionally, inequivalent whenever their characters differ, no group element can map one
amplitude onto another. This forecloses not just an accidental numerical coincidence but the
entire *class* of arguments ("democracy," "equipartition," "a hidden residual $\mathbb Z_3$") that
elsewhere in this model's own tree (the charged-lepton condensate's own $\sqrt2$ amplitude, F92) has
successfully pinned a free-looking parameter. The equipartition mechanism specifically requires a
degenerate multiplet — several components related by an unbroken symmetry, so that "equal weight"
is a meaningful, symmetry-protected statement — and R16.7 shows there is no such multiplet here:
the $E_g$ condensate has already, and unavoidably, split what would have been a degenerate $T_{2g}$
triplet into three inequivalent pieces before any mixing dynamics is even considered. **The
conclusion is not "the model has not yet found the right selector" but "no selector of this
entire class can exist, given that the model's own charged-lepton/neutrino mass mechanism requires
condensing in $E_g$ at a generic angle."** F353 (§16.2.5, R16.9–R16.10) shows this same argument
transfers, unchanged in its mechanics, to the phase content of the amplitudes and hence to
$\delta_{CP}$.

**No mechanism fixes the absolute Majorana scale (F343).** Restated in full because, unlike F254's
theorem, this is a null result across three heterogeneous mechanisms rather than one unified
argument, and each leg fails for a structurally different reason. The lattice's one genuine UV
scale, the Planck-derived cutoff $\Lambda$, sits roughly 19 decades above any phenomenologically
reasonable $M_R$; nothing already registered in the model's own constants — not the charged-lepton
weight $2/9$, not the gravitational coupling $1/(72\pi)$, not any of the model's other closed-form
dimensionless ratios, raised to any small integer power — lands within better than $0.13$ dex of
that specific suppression, and the one near-hit found is explicitly flagged as an unadopted
coincidence rather than a link, following the model's own established standard for treating such
near-misses (cf. F332's `reciprocal_cube_coincidence`, cited by F343 itself). The $E_g/Z_3$
condensate, which *does* fix the neutrino mass texture's shape, is shown by direct symbolic
factorisation to leave the overall prefactor $M_{R0}$ completely untouched — the texture's defining
relation is linear in $M_{R0}$ with no $M_{R0}$-dependence anywhere else, so rescaling it rescales
every mass by the same factor and disturbs nothing else about the texture, which is the algebraic
signature of a genuinely free overall normalisation rather than a hidden constraint. And the one
dynamical mechanism the model has anywhere for generating a hierarchically small scale from a large
cutoff without fine-tuning — asymptotic-freedom running of a confining gauge coupling, the QCD
mechanism — is unavailable to $\nu_R$ specifically because $\nu_R$'s total gauge-singlet status
(itself required for the Majorana term to be gauge-invariant at all, R16.2) means it has no gauge
coupling of any kind for such a mechanism to act on. The three legs are independent: a future
finding could in principle close any one of them (a new registered ratio landing exactly on the
required suppression; a demonstration that the $E_g$ condensate secretly does constrain $M_{R0}$
through some channel not yet examined; a new gauge coupling attached to $\nu_R$) without touching
the other two, and F343 is explicit that none of the three legs is claimed to be a theorem
foreclosing all possible future mechanisms — only that none of the model's *current* structure
supplies one.

## 16.6 What is still open

1. **The absolute active-neutrino mass scale, and the absolute Majorana scale $M_{R0}$, are both
   genuinely free** (CL018, F343) — not merely unfitted but checked, on three independent legs for
   $M_{R0}$, to have no link anywhere in the model's current structure. $M_R$ now stands as the
   fifth named member of a cluster of unfixed absolute scales alongside $v$ (Ch.12), the quark
   masses, and $m_{E_g}$ (Ch.15) — a genuinely open problem for the model as a whole, not specific
   to the neutrino sector.
2. **The three PMNS mixing angles are proven free**, not merely unfitted (F254): a lattice
   derivation of them would require an explicit dynamical computation of three independent
   $T_{2g}$ condensation gaps, parallel to how the charged-lepton mass reduced to the $E_g$ Landau
   ratio (Ch.15) — no such computation exists, and F254's theorem shows no *symmetry* shortcut to
   one is available.
3. **The Dirac CP phase $\delta_{CP}$ is proven free by the identical mechanism** (F353) — the
   ledger closes this as `EXCLUDED` rather than `ABSENT`, meaning the question "does a lattice
   selector exist" is answered (no), not that the phase's actual value is somehow now predicted.
4. **Whether a genuinely dynamical (non-symmetry) mechanism could still fix the $T_{2g}$ gaps or
   the Majorana scale is explicitly not ruled out** by either F254/F353's group-theoretic no-go or
   F343's structural null result — both findings foreclose specific *classes* of mechanism
   (residual-symmetry selectors; the three named scale-anchoring candidates), not the possibility
   of a future first-principles dynamical computation.
5. **Whether the neutrino condensate angle $\delta_\nu$ shares any deeper relationship with the
   charged-lepton angle $\delta^*=2/9$** (Ch.15's weight-as-phase result) beyond sharing the same
   texture *form* is not examined by any assigned finding — F201/F236 treat $\delta_\nu$ as the
   neutrino sector's own independent free parameter throughout.

## 16.7 Falsifiers

- **CL018** (F47): no falsifier is stated, and this is itself the point — a measured absolute
  neutrino mass fixes the model's free $M_R$ rather than testing it. KATRIN, $0\nu\beta\beta$, and
  cosmological mass-sum bounds are all, by the card's own statement, silent on this claim.
- **CL290** (F341, `contingent`): a **structural falsifier** — discovery, anywhere in the model's
  own construction (not added by hand), of a global or gauged symmetry under which $\nu_R$ carries
  a nonzero charge independent of $Y$ would remove the "no protecting symmetry" leg and could
  reopen a Dirac-only possibility. An **empirical falsifier**, external to the model's internal
  argument: neutrinos shown to be Dirac via a lepton-number-conserving discriminator with no viable
  Majorana loophole (this does not bear on F341's internal-consistency argument, which is about
  this model's own structure, not a general Dirac-vs-Majorana theorem). The claim is explicitly
  `contingent` on F165/F279 continuing to stand.
- **CL207/CL223/CL294** (F236/F254/F353): `falsifier: unset` on all three cards — declared debt in
  the claims registry, not a claim that no falsifier exists. Informally, per F254/F353's own text: a
  future lattice derivation of PMNS or $\delta_{CP}$ that returns the mixing amplitudes *equal*
  (democratic) or fixed by any single symmetry parameter would contradict the data and is already
  shown incapable of reaching it (F254 T3); a future *dynamical* (non-symmetry) mechanism fixing the
  $T_{2g}$ gaps would not contradict either no-go (both are scoped to symmetry-selector mechanisms)
  but would make the "genuinely free" framing incomplete rather than wrong.
- **CL175** (F201): `falsifier: unset`. Informally: the node mechanism predicts that the lightest
  sterile mass and the charged-lepton hierarchy share a common structural origin (proximity to a
  $Z_3$ cancellation node); this is not independently testable without also fixing $M_{R0}$, which
  the model does not do.
- **CL232** (F266, `live`): `falsifier: unset` on the card, but the finding's own text is explicit
  that the surviving $\nu$MSM resonant-production window is narrow and an active observational
  target (X-ray line searches, Lyman-$\alpha$ and Milky-Way-satellite constraints) — this is a
  genuinely falsifiable candidate, not a free one, even though its keV mass scale is itself an
  accommodated input. Full falsifier treatment is Chapter 22's territory.
- **CL291** (F343, `live`): explicitly **not** a claim that $M_R$ is provably unfixable in any
  future extension. Three named developments would void one leg without new observation: a new
  gauge coupling for $\nu_R$ (voids leg 3); a general solution to the $v$/quark-mass/$m_{E_g}$
  scale-anchoring cluster (would need re-checking against $M_R$); a dedicated $M_D$/$M_R$
  prefactor-sharing argument (not attempted). The Leg-1 numerical near-coincidence
  ($(1/(72\pi))^8$) is explicitly *not* a falsifier candidate — flagged, not adopted.

---

## Notation established in this chapter

*Harvested into the whole-monograph glossary at Appendix A5. Extends Chapters 1, 12 and 15's
notation; nothing here is redefined.*

| Symbol | Meaning | First used / fixed here |
|---|---|---|
| $\nu_R$ | The right-handed neutrino: a total Standard-Model gauge singlet ($Y_{\nu_R}=0$, structurally forced), the field this entire chapter's mass mechanism acts on. | §16.2.1 (F47) |
| $M_D$ | The Dirac mass coupling $\eta_L$ (the lepton doublet) to $\nu_R$, via the same F27/F41 chiral-$SU(2)$/hypercharge mass step as every other fermion. | §16.2.1 (F47) |
| $M_R$ (single-flavour), $M_{R0}$ (3×3 overall scale) | The bare Majorana mass on $\nu_R$; in the 3×3 extension, the overall prefactor of the $E_g/Z_3$ texture — proven (F343) to be fixed by nothing in the model. | §16.2.1 (F47); §16.2.3/§16.2.6 (F236/F343) |
| $\delta_\nu$ | The neutrino sector's own $E_g$ condensate angle — argued to share the charged-lepton texture's *form* but not its *value* with $\delta^*$ (Ch.15). | §16.2.3 (F236/F201) |
| $t_{xy},t_{yz},t_{zx}$ | The three second-shell $T_{2g}$ (axis-mixing) amplitudes; proven (F254) to transform as three inequivalent 1-d irreps of the residual stabilizer $D_{2h}$, hence genuinely free. | §16.2.3–§16.2.4 (F236/F254) |
| $D_{2h}$ | The residual point-group stabilizer of a generic-angle $E_g$ condensate (order 8, no axis permutations); inherited from Chapter 15's F93 O3. | §16.2.4 (F254, citing Ch.15) |
| $J$ | The rephasing-invariant Jarlskog combination, $J=\mathrm{Im}(U_{e1}U_{\mu2}U_{e2}^*U_{\mu1}^*)$, used to extract $\delta_{CP}$ basis-independently from the $T_{2g}$ phases. | §16.2.5 (F353) |
