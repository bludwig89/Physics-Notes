# Chapter 9 — Electromagnetism

*Chapter 9 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F68-minimal-coupling-forces-even-photon.md`, `findings/F87-charge-coupling-paired-photon.md`,
`findings/F127-alpha-em-derivation-four-avenue-nogo.md`, `findings/F339-alpha-em-nogo-reopening-conditions.md`,
`findings/F349-alpha-em-induced-stiffness-convergent-evidence.md`, `findings/F384-conserved-bcc-em-current.md`,
`findings/F385-u1-link-covariant-step.md`, `findings/F386-a-field-convention.md` (the eight findings
`00-plan.md` §2 assigns to this chapter, all read in full), checked directly against
`docs/theory/supersessions.yaml` (grepped for all eight finding numbers — F68/F87 appear only in S1's
and S2's narrative text, never as a `superseded:` entry for either; no record names F127/F339/F349/
F384/F385/F386 at all) and against `claims-index.md`: **CL002** (F68, among others, `live`, `exact`,
the photon-is-a-bound-pair headline), **CL271** (F68, `live`, `exact`, the colour-structure derivation
— not otherwise this chapter's territory), **CL113** (F127/F339/F349, `live`, `no_go`, `quantitative`,
`falsifier: none`), **CL082** (F87, `withdrawn` — investigated in full in §3.2/§6 below), **CL307**
(F385, among others, `narrowed`, Chapter 10's own card, cited forward only). Notation, postulates and
results are those of Chapters 1, 6 and 8 (`01-postulates-and-ontology.md`,
`06-free-propagation-light-cone.md`, `08-the-photon.md`) — $\mathbf k$, $\Omega_\text{pair}(\mathbf k)$,
$\hat{\mathbf n}(\mathbf k)$, $c_\text{lat}$, R8.1–R8.16 — extended, never redefined. F384–F386 are
2026-09-14 findings, the opening moves of the still-open photon↔fermion investigation
(`docs/roadmaps/photon-fermion-coupling.md`, Stages 1–3); F387 onward (Stage 4/5, the coupled dynamics)
is **not** read or cited here — it is Chapter 10's assignment, per `00-plan.md` §4/§8, and this chapter
deliberately stops at the boundary those stages open.

## 9.0 What this chapter establishes

This chapter builds the actual $U(1)_\text{EM}$ gauge theory on the BCC Weyl walk: the current the walk
itself conserves (F384), the covariant per-link step that couples that current to the paired photon of
Chapter 8 and the fork-adjudicated unitarity/momentum-transfer tension that step carries (F385), the
vector-potential convention that hands the covariant step a field to read (F386), and the two independent
forcing arguments — one from 2026-06 (F68), one from Chapter 8 (R8.3/F91) — that show minimal coupling
itself, not a modelling choice, is what selects the even, non-birefringent, paired channel as the photon
that couples to electric charge. It also states, without softening, the model's own four-avenue no-go on
deriving the coupling's *magnitude* — $\alpha_\text{em}$ — from the lattice rule (F127), characterizes
precisely what would have to be true to reopen each avenue (F339), and reports a second, independent,
non-perturbative evidence line that corroborates two of the four closures (F349). The chapter's honest
center of gravity is the seam between these two halves: everything about the current, the coupling
channel, and the coupling's *form* is settled and exact or machine-precision; the coupling's *magnitude*
is not derived at all, at any avenue tried, and the model consumes it as a free external input from this
chapter forward. Chapter 10 picks up exactly where this chapter's settled half ends — coupling this
current to the photon's own dynamics — and that is a live research report, not resolved here.

## 9.1 Inputs

**Postulates used.** **P4** (exact unitarity, $\mathcal U=e^{-iH}$) underwrites every exactness claim in
this chapter the same way it underwrote Chapter 8's: the current-conservation identity (F384), the
per-link step's unitary special cases (F385), and the vector-potential solve (F386) are all statements
about the spectral and unitary structure of the one-tick BCC Weyl walk, not approximations to it. **P5**
(the primitive field is $\psi\in\mathbb C^2$) is what the current and the covariant step are built *on* —
$\rho=q(|f|^2+|g|^2)$ and the per-link Peierls phases act directly on the Weyl 2-spinor, with no Dirac
mass step required anywhere in this chapter (F384 §6, F385 §7: "only the Weyl 2-spinor case is covered
… the massive Dirac case is not addressed"). **P6** (the chiral $SU(2)$ connection $U(x)$ carrying
hypercharge) is the background structural fact this chapter's U(1) coupling sits inside, not something
it re-derives: the electric-charge U(1) this chapter builds a current and a covariant step for is,
after electroweak mixing, the unbroken combination of the hypercharge phase P6 puts on $U(x)$ and the
$SU(2)_L$ Cartan direction — and F41's structural premise (cited via F349 §4) is explicit that
$U(1)_Y$ "has no independent lattice kinetic term at all — it rides on $U(x)$ as a Stueckelberg phase,"
consistent with treating the scalar Peierls phase $P=e^{i\theta}\mathbb I_2$ this chapter's whole
construction is built from (F68) as *the* concrete lattice realization of that connection's abelian
piece, not a separate ad hoc addition. This chapter does not re-derive the electroweak mixing that
produces $Q=T_3+Y/2$ from $U(x)$ — that is Chapter 12's job — and works throughout with the
already-identified U(1) charge-coupling channel Chapter 8 (via F68) already isolated.

**Prior results used, precisely.** **R8.3** (Ch.8, F91) is the central prior result: the pairing-
classification theorem, "a scalar $\propto\mathbb I$ branch operator forces the even (paired) channel;
a projector $P_L$ forces the chiral (single-branch) channel," with the photon's row derived from
$Q_L=Q_R$ exactly over $\mathbb Q$. This chapter's §9.2.1 (F68) is read *alongside* R8.3, not as a
re-derivation of it — see the precise relationship stated there. **R8.4/R8.5** (F69, the paired photon
and its non-birefringence) is the field this chapter's current and covariant step couple to; nothing
about its dispersion or masslessness is revisited here. **R8.9** (F250, the all-$k$ gauge pole and the
transverse Ward identity $[M_6,P_T\otimes\mathbb I_2]=0$) is the gauge structure F386's Coulomb-gauge
solve for $\mathbf A$ builds on directly (§9.2.5). **R8.1/R8.2** (F37, the Riemann–Silberstein branch
assignment) underlies the curl-symbol machinery (`bcc_curl_symbol`, `C(\mathbf k)$) every result in this
chapter — F384's current, F385's Ward-identity checks, F386's solve — reuses without re-deriving.

**Free inputs consumed, stated precisely — this is the chapter's most consequential honesty point.**

