# Chapter 23 — QED Precision: Vacuum Polarization, Running $\alpha$, $a_e$/$a_\mu$, the Lamb
Shift, and the Comparison Battery

*Chapter 23 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F249-qed-comparison-battery.md`, `findings/F260-qed-scattering-smatrix.md`,
`findings/F252-qed-vertex-ae-lamb-shift.md`, `findings/F257-bethe-log-from-model-spectrum.md`,
`findings/F259-ir-bremsstrahlung.md`, `findings/F261-twoloop-qed-ae-amu.md`,
`findings/F262-positronium-hydrogen-hyperfine-lamb.md`,
`findings/F263-euler-heisenberg-schwinger-nonlinear-qed.md`,
`findings/F264-qed-allorders-renormalizability-anomaly.md`,
`findings/F277-qed-gluon-refold-period.md`, `findings/F311-gap5-three-numbers-adjudicated.md`,
`findings/F322-b9-running-alpha-ew-rederived-post-f277.md`,
`findings/F334-hadronic-vmd-rho-omega-delta-alpha-estimate.md`,
`findings/F336-twoloop-vp-nonlog-scope.md`, `findings/F370-lamb-shift-twoloop-residual-scoped.md`
— the fifteen findings `00-plan.md` §2 assigns to this chapter, all read in full — plus
`docs/monograph/01-postulates-and-ontology.md` (P1–P7), `docs/monograph/09-electromagnetism.md`
§9.1/§9.3 (R9.10–R9.12, the $\alpha_\text{em}$ four-avenue no-go this chapter's every numerical
comparison consumes as an external input), and `docs/monograph/11-mass-without-a-higgs.md`
§11.2.3–§11.2.6 (R11.3–R11.13, the complex-mass mechanism whose electron this chapter's loops act
on). Checked directly against `docs/theory/supersessions.yaml` — **S11** and **S12**, both read in
full (§23.6 below is where their content is presented) — and against `claims-index.md`: **CL222**
(F252, `live`, exact, `falsifier: unset`), **CL224** (F257, `live`, quantitative, `falsifier:
unset`), **CL226** (F259, `live`, exact, `falsifier: unset`), **CL227** (F260, `live`, exact,
`falsifier: unset`), **CL228** (F262, `live`, exact, `falsifier: unset`), **CL229** (F263, `live`,
exact, `falsifier: unset`), **CL230** (F264, `live`, exact, `falsifier: unset`), **CL280** (F322 +
F311 + F251 + F277 + F261 + F138 + F336, `contingent`, quantitative, `falsifier: stated`), **CL288**
(F334 + F103 + F128 + F240, `open`, quantitative, `falsifier: stated`, `rolls_up_to: CL280`), and
**CL019** (F261 + F249, `kind: non_claim`, `status: not_claimed` — the muon $g\!-\!2$ hadronic/EW
scope boundary, cited in §23.6). None of the fifteen assigned findings appears in any
`supersessions.yaml` `superseded:` list. Notation, postulates and results are those of Chapters 1, 9
and 11 — $P=e^{i\theta}\mathbb I_2$, $\rho(\mathbf x)$/$\mathbf J(\mathbf x)$, $\alpha_\text{em}$ as
free external input, $\Omega_\text{rest}(m)=\arcsin m$, $M(\theta)$ — extended, never redefined.*

## 23.0 What this chapter establishes

Chapters 9 and 11 built the model's electromagnetic coupling and mass mechanism and, in each case,
stopped at the boundary of a genuine open construction problem: Chapter 9's no-go on deriving
$\alpha_\text{em}$'s magnitude, Chapter 11's silence on any fermion's numerical mass. This chapter
does something different with both of those open boundaries: it takes the electron mass and
$\alpha_\text{em}$ as **given, measured numbers** — exactly as Chapter 9 disclosed they must be
consumed — and asks what the model's own field content, run through actual loop calculations,
*predicts* once those two numbers are fixed. The answer is precise and, on the whole, favorable: the
model's paired-spinor photon (Chapter 8) and its Weyl-primitive-plus-chiral-$SU(2)$ electron
(Chapter 11) support a genuine perturbative QED expansion — tree level (F260), one loop (F252,
F257, F259), two loops (F261, F336, F370), the nonlinear/non-perturbative sector (F263), and an
all-orders renormalizability closure (F264) — that reproduces the electron and muon anomalous
moments, the hydrogen Lamb shift, the positronium spectrum, and a dozen other precisely measured
numbers to between $10^{-3}$ and $10^{-13}$ relative accuracy, with every input named.

The chapter's second job is to present, honestly and without either softening or inflating it, a
real historical correction: a momentum-refold defect (**F277**, correcting **S11**/**S12**) flipped
the *sign* of the one-loop vacuum-polarization residual computed on this model's own lattice kernel,
before this chapter's assigned findings were written. §23.6 states precisely what broke, what F277
fixed, and how the downstream findings (F311, F322) responded — not as if nothing had gone wrong,
but as the record of a defect found, diagnosed, and corrected, with every affected number re-run and
none of the surrounding exact algebra ($b_0^\text{QED}=4/3$, $Z_1=Z_2$, the Ward identities) ever
in question.

## 23.1 Inputs

**Postulates used.** **P4** (exact unitarity) underwrites every algebraic identity in this chapter —
the Ward–Takahashi identity (F252, F264), charge conjugation (F260), the Bloch–Nordsieck
cancellation (F259) — the same way it underwrote Chapters 8, 9 and 11. **P5** (the massless
two-component Weyl primitive) is the field every loop diagram in this chapter is built from; **P6**
(the chiral $SU(2)$ mechanism, Chapter 11) is what gives that primitive the electron's mass, with
zero new structural assumption introduced in this chapter — the electron propagator used throughout
is exactly Chapter 11's $\Omega_\text{rest}(m)=\arcsin m$ object, continued off-shell.

**Prior results used, precisely.** **R9.1/R9.2** (F68, Ch.9) — the identity-channel Peierls coupling
$P=e^{i\theta}\mathbb I_2$ forced by minimal coupling — is the vertex $e\gamma^\mu$ every diagram in
this chapter attaches to; **R9.3** (F87, Ch.9) is the earlier Aharonov–Bohm/Gauss certification this
chapter's tree-level and loop machinery builds on without re-deriving. **R8.4/R8.5** (F69, Ch.8) is
the internal and external photon line — massless, transverse, non-birefringent — used in every
diagram. **R11.3–R11.13** (F27/F167, Ch.11) is the electron: its exact unitarity, its rest-mass
rotation-angle identity, and R11.14's own statement that the mass *magnitude* is a free input, which
this chapter now spends as a measured number (§23.1, item 1 below) rather than leaving abstract.

**Free inputs consumed — stated plainly, per this chapter's own mandate.**

1. **$\alpha_\text{em}$ is consumed at its measured, CODATA value throughout this chapter, exactly as
   Chapter 9's four-avenue no-go (R9.10–R9.12) requires.** Chapter 9 is explicit that "wherever a
   chapter needs a numerical value of $\alpha_\text{em}$ (most directly Chapter 23's QED precision
   battery)... that value is read in from measurement, not produced by the lattice rule"
   (`09-electromagnetism.md` §9.1, item 1). This is not a hidden inconsistency introduced here — it
   is the single free numerical input Chapter 9 already disclosed this chapter would need, and every
   comparison-with-measurement result below (§23.5) inherits it. CODATA 2022: $\alpha^{-1}=
   137.035999177(21)$ (F249).
2. **The electron mass $m_e=0.51099895$ MeV and the muon mass $m_\mu=105.6575$ MeV (F120/F121
   anchors)** are consumed as measured inputs, exactly as Chapter 11's own free-input accounting
   (§11.1) disclosed: "the overall scale... is Chapter 17's SI-closure derivation... This chapter's
   own comparison-with-measurement content is therefore genuinely null at the numerical level." This
   chapter is the first to spend that scale numerically, reading it in from measurement rather than
   waiting on Chapter 17's derivation, exactly as F249/F260 state their own inputs to be "$\alpha$ and
   the lepton masses."
3. **Nothing else is free.** Every loop coefficient, form factor, and cross section computed below is
   a closed-form or numerically-converged consequence of the model's own vertex ($e\gamma^\mu$,
   forced) and propagators (paired photon, Dirac electron), with the two items above as the only
   external numbers. Several results import a **literature closed form** rather than deriving it on
   the model's own fields — this is flagged precisely, finding by finding, in §23.3 and §23.6 rather
   than left implicit: F252's Bethe logarithm (later removed by F257), F261's six vertex-master
   integrals (Group II of $A_2$), F262's Bethe–Salpeter recoil coefficient and Ore–Powell spectrum,
   and F311/F322/F336's two-loop Källén–Sabry non-log constant.

## 23.2 The derivation

### 23.2.1 Tree level: the S-matrix and the antiparticle sector (F260)

Before any loop, the chapter needs a working tree-level QED S-matrix on the model's own fields, and
in particular a positron — nothing prior had exercised the antiparticle sector at all. F260
(2026-07-22) builds it directly from the model's own ingredients: the F87/F68 identity-channel
vertex $e\gamma^\mu$, the F69/F250 even-law transverse paired photon, and the F27/F46 Dirac electron.
The positron is not a separate postulate — it is the electron's **charge conjugate**,
$v(p,s)=C\bar u(p,s)^\top$ with $C=i\gamma^2\gamma^0$, verified to satisfy $C\gamma^\mu C^{-1}=
-(\gamma^\mu)^\top$ to literal zero (sympy), and the model's own completeness relations $\sum_s
u\bar u=\slashed p+m$, $\sum_s v\bar v=\slashed p-m$ hold to $<10^{-11}$ with **no eigen-decomposition
of a chiral matrix anywhere** (CLAUDE.md's standing constraint).

$$\boxed{\;C\gamma^\mu C^{-1}=-(\gamma^\mu)^\top\text{ (literal 0); }v=C\bar u^\top\text{ satisfies }\textstyle\sum_s v\bar v=\slashed p-m\text{ to }<10^{-11}\;}\tag{R23.1}$$

(F260, gates G1/G2; test `test_F260_qed_scattering.py`.) With the positron in hand, crossing
symmetry between Møller/Bhabha and Compton/annihilation is exact (sympy, literal identities, G3),
and every classic tree cross section reproduces the textbook Mandelstam-invariant closed form to
machine precision, with the gauge (Ward) identity verified on explicit on-shell spinors for every
process:

| Process | $\langle|\mathcal M|^2\rangle$ vs textbook | $\sigma$ vs closed form | Ward |
|---|---|---|---|
| Compton / Klein–Nishina | $<10^{-13}$ | $\le4.5\times10^{-7}$ (→ Thomson as $\omega\to0$) | $<10^{-12}$ |
| Møller | $<10^{-13}$ | — (differential, barn/sr) | — |
| Bhabha | $<10^{-13}$ | — (differential, barn/sr; $=$ Møller under $s\leftrightarrow u$) | — |
| $e^-e^+\to\gamma\gamma$ (Dirac annihilation) | $<10^{-13}$ | $\le1.6\times10^{-6}$ | $<10^{-15}$, both legs |
| $e^-e^+\to\mu^-\mu^+$ | $<10^{-13}$ | $\le1.6\times10^{-8}$ (→ R-ratio unit $4\pi\alpha^2/3s$) | — |

$$\boxed{\;\text{11/11 tree-level gates PASS: crossing exact, Ward exact, every }\langle|\mathcal M|^2\rangle\text{ matches the textbook Mandelstam form to}<10^{-13}\;}\tag{R23.2}$$

(F260, 11/11; test record surfaced as Tier D of `test_F249_qed_comparison_battery.py`.) The
Klein–Nishina total cross section, as $\omega\to0$, reduces to the Thomson value $\sigma_T=
0.6652459$ barn from the model's own $\alpha,m_e$, against CODATA $0.66524587$ barn — the same number
F249's Tier A5 already certified (§23.2.2), now recovered as a genuine $\omega\to0$ limit of the full
Compton process rather than asserted independently.

### 23.2.2 The early qualitative/quantitative battery (F249)

F249 (2026-07-16) predates the loop sector entirely and asks a narrower question first: does the
paired-spinor photon (Chapter 8) reproduce quantitative, not merely qualitative, electrodynamics?
Its Tier A (tree/classical) and Tier B (photon-precision) results — masslessness, luminality at
$1/\sqrt3$, the massless Coulomb pole (not Yukawa), the Thomson cross section, exact Ward/charge
conservation, zero linear birefringence, $O(k^3)$-suppressed anisotropic LIV — are all confirmed and
carried forward without qualification; they are exactly the tree-level content Chapter 9 (R9.1–R9.9)
and Chapter 8 (R8.1–R8.16) already established from the field-theory side, now certified
numerically against measured constants.

$$\boxed{\;\text{Tier A/B: masslessness, luminality (}0.57735\text{ vs }1/\sqrt3\text{), Coulomb pole (}m^2\to0\text{), }\sigma_T\text{ to }3\times10^{-9}\text{, zero birefringence (}3.3\times10^{-16}\text{), }O(k^3)\text{ LIV — all PASS}\;}\tag{R23.3}$$

(F249, 9/9 computed checks; test `test_F249_qed_comparison_battery.py`.) F249's Tier C, however, is
an **honest reference ledger, not a result**: at the time it was written the model had "no
interacting loop sector," and it records $a_e$, running $\alpha(q^2)$, and the Lamb shift as **"not
computable"** — the exact reference values (Schwinger $\alpha/2\pi$, PDG running, Lundeen–Pipkin's
$1057.845$ MHz) named alongside the specific missing machinery, with nothing faked as a pass. Every
one of those three "not computable" items is exactly what §23.2.3–§23.2.5 below compute. **This
chapter reads F249's Tier C as superseded in substance by later findings (chronologically, F252 the
same day, F261 and F262 within a week) without F249's own text being rewritten** — findings are
written once and superseded rather than rewritten, per this monograph's standing convention (already
applied to F192 in Chapter 18/§9's F311 discussion) — and F252's own header carries the explicit
cross-reference "closes the ledger: C1 + C3" confirming this reading is not an inference this chapter
is making unilaterally.

### 23.2.3 One-loop vertex: $a_e=\alpha/2\pi$ and the Lamb shift (F252)

F252 (2026-07-16, the same day as F249) builds the one-loop vertex $\Lambda^\mu(p,p')$ — the
electron emitting and reabsorbing a paired photon — from two F87 identity-channel vertices. The
Ward–Takahashi identity is algebraically exact:

$$q_\mu\Lambda^\mu=\slashed q=S^{-1}(p')-S^{-1}(p)\tag{V1, literal 0}$$

and the magnetic form factor at zero momentum transfer reduces the Peskin–Schroeder Feynman-parameter
integral to a trivial $x$-integration plus $\int_0^1 2z\,dz=1$ **exactly**:

$$\boxed{\;a_e=F_2(0)=\frac{\alpha}{2\pi}=1.16141\times10^{-3}\quad\text{vs measured }1.15965218\times10^{-3}\ (0.15\%)\;}\tag{R23.4}$$

(F252, V2, exact algebraic identity — the $0.15\%$ deviation is entirely the omitted higher-order
QED, closed at two loops in §23.3 below.) The Uehling coefficient $-\tfrac4{15}$ is *derived* here
— not cited — from the low-$q^2$ limit of the F251 one-loop vacuum-polarization bubble (Chapter 9's
sibling finding, not itself assigned to this chapter but the object F252's V3 builds on):
$\Pi(q^2)\to\tfrac{2\alpha}{\pi}\tfrac{q^2}{m^2}\int_0^1x^2(1-x)^2dx=\tfrac{\alpha}{15\pi}\tfrac{q^2}{m^2}$,
exactly. Feeding the resulting self-energy (Bethe log, at this stage a **literature input**,
Drake/Klarsfeld $\ln k_0(2s)=2.8118$) and the derived Uehling piece into the exactly-degenerate
one-body Dirac–Coulomb $2s_{1/2}$–$2p_{1/2}$ splitting (Chapter 24's F125 solver, zero splitting at
tree level) lifts the degeneracy to:

$$\boxed{\;\Delta E_\text{Lamb}=1052.19\text{ MHz (self-energy }+1079.32\text{, Uehling }-27.13\text{) vs measured }1057.845\text{ MHz}=99.5\%\;}\tag{R23.5}$$

(F252, V4, quantitative; residual $\approx5.6$ MHz is higher-order $\alpha(Z\alpha)^5$/two-loop,
explicitly out of leading-order scope — the object §23.6's F370 later scopes precisely.)

### 23.2.4 The Bethe logarithm, derived from the model's own spectrum, no literature input (F257)

F252's one remaining literature constant is the Bethe logarithm. **F257 (2026-07-20) removes it —
this is a genuine strength of the model, worth stating explicitly rather than passing over: nothing
comparable exists elsewhere in this chapter's sources at this level of self-containment.** The Bethe
log is a log-weighted mean excitation energy over the *entire* intermediate spectrum,
$\ln k_0(n,l)=\sum_m|\langle n|\mathbf p|m\rangle|^2(E_m-E_n)\ln|E_m-E_n|\,/\,\sum_m|\langle
n|\mathbf p|m\rangle|^2(E_m-E_n)$ — a direct pseudostate sum converges too slowly to be practical
(the $\ln|E_m-E_n|$ weight emphasizes high-energy virtual states). F257 turns the state sum into a
one-dimensional integral over the model's own **Coulomb resolvent** (Dalgarno–Lewis technique),
solved as a stable tridiagonal inversion of the model's own finite-difference Coulomb Hamiltonian —
i.e., the model's own spectrum, sampled through its resolvent, with no tabulated constant anywhere in
the calculation:

| State | Model $\ln k_0$ | Accepted (Drake/Klarsfeld) | Deviation |
|---|---|---|---|
| $1s$ | $2.9204$ | $2.9841$ | $-2.1\%$ |
| $2s$ | $2.7479$ | $2.8118$ | $-2.3\%$ |
| $2p$ | $-0.0369$ | $-0.0300$ | $+0.007$ (abs) |

$$\boxed{\;\text{Bethe logarithms derived from the model's own Coulomb resolvent, no literature input, to }\sim2\text{--}3\%\;}\tag{R23.6}$$

(F257, B1–B3.) Feeding the model-derived $\ln k_0$ back into F252's Lamb-shift formula (self-energy
now $+1087.1$ MHz, Uehling unchanged $-27.1$ MHz) gives a **fully model-derived** Lamb shift:

$$\boxed{\;\Delta E_\text{Lamb}^\text{fully model-derived}=1059.9\text{ MHz vs measured }1057.845\text{ MHz — within }0.2\%\;}\tag{R23.7}$$

(F257, B4.) F257's own honest caveat: the $\sim2$–$3\%$ per-state deviation is a continuum-representation
systematic of the uniform radial grid (dominated by short-distance behavior in the resolvent's $M_3$
moment), not a grid-spacing artifact — reaching six-digit tabulated precision would need a
logarithmic grid or Coulomb–Sturmian basis, noted as a refinement, not required for the physics point
that the Lamb shift is now derivable from the model's own spectrum with zero literature input.

### 23.2.5 The infrared sector: soft bremsstrahlung and Bloch–Nordsieck cancellation (F259)

F252's vertex and its sibling self-energy are each individually IR-divergent on shell (a small
photon mass $\mu$ regulator carries $\ln\mu$ in the renormalized $F_1(q^2)$ and $Z_2$). F259
(2026-07-22) supplies the real soft-photon emission that cancels it. The eikonal factorization off
the F87 vertex is exact — the on-shell spinor identity $\bar u(p')\gamma^\mu(\slashed p'+m)=2p'^\mu
\bar u(p')$ verified to literal zero — and current conservation for the eikonal current $J^\mu=
p'^\mu/(p'\cdot k)-p^\mu/(p\cdot k)$ is a one-line literal identity, $k_\mu J^\mu=1-1=0$, which lets
the F250 two-polarization transverse residue stand in for the full gauge sum.

$$\boxed{\;k_\mu J^\mu=0\text{ (literal); }\int_\mu^{\Delta E}\frac{d\omega}\omega=\ln\frac{\Delta E}\mu\text{ (exact); coefficient of }\ln\mu^2\text{ in virtual}+\text{soft}=0\text{ (literal — Bloch–Nordsieck)}\;}\tag{R23.8}$$

(F259, B1/B2/B4/B3, all algebraic identities.) The shared IR coefficient $f_{IR}(q^2)$ matches the
closed high-energy form $\ln(-q^2/m^2)-1$ to $8\times10^{-4}$ (Q1, quadrature-limited); the finite,
$\mu$-independent Sudakov correction at $\sqrt{-q^2}=1$ GeV, $\Delta E=100$ MeV is $-0.151$, giving an
exponentiated suppression $e^{-0.151}=0.859$ (Q2). The physically important structural point: the
lattice speed $c_\text{lat}=1/\sqrt3$ **cancels identically** out of the dimensionless IR coefficient
— because the IR log lives entirely at $k\to0$, exactly where Chapter 9's own results (R9's parent,
F249 A2/A3) show Lorentz invariance is restored, the coefficient the lattice produces is the
*continuum* $f_{IR}$, and it cancels the continuum loop like-for-like. This closes the one-loop
sector's *inclusive* finiteness: with F251 ($Z_3$, Chapter 9's sibling), F258 ($Z_2$, likewise), F252
($Z_1$, $F_1$, $a_e$, Lamb) and F259 (IR), the model's one-loop QED produces genuinely finite,
physical cross sections.

### 23.2.6 Two-loop QED: $A_2=-0.328478966$, the two-loop $\beta$-function, and lepton universality (F261)

F261 (2026-07-23) is the first two-loop result in the model's QED sector, and the construction is
distinctive: rather than citing the two-loop electron anomalous-moment coefficient wholesale, it
**derives half of it from the model's own one-loop vacuum polarization**. Dressing the internal
photon of F252's one-loop vertex with F251's own spectral function $\tfrac1\pi\operatorname{Im}
\Pi(s)=\tfrac\alpha{3\pi}(1+2m_f^2/s)\sqrt{1-4m_f^2/s}$ is, by Källén–Lehmann, a superposition of
massive photons, each contributing through F252's own Feynman-parameter kernel $K_1(u)=\int_0^1dx\,
x^2(1-x)/[x^2+u(1-x)]$ (with $K_1(0)=\tfrac12$ recovering Schwinger). The equal-mass dispersive
integral gives the vacuum-polarization group of $A_2$ **model-derived**:

$$\boxed{\;A_2^\text{VP}=\frac{119}{36}-\frac{\pi^2}3=0.0156874219\ldots\quad(3\times10^{-10}\text{ from F251's spectral function alone})\;}\tag{R23.9}$$

(F261, T1.) The vertex-type group (six Laporta–Remiddi master integrals — **cited**, matching F252's
own honesty tier for its six masters, not re-derived from scratch) sums to the established closed
form $-\tfrac{31}{16}+\tfrac{5\pi^2}{12}-\tfrac{\pi^2}2\ln2+\tfrac34\zeta(3)=-0.3441663874\ldots$, and
the two groups' sum is a sympy-exact identity matching Sommerfield–Petermann:

$$A_2=\frac{197}{144}+\frac{\pi^2}{12}-\frac{\pi^2}2\ln2+\frac34\zeta(3)=-0.328478966\ldots\tag{T2, exact}$$

The two-loop QED $\beta$-function coefficient is sympy-exact, $b_1=1$ per unit-charge Dirac fermion
in $\mu\,d\alpha/d\mu=\tfrac{2\alpha^2}{3\pi}+\tfrac{\alpha^3}{2\pi^2}+\ldots$ — this coefficient is
the load-bearing object §23.2.8 (F322) and §23.6 (F311) use to re-derive the running of $\alpha$
post-F277. With the electron's total two-loop coefficient (heavy loops decoupling as $(m_e/m_f)^2$):

$$\boxed{\;a_e=\frac\alpha{2\pi}+A_2(e)\left(\frac\alpha\pi\right)^2=1.15963743\times10^{-3}\quad\text{vs measured }1.15965218\times10^{-3},\ \text{rel. err }1.3\times10^{-5}\;}\tag{R23.10}$$

(F261, T3 — the one-loop's $0.15\%$ cut by two orders of magnitude; residual is the three-loop
$A_3=1.181\ldots$, out of scope.) Lepton universality — the mass-independent $A_1=\tfrac12$, $A_2=
-0.328478966$ are the **same object** for the electron and muon, not a fit — is an exact identity
(U1), and the light-electron-loop-in-heavy-muon-vertex logarithm is what makes $a_\mu\ne a_e$:

$$\boxed{\;A_2^\text{VP}(e\text{ in }\mu)=\tfrac13\ln(m_\mu/m_e)-\tfrac{25}{36}+\ldots=1.09425831\ \text{vs known }1.0942583;\quad A_2(\mu)=0.765857421\ \text{vs known }0.765857410\;}\tag{R23.11}$$

(F261, U2/U3, abs. err $1\times10^{-8}$; the reverse heavy-in-light insertion decouples to
$5.2\times10^{-7}$, an asymmetry of $\sim2\times10^6$.) **Explicitly out of scope, and stated as such
per CL019** (F261's own claim card, `kind: non_claim`, `status: not_claimed`): "Hadronic vacuum
polarisation, hadronic light-by-light and electroweak contributions are not computed and not
claimed" — this chapter makes no claim about the full Standard Model $a_\mu$ or the experimental
muon anomaly, an active, unsettled area (Muon $g\!-\!2$ Theory Initiative white papers).

### 23.2.7 Bound-state QED: positronium, 21 cm, and recoil/finite-size completeness (F262)

F262 (2026-07-23) extends bound-state QED past Chapter 24's single-particle Dirac–Coulomb hydrogen
(F125) and F252/F257's one-loop radiative shift into the two-body and hyperfine sectors, built
entirely from this chapter's own prior pieces: F125's Coulomb solver reused at reduced mass, F260's
charge-conjugate positron and annihilation vertex, F27/F46's $g=2$ Dirac moment, and F252/F257's
radiative Lamb shift.

**Positronium spectrum.** The reduced-mass reduction ($\mu=m_e/2$) is structural and exact:
$E_n(\mathrm{Ps})/E_n(\mathrm H_\infty)=\tfrac12$ for every level, grid-independent (machine zero).

**Hyperfine splitting.** $\Delta E_\text{hfs}=\tfrac7{12}\alpha^4m_ec^2$, with $\tfrac7{12}=\tfrac13+
\tfrac14$ verified exactly (sympy): the spin–spin (Fermi contact) piece $\tfrac13$ from the F27/F46
$g=2$ moments (`rel_err<10^{-12}`), and the virtual-annihilation piece $\tfrac14$ — unique to a
particle–antiparticle pair, forbidden for para-Ps — whose contact strength is **the model's own**
F260 single-photon $e^+e^-$ coupling (the threshold $\beta\to0$ limit of the F260 annihilation cross
section, matching $\sigma v\to\pi\alpha^2/m^2$ to $<0.04\%$):

$$\boxed{\;\Delta E_\text{hfs}=204{,}387\text{ MHz vs measured }203{,}389\text{ MHz }(+0.49\%,\text{ the known }O(\alpha^5)\text{ Karplus–Klein term, out of LO scope})\;}\tag{R23.12}$$

**Decay rates.** The para $\to2\gamma$ rate is **fully model-derived**, built from the F260
threshold cross section: $\Gamma(\text{para})=4(\sigma v)_\text{thr}|\psi(0)|^2$, coefficient
matching $\tfrac12\alpha^5$ to `rel_err<10^{-12}$, giving $\tau=0.1245$ ns against the measured
$0.1245$ ns. The ortho $\to3\gamma$ rate needs the literature Ore–Powell (1949) phase-space
coefficient $\tfrac{2(\pi^2-9)}{9\pi}$ (reproduced by direct integration to `rel_err<5\times10^{-4}$),
giving $\tau=138.7$ ns against the measured $142.05$ ns (the shift is the known $O(\alpha)$
correction).

**Hydrogen 21 cm.** The Fermi contact formula, with the reduced-mass factor and the model's own
electron anomalous moment (F252's $a_e=\alpha/2\pi$) folded in:

$$\boxed{\;1420.49\text{ MHz vs measured }1420.4058\text{ MHz, rel. err }5.8\times10^{-5}\;}\tag{R23.13}$$

(the proton $g$-factor $g_p=5.5857$ is the single non-QED input.) **Recoil and finite size**, on the
F252/F257 baseline ($1052.19$ MHz): reduced-mass rescaling $-1.72$ MHz, leading recoil (cited,
Eides–Grotch–Shelyuto) $+0.36$ MHz, finite nuclear size ($\propto r_p^2$, $r_p=0.8409$ fm) $+0.138$
MHz — giving $1050.97$ MHz against the measured $1057.845$ MHz, a residual of $+6.87$ MHz **that
F262 itself attributes to "two-loop/higher-order radiative QED (the F261 two-loop sector)"** — the
precise object §23.2.6's companion §23.6 finding, F370, later scopes exactly.

$$\boxed{\;\text{recoil}+\text{finite size are sub-MHz to}\sim\text{MHz; the}\sim7\text{ MHz Lamb-shift residual is dominated by two-loop radiative QED, not recoil/size}\;}\tag{R23.14}$$

(F262, 10/10 gates PASS.)

### 23.2.8 Nonlinear and non-perturbative QED (F263)

F263 (2026-07-23) reaches the corner of QED with **no classical Maxwell analogue** — the physics
generated only by integrating out the electron loop. All four results are on the *same* electron
loop already used for F251's vacuum polarization, now with four external legs (the box, Euler–
Heisenberg) or an imaginary part (Schwinger pair production).

$$\mathcal L_\text{EH}=\frac{2\alpha^2}{45m^4}\big[(\mathbf E^2-\mathbf B^2)^2+7(\mathbf E\cdot\mathbf B)^2\big]\tag{EH1, sympy-exact: prefactor }2/45\text{, weight 7}$$

$$\boxed{\;\sigma(\gamma\gamma\to\gamma\gamma)=\frac{973}{10125\pi}\frac{\alpha^4\omega^6}{m^8}\quad(\omega\ll m)\text{ — sympy-exact (Karplus–Neuman), gauge-invariant on all 4 legs, Bose-symmetric}\;}\tag{R23.15}$$

(F263, EH2/EH3.) Field-induced vacuum birefringence — the **nonlinear**, physical effect, distinct
from and consistent with F249's confirmed **zero linear** birefringence of the free photon — has an
exact $7\!:\!4$ ratio between the two polarization eigenmodes (EH4, sympy-exact). Schwinger pair
production falls out of the proper-time integrand's residue structure:

$$\boxed{\;w=\frac{(eE)^2}{4\pi^3}\sum_{n\ge1}\frac1{n^2}e^{-n\pi m^2/eE},\quad E_\text{crit}=m^2/e=1.323\times10^{18}\text{ V/m (rel. err }2.5\times10^{-3}\text{ vs CODATA)}\;}\tag{R23.16}$$

(F263, SC1–SC3; SC3 confirms the rate's Taylor series about $E=0$ is identically zero — a genuine
essential singularity, invisible to any finite order of perturbation theory.) All four EH/SC results
are exact (sympy) except SC2's numerical CODATA comparison; the low-energy light-by-light cross
section is a contact limit, not fit to ATLAS's full-box Pb+Pb observation (different kinematic
regime, explicitly disclosed).

### 23.2.9 All-orders structure: renormalizability, $Z_1=Z_2$, the RG, and the ABJ anomaly (F264)

F264 (2026-07-26) is the chapter's structural closure: not one more loop calculation, but the proof
that the model's QED is a genuine renormalizable theory at **every** order, not merely the orders
computed above. The superficial degree of divergence $D=4-\tfrac32E_f-E_\gamma$ has $\partial D/
\partial V=\partial D/\partial L=0$ identically (sympy) — divergence structure depends only on
external legs, never on internal complexity — leaving exactly three divergent 1PI amplitudes
($\Pi^{\mu\nu}$, $\Sigma$, $\Lambda^\mu$) absorbed by exactly four counterterms $\{Z_1,Z_2,Z_3,
\delta m\}$, at every order, with the four-photon box rendered finite by gauge invariance alone
(explaining why F263's Euler–Heisenberg amplitude needed no counterterm).

$$\boxed{\;q_\mu\Gamma^\mu(p',p)=S^{-1}(p')-S^{-1}(p)\text{ holds at every order (telescoping insertion argument, verified fully symbolic); }q\to0\Rightarrow Z_1=Z_2\text{ uniquely}\;}\tag{R23.17}$$

(F264, R4/R5, sympy-exact.) This forces charge universality $e_R=Z_3^{1/2}e_0$ — every fermion
species carries the same renormalized charge regardless of mass, verified as a literal-zero
difference between two species' renormalized charges despite genuinely different $Z_1,Z_2$
(R6) — and the Callan–Symanzik $\beta$-function is carried **entirely by the photon field**:
$\beta(e)=e\gamma_3(e)$ exactly, with $\beta=e^3/12\pi^2$ reading back F251's own $b_0=4/3$ (R7).
The model-specific structural remark on the Landau pole: $\mu_L\approx10^{277}$ GeV sits **259
decades above** the F107 lattice Brillouin-zone cutoff $\Lambda_a\approx1.9\times10^{18}$ GeV — in
this model the pole lies entirely outside the theory's domain of definition, "a structural remark,
not a resolution of the continuum problem" (F264's own honest framing).

The chiral-anomaly sector threads the Nielsen–Ninomiya no-go rather than evading it. The gauge
current is anomaly-free **structurally**, not by charge-bookkeeping cancellation: the F68/F87
coupling is branch-blind (proportional to $\mathbb I$ in chirality space), so the vector current's
two branch weights are $(+1,+1)$ and the per-branch anomalies cancel identically (A5). The axial
current carries the full anomaly, reached by **two independent exact routes** — Fujikawa's heat
kernel and the shift surface term — agreeing to a factor of exactly 2 (the two chiralities):

$$\boxed{\;\text{Fujikawa: }\lvert\text{coeff}\rvert=\tfrac1{16\pi^2}\text{ (regulator cancels identically); surface term: }\tfrac1{32\pi^2}\text{, D-independent; ratio}=2\text{ exactly}\;}\tag{R23.18}$$

(F264, A3/A4, both sympy-exact, mutually independent.) The BCC walk turns out to be a **minimal**
lattice Weyl fermion — exactly 2 Weyl points per chiral branch in the true (fcc-periodic) Brillouin
zone, not $2^d$ doublers — with the Nielsen–Ninomiya-mandated mirror partner gapped at the band top
($\omega=\pi$) rather than light; the physical electron's *mass* (not an artificial Wilson term) is
the ingredient that breaks the no-go's "exactly conserved chiral charge" hypothesis, a
momentum-space realization of the domain-wall/overlap-fermion mechanism. The measured test:

$$\boxed{\;\Gamma(\pi^0\to\gamma\gamma)=7.749\text{ eV vs PDG }7.80\pm0.12\text{ eV (0.65\%, }0.42\sigma\text{)}\;}\tag{R23.19}$$

(F264, A9 — this single number simultaneously tests the anomaly coefficient *and* the model's colour
count $N_c=3$, F75, Chapter 15: $N_c=2$ gives $-56\%$, $N_c=4$ gives $+77\%$.) F264 also records an
**honest self-correction** of its own motivating framing: it is tempting, but wrong, to attribute the
uncancelled axial anomaly to F250's paired-photon doubler-folding — the anomaly is a fermion-loop
object sampling the whole fermion Brillouin zone regardless of external photon momentum, and what
actually protects it is the mirror-point gapping (A6), a property of the fermion spectrum, not the
photon's; F264 states this correction explicitly rather than letting the two, easily-conflated
mechanisms stand unseparated.

## 23.3 The F277 correction and its consequences (F277, F311, F322)

### 23.3.1 What broke: the momentum-refold defect (F277, correcting S11/S12)

`docs/theory/supersessions.yaml`'s **S11** (2026-08-01, `F272`) and **S12** (2026-08-02, `F277`)
record a real bug, found and fixed in two passes. The defect: a `mod 2π` refold of the shifted
momentum $k+q$ was applied inside several one-loop-integral modules, under the belief that the rule
kernel's period lattice is $2\pi$ per axis. It is not — F267 (Chapter 2) establishes the kernel
$3\Omega_\text{even}^2+k_t^2$'s true period lattice is $\sqrt3\cdot$fcc, so $2\pi$ per axis, $4\pi$
per axis, and the plain fcc vectors are **all not periods of it**, and the refold silently evaluated
the propagator at a genuinely inequivalent momentum. S11 (F272) found and fixed this in one module
(`bgfield_loop`), where the defect was an exact no-op for the Wilson control ($2\times10^{-14}$,
confirming the removal changed nothing spurious) but a real, convergent shift for the rule kernel.

**S12 (F277, 2026-08-02) is the finding assigned to this chapter, and it found the identical defect
surviving in three more modules F272 did not reach, plus a fourth site the original audit missed**:
`qed_vacuum_polarization._fermion_B`, `qed_electron_self_energy._selfenergy_AB`,
`gluon_self_energy._bubble` (unconditional — every call was contaminated, not just one kernel
branch), and `run_d1_vertex_formfactor._Bcoeff_lattice_ff`. F277 verified directly, not asserted,
that no shift of the refold's claimed periods leaves the kernel invariant ($\max|\Delta K|=71.58$ for
the refold's own $2\pi(1,0,0)$, $34.59$ for plain fcc $2\pi(1,1,0)$) while the true period
$\sqrt3\cdot2\pi(1,1,0)$ leaves it invariant to $1.4\times10^{-14}$.

**In vacuum polarization specifically, per the index's own summary, the defect flipped a sign.**
$\Delta=B_\text{rule}-B_\text{cont}$ at $Q=0.3$: under the refold it changes sign between $n=10$ and
$n=14$ and settles at $+1.2\times10^{-2}$; without it, the same quantity converges monotonically to
$-2.121\times10^{-3}$ — opposite sign, six times the magnitude:

$$\boxed{\;\text{refolded: sign-flipping, non-convergent (}\Delta\text{ mean }+3.865\times10^{-3}\text{, spread }1.4484\times10^{-2}\text{); fixed: converges monotonically to }-2.1214\times10^{-3}\text{, spread }1.685\times10^{-5}\text{ (859}\times\text{ tighter)}\;}\tag{R23.20}$$

(F277, §2, verified at $n=10,14,18,22,26$.) The electron self-energy shift is milder (F277's own
term, "milder, and now flat"): `dA_spread` improves $42\times$ ($3.804\times10^{-4}\to
8.977\times10^{-6}$), `dB_spread` $12\times$. The gluon bubble's log-slope ratio (a universality
identity, not a tolerance) goes from $0.9933321$ (0.67% off) to $1.0000542$ — a derived identity
**recovered**, not merely a tighter tolerance met.

$$\boxed{\;\text{What did NOT move: }b_0^\text{QED}=4/3\text{ and }b_0=11\text{ (both exact sympy, no grid, untouched); every affected test still passes: F251 5/5, F258 6/6, F252, F261, F249, F264 (19 checks), F155, F239 — 33 checks re-run, 0 failures, 0 tolerance relaxations}\;}\tag{R23.21}$$

(F277, §6.) This is the sharpest disclosure to carry: **the defect was a line, not a value** —
invisible until the grid resolution $Q>\pi/n$ crosses the corrupted region, so a value-only test on a
coarse grid passes while the bug is live. F277 adds four gate-tier source-level and grid-convergence
tests (`test_bz_period_lattices.py` T6–T9) specifically to guard against this failure mode
recurring.

### 23.3.2 What F277 fixed, and what it did not: the F251/F258/F155 correction (superseded, not this chapter's territory)

F251 (the vacuum-polarization/running-$\alpha$ finding), F258 (electron self-energy), and F155 (a
tadpole/self-energy finding) are **explicitly not among this chapter's fifteen assigned findings** —
`00-plan.md` routes them to appendix A2, the supersession ledger — but this chapter must state
precisely what F277 did to them, per the assignment's own instruction, so that F311's and F322's
corrections (§23.3.3–23.3.4) read as genuine repairs rather than as if nothing had gone wrong. Per
S12's own `findings:` block:

- **F251 (`partially_superseded`).** *Dead*: "every number computed through the refolded
  `_fermion_B`" — the sign-flipped, non-convergent $\Delta$ of R23.20. *Live*: "the one-loop
  vacuum-polarisation construction and the running-coupling derivation. The defect was in a momentum
  refold, not in the physics; F277 re-ran it." $b_0^\text{QED}=4/3$ (exact sympy, no grid) is
  unaffected.
- **F258 (`partially_superseded`).** *Dead*: numbers computed through the refolded `_selfenergy_AB`,
  for the identical reason. *Live*: the self-energy construction — mass renormalization $\delta m$,
  wavefunction renormalization $Z_2$, and the structure of the result.
- **F155 (`partially_superseded`).** *Dead*: numbers reached through the refolded self-energy
  machinery. *Live*: the tadpole sector, recorded EXACT in F155's own status line, untouched.

**None of this chapter's fifteen findings is itself superseded.** Grepping `supersessions.yaml`
found zero hits for F249, F260, F252, F257, F259, F261, F262, F263, F264, F311, F322, F334, F336, or
F370 in any `superseded:` list — confirmed directly rather than inferred, consistent with the task
brief's own instruction. F277 itself, F311, and F322 are the findings that *respond* to the S12
correction, and they are this chapter's own territory.

### 23.3.3 F311: the three completeness-gap numbers were all bookkeeping artifacts, not physics defects

F311 (2026-08-11) is the first response, closing what a standing completeness-report gap (#5) had
flagged for three consecutive reports: three numbers "no report has re-derived." Its Leg A addresses
exactly the worry this chapter's §23.3.1 raises about F251's headline running-$\alpha$ number, B9
(`$\Delta\alpha(M_Z)=0.24\%$ agreement with PDG`) — and answers it not by reading the call graph, but
by **reinstating the removed refold and re-measuring**:

$$\boxed{\;\text{Pi4 (}leptonic\_running\text{, where B9's number comes from) is bit-identical under the reinstated defect; Pi3 (}lattice\_b0\_consistency\text{, what F277 fixed) moves }6880\times\;}\tag{R23.22}$$

(F311, A1.) B9's headline number was never computed through the refolded path at all — S12 is
therefore a **partial** supersession in the precise sense that it reaches Pi3 and not Pi4, and B9's
evidence was never resting on corrected code. F311's second contribution is more consequential: the
$0.24\%$ residual against PDG's leptonic $\Delta\alpha(M_Z)$ **is** the two-loop leptonic term
(Källén–Sabry leading form, **cited**, not derived), not an error:

$$\boxed{\;\text{one-loop}+\text{two-loop (cited constant)}=3.149850\times10^{-2}\text{ vs PDG }3.1498\times10^{-2}\text{: residual }0.245\%\to0.00158\%\text{ — }155\times\text{ improvement, zero fitted parameters}\;}\tag{R23.23}$$

(F311, A2/A3.) F311's remaining legs — ten `candidate` baselines all re-run to zero regressions (a
volatile-key regex bug misfiled timing noise as physics drift for three of them, since fixed), and
the two cosmological-constant "pictures" resolved as chronologically sequential rather than rival —
are Chapter 18/21's territory, not repeated here; only Leg A is this chapter's own content.

### 23.3.4 F322: the same residual re-derived independently, and what F277 actually supplied was the warrant

F322 (2026-08-17, six days after F311, citing it only in a later amendment §6.1) reaches the
identical accounting conclusion — the $0.24\%$ never depended on the refolded path — **independently
and by a different measurement**: rather than reinstating the defect, it perturbs the lattice kernel
by $7.3\times+0.5$ and requires $\Delta\alpha_\ell(M_Z)$ to return bitwise identical, which it does
(`0.03142092800460496`, base and perturbed, to every digit). F322's own framing of what F277 actually
supplied is the sharpest statement in this whole correction sequence:

> "F277 did not change the number, it created its **warrant**."

Because the running is a **subtracted** object $\Delta\alpha(s)=\Pi(0)-\Pi(s)$, Pi3's $q$-flatness
is not merely a diagnostic — it is the direct statement that the lattice leaves $\Delta\alpha$
*itself* invariant, and its measured non-flatness is an error bar on the model's own $\Delta\alpha$
prediction that B9 never had before F277:

$$\boxed{\;\text{post-F277 the lattice contribution to }\Delta\alpha(M_Z)\text{ is bounded at }0.09\text{--}0.22\times\text{ the PDG shortfall and }shrinking\text{ with grid refinement (ratio }0.398\text{); pre-F277 (refold restored) it is }183\text{--}190\times\text{ the shortfall and }flat\text{ (ratio }0.965\text{) — the discriminator of a spurious log}\;}\tag{R23.24}$$

(F322, B9-3/B9-4.) So the pre-F277 "matches PDG to $0.24\%$" headline was **simultaneously right in
value and unwarranted in error bar** — the lattice uncertainty it should have carried was
$\sim190\times$ larger than the agreement it claimed, a defect of *warrant*, not of *number*. F322
then attributes $79.8\%$ of the PDG shortfall to F261's already-derived, sympy-exact two-loop leading
log $b_1=1$ (a coefficient "already in the tree," never before fed into the running):

$$\boxed{\;\Delta\alpha_\ell(M_Z)_\text{model-internal}=0.03148241\text{ (one loop}+b_1\text{ leading log) vs PDG }0.031498\text{: }0.2447\%\to\mathbf{0.0495\%}\;}\tag{R23.25}$$

(F322, §6, B9-5.) §6.1 of F322 (added by amendment) reconciles this $0.0495\%$ explicitly with
F311's $0.00158\%$: they differ by exactly one term, the Källén–Sabry non-log constant F311 imported
and F322 left uncomputed — "neither finding supersedes the other and there is nothing to
adjudicate." F322 also re-derives the electroweak (Weinberg-angle) leg with the model's own,
leptonic-only $\alpha(M_Z)$ rather than PDG's full value, finding the EW residual **doubles**
($+0.222\%\to+0.450\%$) — a factor $2.02$ traced to exactly one missing number, $3.795$ in
$\alpha^{-1}_{\overline{\rm MS}}$: the hadronic vacuum polarization the model defers entirely, the
subject of §23.4's F334.

## 23.4 The hadronic estimate: rho+omega VMD captures 10.2% (F334)

F334 (2026-08-30) confronts the exact gap F322 §7 named — the hadronic piece the model has
otherwise stated *nothing* about (rubric row G3: "NOT claimed, by declared scope") — and supplies
its **first non-imported, quantitative estimate**, using vector-meson machinery the model already
built and validated elsewhere (F103's KSRF pion coupling, F128/F240's $\rho$–$\omega$ degeneracy and
NN universality posit). The construction is a standard narrow-resonance vector-meson-dominance (VMD)
dispersion integral, $\Delta\alpha_V(M_Z^2)=4\pi\alpha/g_V^2$ — the resonance mass cancels
identically — evaluated at the model's own $g_{\rho\pi\pi}=6.0109$ (built from F123's externally-
anchored $f_\pi=92.07$ MeV):

$$\boxed{\;\Delta\alpha_{\rho+\omega}(M_Z^2)=2.820\times10^{-3}=\mathbf{10.2\%}\text{ of the data-driven }\Delta\alpha_\text{had}^{(5)}(M_Z^2)=(276.0\pm1.0)\times10^{-4}\text{ (Davier–Hoecker–Malaescu–Zhang 2020)}\;}\tag{R23.26}$$

(F334, §2.5, V1–V4.) The $\omega$/$\rho$ photon-coupling ratio is fixed **exactly** by the model's
own quark hypercharge assignment ($Q_u=\tfrac23$, $Q_d=-\tfrac13$, Chapter 12's F41/F42), giving
$g_{\omega,\rm EM}/g_{\rho,\rm EM}=3$ over the rationals (V2, sympy-exact) — a standard $SU(3)$-flavour
relation, and what is checked is that the model's own charge assignment reproduces it, not that the
relation itself is novel. F334 honestly self-checks its universality posit against the measured
$\Gamma(\rho\to e^+e^-)$: the prediction undershoots by $31\%$, a downward quench matching the
*direction* (not magnitude) of two independent quenches F240 already found in the NN sector — "a
directional consistency check on the universality posit, not a magnitude one," explicitly not
applied to the headline $10.2\%$ number. Feeding the VMD estimate into F322's EW-leg chain:

$$\boxed{\;\sin^2\theta_W(M_Z)\text{ residual moves }+0.450\%\to+0.427\%\text{ — }10.2\%\text{ of the }\alpha^{-1}\text{ gap closed (}3.795\to3.408\text{) — the same ratio stated two ways, not two independent confirmations (F334 explicitly flags this)}\;}\tag{R23.27}$$

(F334, §4, V6.) F334's own honest accounting of what this is *not*: $\phi$ and heavier resonances
are absent, the $\omega$ is treated as an idealized unmixed isoscalar, the multi-hadron continuum and
charm/bottom contributions are entirely absent, and the narrow-width approximation is a known
underestimate for the physically broad $\rho$. "This is structurally the same barrier the Standard
Model itself faces" — hadronic VP is not computable from local perturbative QFT even for the real
Standard Model; it needs either the data-driven dispersion integral (external, by necessity, for
every precision EW fit) or genuine nonperturbative lattice QCD. F334's own attack-pass review (logged
in its file, 2026-08-30) corrected an overstated "zero imported couplings" framing to name $f_\pi$
and $m_\rho$ as reused external/adopted inputs, and reworded the $\times3$ ratio as confirming the
model's charge assignment against a known relation rather than an independent coincidence — the
corrected text is what this chapter cites above.

## 23.5 Comparison with measurement

The results table below is this chapter's primary content. Every predicted value is computed on the
model's own fields, consuming only $\alpha_\text{em}$ and the lepton masses as external numbers
(§23.1), per Chapter 9's own disclosed no-go.

| # | Quantity | Model | Measured | Agreement | Exactness | Source |
|---|---|---|---|---|---|---|
| R23.1/R23.2 | Tree QED: crossing, Ward, $\langle|\mathcal M|^2\rangle$ (5 processes) | — | — | exact/machine | exact/$<10^{-13}$ | F260 |
| R23.3 | Photon precision: masslessness, luminality, birefringence | see §23.2.2 | see §23.2.2 | PASS | exact/machine | F249 |
| R23.4 | Electron $a_e$, one loop | $\alpha/2\pi=1.16141\times10^{-3}$ | $1.15965218\times10^{-3}$ | $0.15\%$ | exact algebra | F252 |
| R23.5 | Lamb shift, one loop (literature Bethe log) | $1052.19$ MHz | $1057.845$ MHz | $99.5\%$ | quantitative | F252 |
| R23.6/R23.7 | Bethe log + Lamb shift, model-derived | $\ln k_0$: 2--3\%; Lamb $1059.9$ MHz | tabulated; $1057.845$ MHz | $2$--$3\%$; $0.2\%$ | quantitative | F257 |
| R23.8 | IR/Bloch–Nordsieck finiteness | $\mu$-coefficient $=0$ | — | exact | exact | F259 |
| R23.9/R23.10 | $A_2$ (two loop), $a_e$ two loop | $A_2=-0.328478966$; $a_e=1.15963743\times10^{-3}$ | $-0.328478965$; $1.15965218\times10^{-3}$ | machine; $1.3\times10^{-5}$ | exact (VP part model-derived $3\times10^{-10}$) | F261 |
| R23.11 | $A_2(\mu)$, $a_\mu$ QED | $0.765857421$ | $0.765857410$ | $1\times10^{-8}$ | quantitative | F261 |
| R23.12 | Positronium hyperfine | $204{,}387$ MHz | $203{,}389$ MHz | $+0.49\%$ | quantitative | F262 |
| — | Ps para/ortho lifetimes | $0.1245$ / $138.7$ ns | $0.1245$ / $142.05$ ns | exact / $\sim2\%$ | machine (para) / quant. | F262 |
| R23.13 | Hydrogen 21 cm | $1420.49$ MHz | $1420.4058$ MHz | $5.8\times10^{-5}$ | quantitative | F262 |
| R23.14 | Lamb shift, recoil+size complete | $1050.97$ MHz ($+6.87$ residual) | $1057.845$ MHz | see §23.7 | quantitative | F262 |
| R23.15 | Light-by-light $\sigma$, birefringence $7\!:\!4$ | sympy-exact | Karplus–Neuman/Adler | exact | exact | F263 |
| R23.16 | Schwinger $E_\text{crit}$ | $1.323\times10^{18}$ V/m | $1.32\times10^{18}$ V/m (CODATA-derived) | $2.5\times10^{-3}$ | exact structure / quant. value | F263 |
| R23.17–R23.19 | All-orders WT, $Z_1{=}Z_2$, RG, ABJ anomaly | see §23.2.9 | $\pi^0\to\gamma\gamma$: $7.749$ eV | $0.65\%$, $0.42\sigma$ | 14/17 exact, 3 quant. | F264 |
| R23.20/R23.21 | F277 refold fix (VP sign, self-energy, gluon $b_0$) | see §23.3.1 | — | 859$\times$/42$\times$/12$\times$ tighter | measured correction | F277 |
| R23.22/R23.23 | F311: Pi4 untouched; $0.24\%\to0.00158\%$ | see §23.3.3 | PDG leptonic $\Delta\alpha$ | $155\times$ | measured/quant. | F311 |
| R23.24/R23.25 | F322: lattice bound shrinks post-F277; $0.24\%\to0.0495\%$ (model-internal) | see §23.3.4 | PDG leptonic $\Delta\alpha$ | see §23.3.4 | measured/quant. | F322 |
| R23.26/R23.27 | F334: $\rho+\omega$ VMD, $10.2\%$ of $\Delta\alpha_\text{had}^{(5)}$ | $2.820\times10^{-3}$ | $(276.0\pm1.0)\times10^{-4}$ | $10.2\%$ captured | quant., exact sub-piece | F334 |
| — | F336: two-loop LL cross-check (unitarity/dispersion) | $(\alpha/\pi)^2/4$ | matches F261's $b_1{=}1$ | exact | exact, RG-forced consistency | F336 |
| — | F370: Lamb-shift two-loop residual, scoped not closed | Class 1/2 named | — | — | analysis-only | F370 |

## 23.6 What was excluded, and why

**The pre-F277 vacuum-polarization/self-energy numbers (F251, F258, F155 — appendix A2, not this
chapter's own findings).** Fully treated in §23.3.1–23.3.2: the `mod 2π` momentum refold flipped the
sign and inflated the magnitude of the one-loop vacuum-polarization lattice residual, and produced
milder but real drift in the self-energy and a 0.67% error in the gluon-bubble $b_0$ universality
check. All three findings are `partially_superseded` — the numbers computed through the refolded
path are dead; the constructions and the exact algebraic content ($b_0^\text{QED}=4/3$, the tadpole
sector) are unaffected and live. This is not softened here: the sign flip was real, and it is exactly
the kind of defect this monograph's sourcing discipline exists to surface precisely rather than
gloss over.

**A fifth avenue to $\alpha_\text{em}$'s magnitude, attempted from this chapter's own machinery.**
Not attempted anywhere in this chapter's sources — Chapter 9's four-avenue no-go (R9.10) is a
structural obstruction this chapter inherits and works around by consuming $\alpha_\text{em}$ as
measured, not one this chapter's loop machinery could plausibly close (the obstruction is at the
level of the coupling's overall normalization, not its loop structure).

**Hadronic and electroweak contributions to the muon anomaly, beyond QED.** Explicitly excluded per
**CL019** (F261's own claim card, `kind: non_claim`, `status: not_claimed`): "recorded so that
absence is not read as a prediction." This chapter makes no claim about the Standard Model's
experimental muon $g\!-\!2$ tension, which remains an active, disputed area in the literature
independent of anything in this model.

**A full, closed-form two-loop non-log Källén–Sabry constant, derived on the model's own fields
(not imported).** F336 attempted exactly this — extending F261's Källén–Lehmann dispersive
construction from the vertex to the two-point function via the optical theorem — and found it
**cross-checks** the leading-log coefficient (agreeing with F261's $b_1=1$ exactly, though F336's own
attack-pass review found this agreement is largely RG-forced given both external citations are
correct, so its honest value is as an implementation/normalization consistency check, not an
independent physical derivation) while **not deriving** the constant term: two calculations are
missing from the tree entirely (F252's vertex form factor at general $q^2$, currently evaluated only
at $q^2=0$; F259's real-emission calculation, currently soft-limit only), and a structural argument
(§4(b) of F336) shows the Euclidean dispersion shortcut used for the leading log cannot safely be
repurposed for the timelike constant. F336's own falsification criterion, stated for any future
attempt: a value differing from $\zeta(3)-\tfrac5{24}$ by more than a few percent would be "a
genuinely interesting discrepancy worth its own finding," not a bug to paper over.

## 23.7 What is still open

**F334's hadronic estimate is a partial-coverage result, not a closure, and is presented as such.**
It captures $10.2\%$ of $\Delta\alpha_\text{had}^{(5)}(M_Z)$ from two resonances only; $\phi$ and
heavier vector mesons, the multi-hadron continuum, and charm/bottom contributions are all absent by
construction, and the narrow-width approximation is a documented underestimate for the physically
broad $\rho$. F334's own text: "the *majority* of $\Delta\alpha_\text{had}$ is undetermined by the
model." The qualitatively correct route to a real closure — a genuinely nonperturbative computation
of the model's own electromagnetic current–current correlator, in the style of lattice-QCD hadronic
VP calculations, on the model's own real-time quark/gluon dynamics (F86, F94, F317 in Chapter 13's
territory) — is named as the natural next step and explicitly not attempted.

**F370's disclosed two-loop Lamb-shift residual is a genuine, named, unclosed gap, not a vague
"higher order."** F370 (2026-09-05) splits F262's $+6.87$ MHz Lamb-shift residual into two standard
diagram classes and finds both missing from the tree, for different reasons and at different scales.
**Class 1** (pure vacuum polarization / Källén–Sabry-type): reduces, *within this repo's own
dispersive-machinery route*, to exactly the same two missing calculations F336 already named for a
different application (B9's running of $\alpha$) — the general-$q^2$ vertex form factor and the
hard-photon bremsstrahlung phase space — so a future session that builds those two pieces would make
progress on both open items at once. F370's own explicit caveat: this is *not* a claim that no other
route to the local coefficient exists — Källén and Sabry's own 1955 method (direct Feynman-parameter
integration, not the optical-theorem/dispersive route) would not need those two calculations at all,
so the unification is specific to this repo's chosen construction methodology, not universal.
**Class 2** (two-loop self-energy): a structurally different, **larger and more difficult** gap,
untouched by anything in the tree — it needs either a doubly-nested resolvent generalizing F257's
Dalgarno–Lewis construction, or an NRQED hard/soft matched-asymptotic-expansion machinery, neither of
which exists. F370 cites the specialist literature's own record that this class's coefficient
($B_{50}=-21.5561(31)$) "was completed only a few years ago independently by two groups," using the
paper's own description of the expansion's convergence as "very slow… or even nonperturbative"
(Pachucki 2001) — a documented indication, not independently re-verified by this session's own
calculation, that Class 2 is both larger and harder than Class 1.

$$\boxed{\;\text{even a full closure of Class 1 (the tractable, minor piece) would leave the Lamb-shift residual dominated by Class 2, which has no model-native starting point at all}\;}\tag{\text{F370's own conclusion}}$$

**The absolute Brillouin-zone measure for rule-kernel integrals remains open**, independent of the
sign-flip defect F277 fixed. Every number in R23.20–R23.25 is a **subtracted** lattice-minus-continuum
difference on a common domain, which is exactly what makes the comparison meaningful regardless of
this open item — but the midpoint cube $[-\pi,\pi]^4$ is still not a fundamental domain of a
$\sqrt3\cdot$fcc-periodic function, and F267 (Chapter 2) is where this gets settled, not here.

**`test-results/d1_vertex_formfactor.json` is `stale_by_design`** per S12's own baseline record —
the fourth refold site's re-run needs $n=48$, which OOMs the sandbox (2.7 GB, ~90 s per kernel,
exceeding the 45-second cap); the expected shift ($+6.3\times10^{-4}$ at $n=24$) is recorded and the
Wilson control (unchanged to $2\times10^{-13}$) is what makes the fix safe pending that re-run.

**Every claim card resting on this chapter's findings except CL280 and CL288 carries
`falsifier: unset`** — declared debt per `tools/check_claims.py`, not a claim that no falsifier
exists (that would require `falsifier: none`, which needs a structural reason to be named). This is
reported as-is, consistent with how Chapter 11 reported the same debt for its own headline card.

## 23.8 Falsifiers

From the relevant claim cards, at their actual status:

1. **CL280 (F322/F311/F251/F277/F261/F138/F336, the running-$\alpha$ card, `status: contingent`)
   carries `falsifier: stated`, three named, with thresholds**: (i) if the spread of the
   subtracted transverse coefficient $\Delta$ stops falling with grid refinement (ratio
   $\ge0.7$ at $n\in\{20,24,28\}$), the non-flatness is a residual log rather than grid noise and
   the lattice contribution is no longer bounded below the PDG residual — exactly what the
   `refold_control` perturbation demonstrates (ratio $0.965$); (ii) an improved PDG leptonic
   $\Delta\alpha(M_Z)$ moving more than $\sim1.5\times10^{-5}$ away from $0.03148241$ would mean the
   two-loop leading log stops improving on one loop; (iii) a measured $\sin^2\bar\theta_W(M_Z)$
   differing from $0.2317341$ by more than $0.5\%$ falsifies the F138 matching independently of the
   running of $\alpha$.
2. **CL288 (F334, the hadronic VMD estimate, `status: open`, `rolls_up_to: CL280`) carries
   `falsifier: stated`**, but explicitly flagged as "checkable in principle, not in practice today":
   a genuinely nonperturbative computation of the model's own EM current–current correlator
   returning a $\rho+\omega$-region contribution outside roughly $[1\times10^{-3},6\times10^{-3}]$
   would falsify the narrow-resonance VMD proxy — but the model's own lattice-correlator machinery
   does not yet compute this spectral function, so no near-term test exists.
3. **CL019 (F261 + F249, `kind: non_claim`, `status: not_claimed`) carries `falsifier: none`** — by
   construction, since it asserts nothing: "a model silent on the hadronic pieces has said nothing
   about that tension."
4. **CL222/CL224/CL226/CL227/CL228/CL229/CL230 (F252, F257, F259, F260, F262, F263, F264
   respectively — every other headline card of this chapter) all carry `falsifier: unset`**,
   declared debt rather than a stated falsifier or an argued absence — reported as-is, per this
   chapter's own item in §23.7, not silently upgraded or hidden.
5. **F277, F311, F322, F334, F336, F370 issue no claim cards of their own, or (F311, F336) roll into
   cards not primarily theirs** — their internal falsifiers are the declared negative controls each
   finding's own test record carries, verified to turn exactly the declared legs red and no others
   (`can-fail`), the same protocol Chapter 9 already used in place of a claim-card falsifier where no
   claim is issued.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–11's tables.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $v(p,s)=C\bar u(p,s)^\top$ | The positron spinor, the electron's charge conjugate; $C=i\gamma^2\gamma^0$ | §23.2.1 (F260) |
| $\Lambda^\mu(p,p')$ | The one-loop QED vertex correction | §23.2.3 (F252) |
| $F_1(q^2)$, $F_2(q^2)$ | The electric and magnetic (anomalous-moment) form factors; $a_e=F_2(0)$ | §23.2.3 (F252) |
| $\ln k_0(n,l)$ | The Bethe logarithm, here derived from the model's own Coulomb resolvent | §23.2.4 (F257) |
| $f_{IR}(q^2)$ | The shared infrared coefficient of the virtual and soft-real one-loop corrections | §23.2.5 (F259) |
| $A_2$, $A_2^\text{VP}$, $A_2^\text{vertex}$ | The two-loop $a_e$ coefficient and its vacuum-polarization/vertex decomposition | §23.2.6 (F261) |
| $K_1(u)$ | F252's Feynman-parameter kernel, reused to dress the internal photon with F251's spectral function | §23.2.6 (F261) |
| $\mathcal L_\text{EH}$ | The Euler–Heisenberg effective Lagrangian | §23.2.8 (F263) |
| $w$, $E_\text{crit}$ | The Schwinger pair-production rate and critical field | §23.2.8 (F263) |
| $D=4-\tfrac32E_f-E_\gamma$ | The superficial degree of divergence of a 1PI QED amplitude | §23.2.9 (F264) |
| $\{Z_1,Z_2,Z_3,\delta m\}$ | The four QED counterterms; $Z_1=Z_2$ proved at every order | §23.2.9 (F264) |
| $\Delta=B_\text{rule}-B_\text{cont}$ | The subtracted lattice-minus-continuum transverse vacuum-polarization coefficient; the F277/F311/F322 correction's central diagnostic | §23.3.1 (F277) |
| $\Delta\alpha_V(M_Z^2)=4\pi\alpha/g_V^2$ | The narrow-resonance VMD estimate of a vector meson's hadronic-VP contribution | §23.4 (F334) |

---

*One item is tracked in `docs/monograph/GAPS.md` reasoning but not logged as a new numbered gap:
F249's Tier C ("not computable") reference ledger is superseded in substance by F252 (same day),
F261, and F262, without F249's own text being rewritten — per this monograph's standing convention
(findings are written once, superseded rather than rewritten) this is not a hole the documentation
papers over; it is stated plainly in §23.2.2 with F252's own cross-reference as direct evidence this
chapter's reading is not an unsupported inference. No genuine undisclosed gap — a place where a
source asserts something without justifying it, or where an assumption is smuggled in unnamed — was
found in this chapter's fifteen assigned findings; every open item found (F334's partial hadronic
coverage, F370's two-class Lamb-shift residual, the claim cards' `falsifier: unset` debt, the
outstanding `d1_vertex_formfactor.json` re-run) is already disclosed honestly by its own source
finding and is carried forward in §23.7 rather than logged as a new `[G-N]` entry, the same treatment
Chapters 6, 9 and 11 gave their own sources' self-disclosed open questions. No finding, claim card,
module, or test record was created or modified in the writing of this chapter.*