1. **The electric charge magnitude, equivalently $\alpha_\text{em}=e^2/4\pi\hbar c$, is a free external
   input at this stage of the model, not a derived quantity.** Every coupling *ratio* adjacent to it is
   derived elsewhere in the project — $\sin^2\theta_W=1/4$ bare from $\sigma\leftrightarrow\tau$-swap
   geometry (F45), $g_s^2\chi=1/4$ from rotor stiffness (F115-CM3), the full electroweak family from one
   parameter (F115-CM1) — but the *overall scale* that fixes $e$ itself is not. §9.5 states the no-go in
   full; the practical consequence for the rest of the monograph is that wherever a chapter needs a
   numerical value of $\alpha_\text{em}$ (most directly Chapter 23's QED precision battery — F249's
   comparison battery, F252's $a_e$ and Lamb shift, F261's two-loop $a_e$/$a_\mu$, F334's hadronic vacuum
   polarization estimate — all of which run the model's QED machinery *at* the measured CODATA value)
   that value is read in from measurement, not produced by the lattice rule. This chapter is the point
   in the dependency chain where that fact first becomes load-bearing, and it is recorded here rather
   than left implicit in a later chapter's numerics.
2. **The identity-channel Peierls phase $P=e^{i\theta}\mathbb I_2$ is the coupling *form* minimal coupling
   forces (F68/R8.3); it is not itself derived from a still-deeper principle** — it is the lattice
   realization of "gauge the phase ambiguity already present in the spinor representation," the same
   move P6 makes for the $SU(2)$ mass connection, applied here to the abelian piece. Nothing in this
   chapter's sources offers an argument that this specific coupling mechanism, rather than some other
   way of attaching a U(1) charge to a lattice fermion, is *the* one nature uses — it is adopted because
   it is the construction under which the rest of this chapter's algebra (current conservation, the
   Aharonov–Bohm loop, the covariant step) closes exactly.
3. **The per-link covariant step's exact unitarity is available only for curl-free (uniform or
   spatial-gradient) $\mathbf A$** (F385 §5b); for the genuinely curl-carrying part of the field — the
   part this chapter's whole photon-coupling machinery exists to handle — no construction tested closes
   both unitarity and momentum transfer simultaneously at general field strength (§9.2.4). This is not a
   free input in the same sense as items 1–2; it is a genuine, disclosed open construction gap, carried
   forward explicitly rather than smoothed into "solved."
4. **Nothing else is free.** The current (F384), the Ward identities (F385/F386), and the Coulomb-gauge
   solve (F386) are closed-form consequences of the walk's own unitary and the already-existing
   `bcc_curl_symbol`, introducing no additional fitted constant.

## 9.2 The derivation

### 9.2.1 Two independent forcing arguments for the same channel: F68 and R8.3, related precisely (F68)

Chapter 8 (R8.3, F91, 2026-06-04) derived a four-sector pairing-classification theorem: a coupling
operator that is a scalar $\propto\mathbb I$ in branch space forces the even (paired) propagation
channel, while a projector $P_L$ forces the chiral (single-branch) channel, with the photon's row
following from $Q_L=Q_R$ exactly over $\mathbb Q$. **F68 (2026-06-01) is not a re-derivation of R8.3
after the fact — it is the earlier, narrower result R8.3 itself credits as its seed.** F91's own text,
already quoted in Chapter 8 (§8.2.2), states this precisely: the photon's forcing argument is "exactly
the F68 minimal-coupling argument Chapters 6/9 already lean on, here **promoted** from a single-sector
observation to one leg of a four-sector theorem." The relationship is genetic, not parallel-and-
redundant: F68 supplied the single-sector commutator computation; F91 generalized its structure into a
branch-operator classification covering $\gamma$, $W^\pm$, $Z$, and the gluon at once.

**What F68 derives, concretely, that R8.3's table does not itself restate.** In this model the U(1)
connection enters the fermion update only as a scalar Peierls phase proportional to the identity in
Weyl-spinor space — verified directly on the model's *own* operators, not asserted abstractly:

- The complex-mass U(1) step (`mass_step_1flavor_u1`) carries the off-diagonal block $i\,s_m\,e^{i\theta}
  \mathbf I$; the hypercharge step (`ca_hypercharge`) carries $e^{i\alpha(x)Y/2}\mathbf I$ per chirality.
  So the coupling operator is $P=e^{i\theta}\mathbf I_2$, and the Weyl QCA unitary is $U^\pm(\mathbf
  k)=u\,\mathbf I-i(\mathbf n\cdot\boldsymbol\sigma)$ (Ch.6's R6.1-family object).

$$\boxed{\;[P,U^\pm(\mathbf k)]=0\ \text{for every }\mathbf k\ (\text{residual }1.1\times10^{-16}\text{ over 4000 random }\mathbf k\times\text{both branches})\;\Longrightarrow\;P\psi^\pm=e^{i\theta}\psi^\pm,\ \text{identical on both helicities}\;}\tag{R9.1}$$

(F68, T1, machine $1.1\times10^{-16}$; confirmed exactly, residual $0.0$, on the real U(1) mass step,
T2.) An identity coupling can source only the helicity-symmetric dispersion — the even law — because
it advances both Riemann–Silberstein eigenstates by the same phase; this is the non-birefringence
mechanism stated at the single-operator level, before R8.3's later four-sector table existed to name it.
**F68's second, independent contribution** is the explicit contrast with the composite bilinear photon
(Ch.8 §8.5, F39): the bilinear's field operator is $\sigma^i$, and $\sigma^i$ does **not** commute with
$\mathbf n\cdot\boldsymbol\sigma$ ($\lVert[\sigma_x,\mathbf n\cdot\boldsymbol\sigma]\rVert=1.99$, structural),
so the composite channel couples to the branch splitting and carries genuine birefringence
($1.03\times10^{-2}$ at $k=0.4$ on the body diagonal, T3). **This is the conceptual seed of R8.3's whole
$(g_L,g_R)$ classification framework**: F68 is the first place in the project's record that the identity
channel and the $\sigma$-vector channel are shown to be *different representations of the same lattice
$SU(2)$*, with birefringence living entirely in the one the U(1) coupling structurally cannot reach.

$$\boxed{\;\text{the U(1)-coupled photon and the composite }\sigma\text{-bilinear photon are two channels of one }SU(2)\text{; minimal coupling selects the identity channel, forced}\;}\tag{R9.2}$$

(F68, exact/structural/machine, 5 checks; test `test_F68_minimal_coupling_forces_even_photon.py`.) This
chapter therefore does not re-derive R8.3 — it cites it, per the assignment's own instruction — but it
does derive, independently and from the real U(1) mass-step and hypercharge operators rather than from
the abstract $(g_L,g_R)$ table, the specific claim that *this* chapter's electric-charge coupling is the
forced channel. The two results are convergent, not duplicative: R8.3 is the general theorem; R9.1/R9.2
is the concrete, operator-level instance for the specific charge this chapter builds a current and a
covariant step for.

### 9.2.2 The earlier end-to-end certification, and its withdrawn claim card investigated (F87)

Before the 2026-09 current/covariant-step programme (F384–F386, §9.2.3–9.2.5), the project already built
and verified a first-generation charge-coupling loop directly on the F69 paired photon, three days after
F91 (2026-06-03). F87 rebuilt the Aharonov–Bohm holonomy and the sourced Maxwell curl on the even-law
$(\mathbf E,\mathbf B)$ field after the old Standard-Model-style gauge step was removed in Phase E1, and
closed them into one loop:

- **Aharonov–Bohm (a charge *reads* the field).** The ordered product of Peierls link phases around a
  closed loop is the discrete Stokes theorem, $W(\partial S)=\exp(iq\Phi_\text{enc})$, exact on the
  lattice (AB2, $1.1\times10^{-16}$); a charged fermion encircling a flux tube picks up the phase even on
  a field-free path (AB3), identically for either helicity (AB4, $3.3\times10^{-16}$, the same
  helicity-blindness R9.1 establishes), and linearly in $q$ (AB5, exact, $0.0$).
- **Sourced Maxwell curl (a charge *sources* the field).** With $C(\mathbf k)=2\mathbf n(\mathbf k/2)$ the
  paired photon's curl generator, $C\cdot(C\times\mathbf x)\equiv0$ (MX2, machine $5.3\times10^{-16}$)
  means the curl term never sources charge, so the Gauss constraint $iC\cdot\mathbf E=\rho$ is preserved
  under continuity — charge conservation, to machine precision, on the paired photon's own propagator
  (MX3, $2.0\times10^{-12}$ over 100 sourced ticks).
- **End-to-end.** A compact interior flux tube sourced by its own Ampère wall current gives a solved
  Coulomb-gauge $A$ whose holonomy equals $q\times$ the enclosed flux, both ways, to machine precision.

$$\boxed{\;\text{the identity-channel Peierls coupling reads a flux via a helicity-blind holonomy and sources a field while conserving charge, both to machine precision, on the paired photon}\;}\tag{R9.3}$$

(F87, 20/20 PASS; test `test_F87_charge_coupling_paired_photon.py`.) F87's own text is explicit about
scope: this is the *Abelian* coupling path only, verified as an operator/transport phase, not a
scattering amplitude, and it uses `ca_maxwell.maxwell_curl_residual`'s eigen-mode curl symbol directly
rather than deriving a current from the walk's own continuity equation the way F384 later does (§9.2.3)
— F384's own caveat states plainly that "F29/F65-F69/F87 and the SU(2)/SU(3) analogues never checked
their bilinear currents against exact discrete continuity, so this finding does not retroactively call
any of them into question." F87 is therefore **not superseded in substance** by F384–F386: it remains a
valid, still-cited self-consistency certification of the charge-coupling loop's machinery
(`bcc_curl_symbol`, the Gauss/Ampère apparatus), which F384–F386 reuse directly rather than replace.

**The `withdrawn` status of CL082 (F87's claim card), investigated.** `claims-index.md` lists **CL082**
as `status: withdrawn`. Reading the card directly (`docs/claims/CL082-...md`) shows the same mechanical
pattern Chapters 7 and 8 already found for CL029/F15 and CL084/F89, CL251/F306: the card's own `##
Status & history` section states the withdrawal was inferred because "**a supersession/withdrawal
banner appears in this finding's header**," and then quotes the supposed banner verbatim — which reads
"Confirmed — 20/20 PASS. **Numbering:** built after the concurrent colour-dielectric finding had already
taken F86 → this is **F87**." **This is not a supersession or withdrawal banner; it is F87's own
`**Status:**` line, reporting a full pass and a routine finding-number collision note.** F87 does not
appear in any of `supersessions.yaml`'s 23 records as a `superseded:` entry; the two mentions of its
result artifact under **S1** (§5 above) are both explicitly float-floor/undeclared-input drift-tracking
notes ("the CAUSE is float-floor churn, not S1's photon supersession... Not a regression and not a
physics change," `supersessions.yaml` S1), never a claim that F87's physics is wrong or retired. This is
the identical claims-layer bookkeeping artifact this monograph has now found four times (F15/CL029,
F89/CL084, F306/CL251, F87/CL082) — most likely a mechanical, prose-scraping seeding pass that
mis-detects ordinary status prose (a "confirmed" line, a numbering aside, a "supersedes the
interpretation of" cross-reference) as a withdrawal signal. **Unlike F89's case (Ch.8 §8.2.12), there is
no substantive correction owed to F87's own content here** — its result stands exactly as reported, and
this chapter treats R9.3 as live, cited alongside F384–F386 as the earlier-but-still-valid half of the
same charge-coupling story.

### 9.2.3 The conserved current the walk actually carries (F384)

F87 and the project's other bilinear currents (the SU(2) isospin current, the SU(3) colour current) all
use the naive pattern $J^i=q\psi^\dagger\sigma^i\psi$ by analogy with a continuum or tight-binding
current, never checked against the walk's own exact discrete continuity equation. F384 (2026-09-14, Stage
1 of `docs/roadmaps/photon-fermion-coupling.md`) performs that check and derives the current the BCC
Weyl walk actually conserves, rather than the one analogy suggests.

$\rho(\mathbf x)=q(|f(\mathbf x)|^2+|g(\mathbf x)|^2)$ needs no derivation — it is exactly what
`weyl_step_3d_bcc`'s unitarity conserves in total, any $f,g$, to machine precision. The naive current
fails, and for a structural reason specific to this lattice, not a coefficient error: the BCC walk's hop
is a *fractional* lattice shift ($\mathbf d/\sqrt3$, not an integer `np.roll`), so its real-space kernel
is not compactly supported, and no local nearest-neighbour bilinear can be exact by construction the way
one can for an ordinary tight-binding hop. What **is** exact is the Fourier-space continuity relation
itself: $\rho(t{+}1,\mathbf x)-\rho(t,\mathbf x)$ and $\mathbf J(\mathbf x)$ are two real-space fields
whose divergence relation holds mode-by-mode, regardless of how either was produced, so the walk's own
one-tick $\rho$-difference (computed from a real tick, not an approximation) fixes a one-equation-per-mode
linear system with a unique **minimal** (purely $\hat{\mathbf C}(\mathbf k)$-longitudinal) solution:

$$\boxed{\;\tilde{\mathbf J}(\mathbf k)=i\,\hat{\mathbf C}(\mathbf k)\,\frac{\tilde\rho(t{+}1,\mathbf k)-\tilde\rho(t,\mathbf k)}{|\mathbf C(\mathbf k)|}\ \ (\mathbf k\neq0,\ \tilde{\mathbf J}(0)=0)\;}\tag{R9.4}$$

(F384, `construction_closes`, masked residual $3.1\times10^{-17}$; the naive current is worse by
$\sim5\times10^{15}\times$ on the same packet, `naive_current_much_worse`, both legs post-review-fixed to
compare against the derived current's own masked residual rather than its raw one.) **Two honest
qualifications, stated in the finding and carried here rather than smoothed away.** First, a genuine,
disclosed structural gap: at the 7 non-origin Nyquist-corner modes where $C(\mathbf k)=0$ exactly (the
symmetrisation that forces $C(-\mathbf k)=-C(\mathbf k)$ for any real-field curl symbol), no current of
any kind can source or drain that mode — `conserved_current` returns this leftover explicitly rather than
masking it, and the gate-tier check is scoped to the modes where a solution exists at all. Second, this
current is **not unique**: continuity fixes only the projection of $\tilde{\mathbf J}(\mathbf k)$ along
$\hat{\mathbf C}(\mathbf k)$; the transverse part is free gauge content, and F384 is explicit that "any
Stage 2–5 use of this current should not assume its transverse structure carries physical content." Only
the Weyl 2-spinor case is covered; the massive Dirac case is untouched.

$$\boxed{\;\rho\ \text{is the walk's own conserved density, exactly; }\mathbf J\ \text{is the minimal, purely longitudinal-in-}\hat{\mathbf C}(\mathbf k)\text{ solution to the walk's own exact discrete continuity equation}\;}\tag{R9.5}$$

(F384, 4/4 legs PASS, one declared control verified red exactly where declared, `can-fail` verified;
test record `F384-conserved-em-current`, gate tier.) **This finding carries no claim card by design**
— per D12's bar ("extends established physics," not "is interesting"), F384 states directly: "this is
an engine-capability addition... rather than a claim about what the model predicts or shows against
established physics; no `docs/claims/` card is issued." This chapter reads that as deliberate scoping,
consistent with what F384's own `**Status:**`/`**Checked:**` lines report: Confirmed, 4/4 legs PASS,
independently cold-re-derived and adversarially reviewed to **CONFIRMED-NARROWER** — a settled result,
not a provisional one, even though it issues no claim.

### 9.2.4 The per-link covariant step, and its unitarity/momentum-transfer fork adjudication (F385)

F384 gives the fermion→field half (a current the walk conserves); it says nothing about the field acting
back on the fermion with a directional force. The model's only pre-existing field→fermion U(1) path
(`minimal_coupling.u1_wrap_weyl_step_3d_bcc`) is *momentum-blind*: it multiplies $\psi$ by one common
site phase before and after an unbiased kinetic step, and a common factor cannot bias the hop amplitude
in one direction over its opposite. F385 (2026-09-14, Stage 2) supplies the missing directional handle —
a per-link construction, the U(1) analogue of the model's existing $SU(2)$ covariant step — and
adjudicates the tension its own docstring precedent (`weak_wmu.covariant_weyl_step_3d_bcc_exact`) already
flags: the analogous $SU(2)$ sum is unitary only when every link is the identity.

Decomposing the BCC unitary as $U_\text{BCC}(\mathbf k)=\sum_{\mathbf d}M_{\mathbf d}\,e^{i\mathbf
k\cdot\mathbf d/\sqrt3}$ (already in the codebase), the new construction attaches a *separate* Peierls
phase to each of the 8 fractional hop directions individually:

$$\boxed{\;\psi'(\mathbf x)=\sum_{\mathbf d}U_{\mathbf d}(\mathbf x)\big[M_{\mathbf d}\cdot\text{shift}_{\mathbf d/\sqrt3}\psi\big](\mathbf x),\qquad U_{\mathbf d}(\mathbf x)=e^{iq\mathbf A(\mathbf x)\cdot\mathbf d/\sqrt3}\;}\tag{R9.6}$$

(F385, `u1_link_weyl_step_3d_bcc`; reduces exactly to the free step at $\mathbf A\equiv0$, residual
$0.0$, all forks tested.) **For a spatially uniform $\mathbf A_0$, this collapses exactly to a rigid
momentum shift** — $\sum_{\mathbf d}M_{\mathbf d}e^{i(\mathbf k+q\mathbf A_0)\cdot\mathbf d/\sqrt3}=
U_\text{BCC}(\mathbf k+q\mathbf A_0)$, unitary for every argument because $U_\text{BCC}$ is (verified
bit-for-bit, $3.5\times10^{-15}$) — the lattice form of the continuum canonical shift $p\to p-qA$. The
tension is strictly a property of **non-uniform** $\mathbf A$: the primary construction (fork a) trades
norm conservation for momentum transfer, at a measured $O(|qA|\cdot a)$ rate (log-log slope $0.996$ over
a 16$\times$ amplitude sweep) — a genuine secular force, distinguished directly from a one-tick phase-
mixing artifact by an accumulating (not oscillating) momentum shift against a held-static field over ten
ticks (§9.2.4's decisive check, F385 §5). Two alternative constructions were adjudicated against it and
narrowed, not merely proposed:

- **Strang-split (fork b).** Halves the phase between source and destination site; reduces the drift
  *coefficient* by $\sim31\%$ but **does not change the power law** — the slope stays $\approx0.998$, not
  the hoped-for $O(a^2)$.
- **Per-site polar renormalisation (fork d).** Exactly norm-conserving by construction (machine,
  $2.2\times10^{-16}$, any $\mathbf A$) and carries a momentum kick of the *same order of magnitude* as
  fork (a) at the gate's tested width ($\sigma=3$) — but this does **not generalise**: the ratio
  `mag_d/mag_a` grows unboundedly with field width, from $1.17\times$ at $\sigma=1$ to $200\times$ at
  $\sigma=50$ on the same lattice, so "comparable to fork (a)" is a property of localised fields
  specifically, narrowed after independent review, not a general equivalence.

$$\boxed{\;\text{for curl-free (uniform/gradient) }\mathbf A,\text{ exact unitary momentum transfer is already available (}\S3\text{'s rigid shift and the pre-existing Bloch-acceleration mechanism); the per-link construction's unitarity/momentum-transfer tension is strictly a property of the curl-}\textit{carrying}\text{ part of }\mathbf A\;}\tag{R9.7}$$

(F385, 10/10 legs PASS, one declared control verified red exactly where declared, `can-fail` verified;
test record `F385-u1-link-covariant-step`, gate tier.) This is the sharpest scoping result in this
chapter's derivation: it is not that the model cannot couple the photon to the fermion at all — the
curl-free case is exactly solved, twice over, by independent mechanisms — it is that the genuinely new
physics a photon *beam* would carry (its transverse, curl-carrying content) is exactly the part no
construction tested here handles both exactly and at unbounded field strength. Only the Weyl 2-spinor
case is covered; Stage 3 (below) supplies no dynamical $\mathbf A$ of its own — every field used in F385
is a hand-built test bump.

### 9.2.5 The vector-potential convention (F386)

F385's covariant step needs an $\mathbf A$ to attach its per-link phases to; the photon channel itself
carries $(\mathbf E,\mathbf B)$, not $\mathbf A$ directly. F386 (2026-09-14, Stage 3) decides, and
verifies, between two candidates the roadmap named: **accumulate** ($\mathbf A\leftarrow\mathbf A+
\mathbf E$ per tick, the pattern already used for the $W$ field) and **solve** (a Coulomb-gauge
$\mathbf A$ read off $\mathbf B$ each tick, with no accumulator state).

$$\boxed{\;\mathbf A(\mathbf k)=i\,\frac{\mathbf C(\mathbf k)\times\mathbf B_T(\mathbf k)}{|\mathbf C(\mathbf k)|^2}\;}\tag{R9.8}$$

(F386, `solve_A_coulomb_3d`; reuses `bcc_curl_symbol`, the same curl operator Stage 1's current and
F87's Gauss/Ampère machinery already use — no new curl construction. Manifestly $\mathbf C$-transverse
by construction, `solve_is_purely_transverse`, $1.17\times10^{-16}$; recovers $\mathbf B$'s own
transverse part to FFT round-off, `solve_curl_recovers_B`, $2.35\times10^{-14}$.) **The decisive argument
for `solve` over `accumulate` is structural, not aesthetic.** F384's own current is *defined* as purely
$\hat{\mathbf C}(\mathbf k)$-longitudinal (R9.5) — so any `em_photon` channel sourcing $\mathbf E$ from
that current and then accumulating $\mathbf A\leftarrow\mathbf A+\mathbf E$ inherits that longitudinal
content directly, every tick, with no mechanism to separate it from genuine transverse photon content.
Measured directly: a pure-charge-source scenario (no real photon seeded) leaves `accumulate`'s
$\mathbf A$ **entirely** longitudinal, fraction $1.000000$ (`accumulate_inherits_longitudinal_content`),
while `solve` correctly returns $\mathbf A\approx0$ (`solve_gives_zero_A_for_pure_charge_source`, norm
$1.89\times10^{-33}$) — not because $\mathbf B$ stays zero in that scenario (it does not, for a subtle
reason traced in review, §9.6 below), but because `solve` reads only $\mathbf B$'s own genuine
$\mathbf C$-transverse projection, which is exactly zero there. The inertness of the purely-longitudinal
sector is confirmed independently by reusing F385's own Ward-identity machinery (a pure gradient
$\mathbf A=\nabla\chi$ produces only the already-disclosed $O(a)$ local-Ward defect F385 measured for a
general $\mathbf A$, not a new force channel).

$$\boxed{\;\text{Stage 3 adopts }\texttt{solve}\text{: a pure function of }\mathbf B\text{ that structurally discards exactly the longitudinal content }\texttt{accumulate}\text{ cannot avoid inheriting from F384's own current}\;}\tag{R9.9}$$

(F386, 7/7 legs PASS, one declared control verified red exactly where declared, `can-fail` verified;
test record `F386-a-field-convention`, gate tier.) Only the Weyl 2-spinor/U(1) case is covered, matching
F384/F385's scope; F386 does not build the coupled `em_photon`/`fermion_em` channel pair itself (Stage
4) or run the closed-loop momentum-transfer scenario (Stage 5) — that hand-off is stated in full in §9.7.

## 9.3 The $\alpha_\text{em}$ no-go, in full

### 9.3.1 The original four-avenue no-go (F127)

$\alpha_\text{em}\approx1/137.036$ is, as of this chapter, the model's **last irreducible dimensionless
input**. Every coupling ratio adjacent to it is already derived — $\sin^2\theta_W=1/4$ bare (F45),
$g_s^2\chi=1/4$ (F115-CM3), the electroweak family from one parameter (F115-CM1) — but four independent
routes to deriving $\alpha_\text{em}$'s own magnitude from the lattice rule were tried, and all four
report a sharp or inconclusive negative:

| Avenue | Verdict | Reason |
|---|---|---|
| **A** — Sakharov-style induced coupling | sharp negative | The U(1) Ward identity $\Pi^{\mu\nu}(0)=0$ blocks the mechanism that generates $G$ for gravity (there the conformal anomaly, $T^\mu_{\ \mu}=0$, forces zero tree stiffness; electromagnetism has no analogous anomaly to exploit) |
| **B** — an $O(1)$ lattice scale near the EW matching point | sharp negative | $\mu_\star/E_\text{lat}\sim10^{-15}$; no $O(1)$ lattice-scale coincidence near the matching scale |
| **C** — topology fixes the coupling | sharp negative | Anomaly cancellation and compactness fix the charge *spectrum* $\{0,\pm\tfrac13,\pm\tfrac23,\pm1\}$, not the *magnitude* $\lvert e\rvert$ |
| **D** — structural/impedance normalization | inconclusive | $Z=1$, $c_\text{lat}=1/\sqrt3$, and the curl normalization are all structural, but the Peierls coupling $q$ is independent of all of them — no constraint found |

Two further, non-avenue notes complete the picture rather than adding a fifth route: **E**, a numerical
observation ($1/\alpha(\Lambda)=64=z_{NN}^2$ under one-loop running gives $1/\alpha(0)\approx138.6$,
$1.14\%$ from $137.036$) explicitly flagged as "suggestive; not derived from the rule," and **F**, a
diagnosis naming the missing structural element rather than supplying one.

$$\boxed{\;\text{all four avenues (A–D) produce sharp negatives or an inconclusive result; the structural obstruction is the U(1) Ward identity — }\Pi(0)=0\text{ blocks the one mechanism (Sakharov induction) that succeeds for gravity}\;}\tag{R9.10}$$

(F127, `no_go`, quantitative; artifact `test-results/F127_alpha_em_derivation.json`; test record
`F127-alpha-em-derivation`.)

### 9.3.2 Reopening conditions, characterized (F339)

F339 (2026-08-31) does not attempt to move $\alpha_\text{em}$ off `OPEN` — it names, for each of the four
avenues, the one assumption whose failure would reopen it, using three findings dated after F127 that
F127 itself could not have cited, and independently re-verifies the two hardest load-bearing algebraic
facts from scratch rather than restating cited numbers.

| Avenue | Reopening condition | Status after F339 |
|---|---|---|
| **A** | A lattice mechanism generating a $q$-independent piece of $\Pi^{\mu\nu}$ not captured by the one-loop fermion bubble — e.g. a compositeness/form-factor effect at the paired photon's own binding scale | **Narrower than F127 stated, not open.** F251/F277 *computed* $\Pi^{\mu\nu}$ on the model's own lattice and found $q_\mu\Pi^{\mu\nu}(q)=0$ exactly, in sympy — not assumed. The compositeness loophole survives, untouched, as the sole residual. |
| **B** | A genuine dynamical origin for $\mu_\star$, distinct from an accidental $O(1)$ cutoff ratio | **Premise superseded, but the supersession does not help.** F138 derives $\mu_\star=4\pi v$ exactly (the model's own NDA compositeness scale) — so a structural origin *does* exist, contra F127's "no structural threshold" reading — but $4\pi v$ constrains $v$ (ledger row D#17), not $\alpha$; avenue B's negative for $\alpha$ still stands, for a different reason than F127 gave. |
| **C** | A second, independent topological/quantization condition tying the U(1) generator's absolute normalization to a lattice-fixed geometric quantity — the standard route is Dirac monopole quantization, $eg_m=2\pi n$, if $g_m$ is independently fixed by the lattice | **Genuinely unexplored, not merely unattempted.** Zero mentions of "monopole," "Dirac quantization," or "instanton" anywhere in the project (mechanically checked). The one true fifth-avenue candidate — not attempted, flagged for a future session. |
| **D** | A constraint tying the U(1) coupling's *overall* scale — not just charge ratios — to something already fixed elsewhere in the lattice | **Confirmed still open, now precisely bounded.** F165/F279 (independently re-derived here, exact rank-6-of-7 over $\mathbb Q$) prove hypercharge quantization fixes every charge *ratio*, with exactly one residual degree of freedom — the overall normalization, fixed to $\tfrac16$ purely by SM-labelling convention. This cannot be the source of a closure by construction. |

$$\boxed{\;\text{`OPEN, no gap analysis' (F127) becomes `OPEN, four reopening conditions named, two unattempted attack surfaces named' (F339) — no new number for }\alpha_\text{em}\text{ is claimed}\;}\tag{R9.11}$$

(F339, `no_go` characterization, 4/4 checks PASS, independently reviewed to **CONFIRMED-NARROWER** after
a correction; test record `F339-alpha-em-reopening-conditions`.) The two concrete, unattempted attack
surfaces F339 names are (1) a monopole/soliton construction on the BCC lattice (avenue C's route), and
(2) the vertex/overlap-integral calculation F127's own avenue F proposed — both deliberately not
attempted in the same session, per the source's own stated caution about this sub-field's "history of
false positives."

### 9.3.3 Independent corroborating evidence (F349)

F349 (2026-09-02) does not move the grade either — it reports a second, disjoint evidence trail,
assembled independently before F339 was found in the tree, bearing on avenues A and D from a technically
unrelated construction: the wrap/walk-loop stiffness family (F143, F147, F149, F153, all 2026-06,
predating F339 by ten weeks and never cited by it).

- **Avenue A, corroborated by a stronger, non-perturbative mechanism.** F143 proves the transverse
  U(1)$_Y$ wrap-channel stiffness is exactly zero **at all orders and all scales** — a unitary-conjugation
  argument, not a one-loop transversality check — residual $1.33\times10^{-15}$; F147 proves the free
  one-tick sea's static response is exactly zero in every gauge channel via an explicit spectral-symmetry
  mechanism; F149 confirms the rigidity survives turning on a Dirac mass. **Scope caveat, stated
  precisely:** this is the *raw*, pre-mixing wrap channel, not literally F251/F277's post-mixing
  physical-photon object — corroboration by an independent mechanism reaching the same qualitative
  conclusion, not a strict logical subsumption of F339's argument.
- **Avenue D, narrowed by structural exhaustion rather than ratio-counting.** F41 (machine precision)
  shows $U(1)_Y$ has no independent lattice kinetic term at all — it rides on $U(x)$ as a Stueckelberg
  phase — so no analogue of the strong-sector's $g_s^2\chi=\tfrac14$ rotor-stiffness lock is available
  *by construction*. The fermion-loop route is closed exactly (F143/F147, above); the condensate-sector
  route was attempted (F149/F153, a Dirac-mass proxy for EWSB) and **explicitly exhausted without a clean
  result** at the perturbative-proxy level — the physical condensate coupling is $O(1)$ (F153, $E_g$
  amplitude $e=0.728$), outside every perturbative proxy tried.

$$\boxed{\;\text{avenue D's residual attack surface is narrowed from "an unattempted vertex calculation" to specifically "the non-perturbative }E_g\text{ condensate self-energy (F118), propagated through the same wrap-stiffness channel" — a harder but far better-defined target}\;}\tag{R9.12}$$

(F349, `no_go` corroboration, 6/6 checks PASS, independently reviewed to **CONFIRMED-NARROWER**; test
record `F349-alpha-em-convergent-stiffness-evidence`.) Avenues B, C, E, F are unchanged by this evidence
line. F349's own external-calibration note is worth carrying here directly: CODATA 2022 gives
$1/\alpha=137.035999177(21)$, a relative uncertainty of $1.6\times10^{-10}$ — eight orders of magnitude
tighter than avenue E's $1.14\%$ coincidence, and this sub-field (Eddington's 1929–1944 attempts to
derive $1/\alpha=136\to137$ from group theory, now regarded as numerology) is the standing cautionary
example for why that coincidence is recorded as exactly what it is and nothing more.

## 9.4 Results table

| # | Statement | Exactness | Residual / tolerance | Source |
|---|---|---|---|---|
| R9.1/R9.2 | Minimal coupling's identity-channel Peierls phase $P=e^{i\theta}\mathbb I_2$ commutes with $U^\pm(\mathbf k)$ for every $\mathbf k$; the composite $\sigma$-bilinear is a distinct, non-commuting channel — the F68 single-sector seed of R8.3's four-sector theorem | exact (structural, $[\sigma_x,\mathbf n\cdot\boldsymbol\sigma]\neq0$) / machine ($1.1\times10^{-16}$) | 5 checks | F68; CL002 (`live`, exact) |
| R9.3 | Aharonov–Bohm holonomy and sourced Maxwell curl close into one self-consistent loop on the paired photon; charge conserved to machine precision | machine | $\le2.0\times10^{-12}$ (worst leg) | F87 (20/20 PASS); CL082 investigated, §9.2.2 |
| R9.4/R9.5 | The BCC Weyl walk's exactly conserved current: $\rho$ trivial, $\mathbf J$ the minimal purely-$\hat{\mathbf C}(\mathbf k)$-longitudinal solution to exact discrete continuity; Nyquist-corner gap disclosed | machine (masked) | $3.1\times10^{-17}$ | F384; no claim card (D12 scope, see §9.2.3) |
| R9.6/R9.7 | Per-link covariant U(1) step; uniform-$\mathbf A$ exactly unitary; curl-carrying $\mathbf A$ trades unitarity for $O(\lvert qA\rvert\cdot a)$ momentum transfer, adjudicated across three forks | machine (6/10 legs) / quantitative (4/10 legs) | $\le3.8\times10^{-15}$ (machine legs) | F385; no claim card |
| R9.8/R9.9 | Vector-potential convention: Coulomb-gauge `solve` adopted over `accumulate`, purely $\mathbf C$-transverse by construction, structurally excludes F384's longitudinal current content | machine (solve legs) / quantitative (accumulate/Ward legs) | $\le2.35\times10^{-14}$ (machine legs) | F386; no claim card |
| R9.10 | Four-avenue $\alpha_\text{em}$ no-go: A/B/C sharp negative, D inconclusive; U(1) Ward identity is the structural obstruction | **no_go**, quantitative | — | F127; CL113 (`live`, `no_go`, `falsifier: none`) |
| R9.11 | Reopening conditions named for all four avenues; two unattempted attack surfaces identified; grade unchanged | **no_go** (characterization), quantitative + exact rational | 4/4 checks | F339; CL113 |
| R9.12 | Independent non-perturbative evidence corroborates avenues A/D; avenue D's residual narrowed to F118's $O(1)$ self-energy | **no_go** (corroboration), machine + exact rational | $\le1.33\times10^{-15}$ | F349; CL113 |

## 9.5 Comparison with measurement

**No direct numerical comparison against a measured electromagnetic observable is made in this chapter,
and none could be, honestly, given §9.3's own conclusion.** Every result above is either a structural/
exactness statement about the lattice construction (R9.1–R9.9, checked against the walk's own unitary,
not against data) or a no-go about what the construction *cannot* yet produce (R9.10–R9.12). The one
place a measured number enters this chapter at all is CODATA's $1/\alpha=137.035999177(21)$, cited in
§9.3.3 purely as a precision yardstick against which avenue E's $1.14\%$ numerical coincidence is shown
to fall far short of being a derivation — not as a comparison this chapter's own results are checked
against. **The actual quantitative EM comparison against measurement is deferred entirely to Chapter 23**
(QED precision): F249's comparison battery, F252's $a_e$/Lamb shift, F261's two-loop $a_e$/$a_\mu$, and
F334's hadronic vacuum-polarization estimate all run the model's QED machinery *at* the measured value of
$\alpha_\text{em}$, consuming it as the external input this chapter's no-go establishes it must be. A
reader looking for "does this model's electromagnetism match nature numerically" should read this
chapter as establishing the *machinery* that makes such a comparison possible (the current, the coupling,
the field convention) and Chapter 23 as where the comparison is actually run — conflating the two would
overstate what is shown here.

## 9.6 What was excluded, and why

**The composite $\sigma$-bilinear as the electric-charge photon.** Already excluded in full in Chapter 8
(§8.5, R8.16) on two independent grounds — GRB/AGN polarimetry (S1) and the identity-channel forcing this
chapter's own F68 supplies (R9.1/R9.2). Not re-argued here; this chapter's contribution is showing the
forcing holds at the level of the model's actual U(1) mass-step and hypercharge operators, not only the
abstract $(g_L,g_R)$ classification.

**`accumulate` as the vector-potential convention.** Excluded by F386 (§9.2.5, R9.8/R9.9): it structurally
cannot avoid inheriting F384's own purely-longitudinal current content as spurious $\mathbf A$, with no
mechanism to separate that from a genuine transverse photon. `solve` is adopted instead.

**Strang-splitting and unbounded per-site renormalisation as fixes for the per-link step's unitarity/
momentum-transfer tension.** Both tested (F385 §9.2.4, forks b and d) and both found not to generalise:
Strang-splitting reduces the drift coefficient but not its power law; per-site renormalisation is exact
but its momentum-transfer signal diverges from fork (a)'s at broad field widths rather than tracking it.
Neither is adopted as *the* Stage 2 construction; fork (a) (accept the drift, scoped to the curl-carrying
sector where it is unavoidable per R9.7) is the one Stage 3/4 build on.

**The four avenues to deriving $\alpha_\text{em}$ (F127), in full, with F339's reopening conditions and
F349's corroboration.** Presented in §9.3 above as the chapter's own dedicated no-go section, per the
build instructions' explicit direction that a no-go this consequential (it names the model's last free
dimensionless input) gets its own clearly-marked treatment rather than a brief mention — see §9.3.1–9.3.3
for the full avenue-by-avenue argument, not repeated here.

## 9.7 What is still open — and the hand-off to Chapter 10

**F384, F385, and F386 are solid, settled results, not provisional ones.** Each carries a `**Status:**
Confirmed` line with an explicit pass count (4/4, 10/10, 7/7 legs respectively), a documented control
that verifies red exactly where declared, a `can-fail` check, and — beyond the ordinary gate-tier bar —
each was independently cold-re-derived by a separate subagent and adversarially reviewed, landing at
**CONFIRMED-NARROWER** in all three cases: the reviews found and fixed real fragilities (a control-test
comparator in F384, a mis-measured order-of-magnitude claim in F385, a factual error about whether
$\mathbf B$ stays zero in F386) but did not overturn any of the three findings' central constructions.
This chapter treats them as the settled foundation they are: the current the walk conserves, the
covariant step that couples it (scoped precisely to where it is and is not exact), and the field
convention that feeds that step — all in place, all machine-precision or exactly verified within their
stated scope.

**What is not yet built, stated plainly rather than summarized ahead of its own chapter.** None of
F384–F386 wires these three pieces into an actual running coupled channel — F386 §4 is explicit that
"this does not build the coupled `em_photon`/`fermion_em` channel pair itself (Stage 4) or run the
closed-loop momentum-transfer scenario (Stage 5)." Every $\mathbf A$ field used in this chapter's own
derivation is a hand-built test bump, not one sourced by a live photon channel reacting to a real
fermion's current in real time. This chapter deliberately does not attempt that coupling, and does not
summarize what happens when it is attempted — this chapter's authors have not read Chapter 10's findings
(F387–F395) and Chapter 10 does not yet exist as a settled document (`00-plan.md` §4 states plainly that
it is written as a live research report, not a retrospective). What can be said honestly from *this*
chapter's own vantage point is only that the foundation Chapter 10 builds on is sound, and that the two
open technical seams this chapter's own findings already name — the curl-carrying-vs-curl-free scope
limit of the per-link step (R9.7), and the $\Omega_\text{pair}(\mathbf k)$-vs-$\lvert C_\text{odd}
(\mathbf k)\rvert$ propagator mismatch F386's own review traced (§9.2.5, "why $\mathbf B$ doesn't stay
zero") — are precisely the seams a reader should expect Chapter 10's coupled-dynamics investigation to
run into first.

Two further disclosed-but-unresolved technical items, named by their own findings rather than
rediscovered here, are worth carrying forward explicitly:

1. **`bcc_curl_symbol`'s direction is exactly anisotropic off the cubic axes** — $\hat{\mathbf C}(\mathbf
   k)\to(k_x,-k_y,k_z)/\lvert k\rvert$, not $\hat{\mathbf k}$, a genuine continuum-limit property (stable
   from $L=16$ to $L=256$), traced to the same sign convention that is load-bearing and correct for the
   fermion sector's own dispersion but was not previously known to propagate into the curl symbol's
   *direction* (its magnitude is unaffected — every existing speed/magnitude check, including F87's own
   MX1, is untouched). F386 flags this explicitly as unresolved and possibly deserving its own finding
   number; this chapter does not attempt that reconciliation.
2. **The binding coupling that puts the photon exactly at two-body criticality (Ch.8, F169) remains
   undetermined from the U(1) minimal-coupling Lagrangian this chapter builds.** F169's own open item is
   unchanged by anything in this chapter: this chapter derives the current and the coupling *form*, not
   the interaction strength that would let a first-principles binding calculation be attempted.

**The $\alpha_\text{em}$ no-go itself is not "open" in the same sense as the above** — it is a settled
characterization of a genuine, currently-standing structural obstruction (§9.3), not a construction gap
awaiting the next session's fix. Reopening it requires one of the two concrete attack surfaces F339/F349
name (a monopole construction, or the non-perturbative $E_g$ condensate self-energy), both explicitly
unattempted and both flagged as genuine future research, not routine follow-up.

## 9.8 Falsifiers

From the relevant claim cards, at their actual status:

1. **CL002 (F68 among its findings) carries `falsifier: stated`** — inherited from Chapter 8's own
   treatment (§8.7): any confirmed detection of linear vacuum birefringence with the energy dependence
   the excluded chiral construction predicts would falsify the paired-photon/identity-channel picture
   this chapter's coupling is built on.
2. **CL113 (F127/F339/F349, the $\alpha_\text{em}$ no-go) carries `falsifier: none` — structural, and
   the card states precisely why.** A no-go against a derivation is not falsified by an experiment; it is
   falsified by *finding the derivation*. The two named routes: (1) constructing a Dirac-monopole-type
   soliton on the BCC lattice whose magnetic charge is independently fixed by lattice geometry, giving
   $\lvert e\rvert$ via Dirac quantization (avenue C); or (2) computing the non-perturbative $E_g$
   condensate self-energy (F118) propagated through the wrap-stiffness channel (avenue D's narrowed
   residual, F349). Either closing would reopen $\alpha_\text{em}$ from `OPEN`.
3. **F384, F385, F386 carry no claim cards and therefore no stated falsifiers of their own** — by design,
   per D12's bar (engine-capability additions, not claims against established physics). Their own
   internal falsifiers are the declared negative controls each finding's own test record carries (§9.2.3–
   9.2.5): each control is verified, measured, to turn exactly its declared legs red and no others — the
   `can-fail` protocol substituting for a claim-card falsifier where no claim is issued.
4. **CL307 (Chapter 10's own card, `narrowed`, citing F385 among others) is not this chapter's to
   state** — it belongs to the coupled-dynamics investigation this chapter explicitly does not enter
   (§9.7). Named here only so a reader following falsifiers forward knows where the next one is written,
   not to summarize its content.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–8's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $P=e^{i\theta}\mathbb I_2$ | The identity-channel Peierls (gauge) phase the U(1) connection applies to a Weyl spinor; commutes with $U^\pm(\mathbf k)$ for every $\mathbf k$, forcing the even/non-birefringent channel. | §9.2.1 |
| $\rho(\mathbf x)$, $\mathbf J(\mathbf x)$ | The BCC Weyl walk's exactly conserved U(1) charge density and current; $\rho$ trivial from unitarity, $\mathbf J$ the minimal purely-$\hat{\mathbf C}(\mathbf k)$-longitudinal solution to exact discrete continuity. | §9.2.3 |
| $\mathbf C(\mathbf k)$, $\hat{\mathbf C}(\mathbf k)$ | The (odd-in-$\mathbf k$) BCC curl symbol underlying the Gauss/Ampère machinery, the current's continuity equation, and the $\mathbf A$-field solve; exactly anisotropic in *direction* off the cubic axes (§9.7 item 1), isotropic in magnitude. | §9.2.2 (F87), formalized §9.2.3 |
| $U_{\mathbf d}(\mathbf x)=e^{iq\mathbf A(\mathbf x)\cdot\mathbf d/\sqrt3}$ | The per-link Peierls phase attached to each of the 8 BCC hop directions individually; the covariant step's basic object. | §9.2.4 |
| $\mu_\star$ | The Higgs-free electroweak matching scale, $=4\pi v$ exactly (F138); the structural scale avenue B's reopening condition turns on, orthogonal to deriving $\alpha_\text{em}$ itself. | §9.3.2 |

---

*No new gap logged this chapter: the two disclosed-but-unresolved technical items (§9.7) are already
named honestly by their own source findings (F386's own text flags the curl-symbol anisotropy as
possibly warranting its own finding number) rather than smuggled in without acknowledgement, so neither
meets this monograph's bar for a `docs/monograph/GAPS.md` entry (a place where the *documentation* would
otherwise paper over a hole) — they are carried forward in §9.7 as ordinary open research items instead,
the same treatment Chapters 1–8 gave their own sources' self-disclosed open questions. The CL082/F87
claims-layer investigation (§9.2.2) found the same mechanical bookkeeping pattern Chapters 7 and 8 already
logged (no new instance, not re-logged); no other claim card discrepancy was found for CL113 or CL002/
CL271 as cited here. No finding, claim card, module, or test record was created or modified in the
writing of this chapter.*
