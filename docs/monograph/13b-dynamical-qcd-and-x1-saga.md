# Chapter 13b — Dynamical Strong-Coupling QCD and the X1 Casimir-Normalisation Saga

*Chapter 13b of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). This is the SECOND HALF
of a chapter split authorised by the plan's §8: the original "Chapter 13: Colour and the strong sector"
carried 49 findings, too many for one file. **13a** (`docs/monograph/13a-colour-structure-and-confinement.md`,
26 findings, read in full for this chapter) covers the qualitative/structural half — why $SU(3)$, why
three colours, and the confinement mechanism. **13b** (this file, 23 findings) continues from there with
the quantitative $\alpha_s$ derivation, the lattice-to-continuum scheme-conversion program, and a genuine
multi-session research controversy — which normalisation convention correctly reads the model's own
transfer-operator identity — that plays out across roughly three months of findings and reaches a real
resolution. Sourced from `findings/F72-no-universal-even-propagator-channel-selection.md`,
`findings/F111b-tree-gauge-su3-ladder.md`, `findings/F124-sqrt-sigma-over-fpi-two-qcd-calibrations.md`,
`findings/F130-blockspin-rg-gauge-gravity.md`, `findings/F144-route-a-alpha-s-dimensional-transmutation.md`,
`findings/F145-route-c-induced-njl-coupling.md`, `findings/F151-scheme-constant-determined.md`,
`findings/F152-ir-coupling-the-irface.md`, `findings/F154-residuals-A-B-built-and-solved.md`,
`findings/F163-wilson-lattice-selfenergy-vertices-28p81-gate.md`,
`findings/F172-residual-algebraic-or-computed.md`,
`findings/F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1.md`,
`findings/F265-bcc-gauge-action-blindness.md`, `findings/F280-d1-subtracted-against-wilson.md`,
`findings/F287-bgfield-apparatus-sound-post-F277.md`, `findings/F305-bcc-rhombic-lpt-vertices.md`,
`findings/F307-action-consistent-d1-and-a-live-refold.md`,
`findings/F308-refold-repaired-and-two-defects-not-one.md`,
`findings/F323-anisotropy-derived-and-d4-casimir.md`,
`findings/F337-l6-decided-native-sweep-outside-bracket.md`,
`findings/F340-strong-cp-l6-bridge-and-nonperturbative-reality.md`,
`findings/F350-ws-mask-cutcell-does-not-explain-d1-slow-convergence.md`, and
`findings/F362-blockspin-fluctuation-eigenvalue-remains-integer.md` — all 23 read in full. Checked
against `docs/theory/supersessions.yaml`: none of these 23 findings is itself named in `superseded:` by
any of the 23 records, but **S22-F298-mixed-matching-C_F-and-the-X1-branch** (F298/F299/F303 → F325;
read in full) is the record whose *resolution* this chapter's Group C narrative builds toward, and
**S21-F94-hypercubic-action-not-the-model-lattice** (F94 → F323/F265) is the record explaining why
Group B's lattice-technical corrections matter at all. Checked against `claims-index.md`: **CL022**
(the headline open tension), **CL252** (the $d_1$ bracket, rolls up to CL022), **CL282**/**CL281**/**CL257**
(the $N_c$/Casimir-branch cards, Chapter 13a's territory, cited not re-derived), **CL128** (F145, `no_go`,
`live`), **CL145** (F163, `no_go`, `open`), **CL069** (F72, `withdrawn` — checked and found to be the
same claims-layer bookkeeping artifact Chapters 8/12/19 already documented, see §13b.1), **CL231**
(F265, `withdrawn` — same artifact, checked below). Notation and results are those of Chapters 1, 2, 4,
11, 12 and 13a — $c_\text{lat}$, $g_s$, $\alpha_s$, $D(\mathbf k)$, the BCC lattice constant $a=2/\sqrt3$,
the rhombic gauge action — extended, never redefined.

## 13b.0 What this chapter establishes, and its one-paragraph statement

Chapter 13a established that an internal colour index of odd dimension $\ge3$ is forced (not chosen)
and that the resulting $SU(3)$ Yang–Mills theory with quarks confines by an explicit, multi-route
mechanism. This chapter asks the quantitative question that mechanism leaves open: *what number is the
strong coupling, and does the model's own bare lattice coupling — derived, not fit, from the rule's
circular $(\mathbf E,\mathbf B)$ rotation alone — actually reproduce the measured $\alpha_s(M_Z)$ once run
down sixteen decades of asymptotic freedom?* The answer, stated in full before the derivation: **yes, to
better than 2%, with the entire residual compressed into one lattice-to-continuum scheme-matching
constant** ($g_s=\tfrac12$ at the lattice scale, F144) — but that scheme constant is not yet itself
derived to a digit, and the honest state of the project's attempt to compute it is a real research
controversy, not a clean derivation. Two distinguishable open items live inside that residual, and
conflating them is the mistake this chapter works to avoid: **X1** (which of two operator-matching
conventions correctly reads $N_c$-dependence off the rule's own $\hat E^2$–$SU(N)$-Casimir identity) is
**resolved** — Chapter 13a's R13a.5 already reports this, and this chapter narrates the multi-finding
search that led there and cites, not re-derives, the resolution (F325). **$d_1$** (the specific one-loop
vertex-form-factor integral that would *pin* $\alpha_s(M_Z)$ to a digit within the branch X1 adopted) is
**not** resolved: the most recent, best-engineered attempt at it (F337, on the genuine BCC gauge action
Group B of this chapter derives) sharpens the tension rather than closing it, and a follow-up (F350) rules
out the leading candidate explanation for why. This chapter presents that honestly, ending in a
genuinely open state for $d_1$ even though X1 itself is closed — the two are different objects, and the
project's own claim cards (CL022, CL252) currently reflect the state as of X1's resolution (2026-08-18),
not the later $d_1$ development (§13b.7's Gap).

## 13b.1 Inputs

**Postulates used.** No new postulates beyond those Chapters 1–13a already established. **P4**
(unitarity) and the BCC connectivity of **P3** underlie the whole lattice-Feynman-rule apparatus this
chapter builds (Group B); nothing here revisits the postulate ledger.

**Prior results used, precisely.** **R13a.1–R13a.3** (the forced $SU(3)$ structure, the forced even
gluon propagation law, and the certified dynamical gluon sector) are the object this chapter's coupling
runs on — Group A's $g_s=\tfrac12$ lock is a statement about *that* gluon sector, not a new construction.
**R13a.9–R13a.15** (the confinement chain — 2D exact area law, colour-magnetic condensate, centre-algebra
string tension, real-time flux tube, the real-space scalar-confinement no-go) supply the objects Group A's
IR-face discussion (F152) and Group D's scale-setting cross-check (F124) both consume: the condensate VEV
$v$ and the dual-Meissner gluon mass $m_D$. **R13a.5** (F324/F325 — the $N_c$ bracket narrowed to
$\{3\}$ by a since-withdrawn upper bound, then reopened to odd $N_c\ne1$ once X1 resolved in favour of the
centre reading) is the result this chapter's Group C narrative is *built to arrive at*, cited rather than
re-derived — this chapter tells the story of the findings (F172, F239, F280, F287, F163, plus F111b's
role) that made F325's resolution necessary and possible, and then continues past it into territory F325
did not touch ($d_1$ itself). **R2.16/R2.17** (`docs/monograph/02-dimensions-and-lattice-selection.md`
— the cubic FFT array is *not* the BCC crystal's true Brillouin zone, roughly 77% coverage, and each
$k$-space average must be classified per observable as a mode sum or a biased BZ-integral stand-in) is
the structural fact underlying every one of Group B's lattice-technical corrections: F265's discovery
that the gauge *action* was built on a simple-cubic composite while the gauge *propagator* was already
BCC is a direct instance of exactly the naive-cubic-array hazard R2.16 names, now discovered independently
in the gauge sector three chapters later.

**Free inputs consumed, stated precisely, per the plan's instruction to be exact about what is derived
versus fit.** This is the chapter's most important accounting question and it does not have a single
clean answer:

1. **The bare coupling $g_s=\tfrac12$ at the lattice scale is derived, not fit** — from the rule's own
   circular $(\mathbf E,\mathbf B)$ rotation (which *forces* equal electric/magnetic stiffness, $\chi=1$)
   composed with the F110 C7 matrix identity ($\chi=1/(4g_s^2)$) — **modulo one still-open normalisation**
   F144's own X1-era correction discloses: the circularity lemma fixes only the electric/magnetic
   stiffness *ratio*, $\chi=1/\Omega(k)$, and $\chi=1$ specifically inherits F101's normalisation choice
   of which $\Omega$ the single-plaquette rotor carries on the BCC dispersion — "two inherited choices of
   one origin," not zero knobs (§13b.2.1).
2. **The lattice scale $\mu_0=\hbar c/a$ is Chapter 17's canonical decision (F79/F107), imported here, not
   re-derived.**
3. **The scheme-matching constant ($q_\ast$, equivalently the finite constant $d_1$) is the single largest
   free input in this chapter**, and it is genuinely open, not merely unfinished — Group C's whole
   narrative is the record of attempting to close it. The model's own tadpole-free structure *brackets*
   it ($q_\ast a\in[1/\sqrt3,1]$, equivalently $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}\in[1,7.98]$,
   F280) without pinning a digit.
4. **Is $\alpha_s(M_Z)_\text{PDG}$ used as an external comparison target, or fed into the derivation?**
   Both, in two logically separate uses that must not be conflated. (a) The **headline comparison**
   (§13b.5, CL022) runs the model's boundary condition $\alpha_s(\mu_0)=1/(16\pi)$ down to $M_Z$ at
   one loop with **no scheme constant applied at all** (the "natural," $\mu_0=1/a$ convention) and
   compares the resulting $0.1195$–$0.11955$ to the measured $0.1175(10)$ — this is the honest,
   zero-additional-parameter prediction, and the resulting $+1.7\%$/$2.1\sigma$ gap is real, not an
   artefact of a missing fit. (b) A **separate, weaker cross-check** (F151 §§S3–S4) folds in the derived
   exact scheme leg ($a_1=\tfrac{11}3$) and scans the model's own *geometric* convention band for
   $q_\ast$ (no fit to $\alpha_s(M_Z)$ anywhere in setting the band's edges) — that band, $\alpha_s(M_Z)
   \in[0.1143,0.1232]$, *brackets* the measured value without using it; only *then*, as a distinct final
   step, is the measured $\alpha_s(M_Z)$ used to *imply* a specific $q_\ast=0.7327/a$ inside that band
   (a genuine one-parameter fit), whose corroboration is that it independently reproduces $\Lambda^{(3)}_{
   \overline{\rm MS}}=347$ MeV against the lattice-QCD-community value $343(12)$ MeV (FLAG) to $1.1\%$ — a
   different observable from the one fit, and therefore a real (if modest) cross-check rather than a
   circularity.

**One documentation-layer correction to note before the derivation, per the plan's binding
cross-checks.** `claims-index.md`'s **CL231** (F265) and **CL069** (F72) both read `status: withdrawn`,
and in both cases this is a mechanical seeding-pass artefact, not a physics withdrawal, of exactly the
kind Chapters 8 (Gap G-6), 12 (Gap G-7) and 19 (Gap G-9) already documented and named a recurring class.
CL231's own body states plainly why: its `withdrawn` verdict was *inferred* from F265's header line
— *"Supersedes the composite-SC field strength in `ca_wmu.plaquette_field_strength`..."* — which
describes F265 superseding **older code**, not F265 itself being superseded; F265's own status line reads
"established (12/12 checks)" and it appears in no `supersessions.yaml` record's own `superseded:` list.
CL069 is the identical mechanical misread: its quoted "supersession/withdrawal banner" is F72's own
`**Status:** Confirmed — 4/4 checks PASS...`, which contains no such banner. Both findings are read and
used as live, established results throughout this chapter (§§13b.2.6, 13b.3.1); no new numbered gap is
logged for this, since it is the same already-documented pattern, now confirmed to recur a fourth and
fifth time.

## 13b.2 The derivation — Group A: deriving $\alpha_s$

### 13b.2.1 The lock, derived: rule circularity $\Rightarrow\chi=1\Rightarrow g_s=\tfrac12$ (F144)

F115 had *assumed* the F101 rotor normalisation $\chi=1$; F144 derives it in three steps. **(1)** The
rule's per-mode step (`ca_wmu._f26_rotation_step`) is an exact circular rotation on the real
$(\mathbf E,\mathbf B)$ pair — orthogonal, unit determinant, equal-diagonal, residuals $<10^{-15}$ on
every mode. **(2)** A sympy-exact lemma: for the quadratic rotor $H=\tfrac a2E^2+\tfrac b2B^2$, the
one-tick flow matrix is orthogonal **iff $a=b$** — a circular rotation *forces* equal electric/magnetic
stiffness. **(3)** The F110 C7 matrix identity (re-verified, residual $=0$ at three couplings): the
1-plaquette dual $U(1)$ link Hamiltonian *is* the compact rotor with $\chi=1/(4g_s^2)$. Combining:

$$\chi=1\ \wedge\ \chi=\frac{1}{4g_s^2}\ \Longrightarrow\ \boxed{g_s=\tfrac12,\quad\alpha_s(\mu_0)=\frac{1}{16\pi}=0.01989}\tag{R13b.1}$$

at $\mu_0=\hbar c/a=1.850\times10^{18}$ GeV (F107). **The correction added at X1's resolution (2026-08-18,
in F144's own header, before F325 was written) is load-bearing for how this result should be read**: step
2's lemma fixes the stiffness *ratio*, not $\chi$ itself — the residual vanishes at $a=b$ for *every* $b$
— so $\chi=1$ specifically requires $\Omega=1$ and is inherited from F101 §7's normalisation of which
$\Omega$ the rotor carries on the BCC dispersion, not a second independent derivation. **A1 therefore
carries two inherited choices of one origin, not zero knobs**, and the open item is exactly which $\Omega$
the single-plaquette rotor should carry (plausibly F155's $q_\ast$, §13b.4.4) — data wants
$\Omega=0.997829$.

(F144 §2, checks A1: residuals $<10^{-15}$/exact/exact. `test_F144_route_a_alpha_s.py`, 5/5 PASS.)

### 13b.2.2 $\alpha_s(M_Z)$: the zero-parameter prediction, and the 19-decade hierarchy (F144)

Standard $\overline{\rm MS}$ running (RK4 in $\ln\mu$, thresholds at $m_t,m_b,m_c$) gives, at $\mu_0=
1.85\times10^{18}$ GeV with **no scheme constant applied**:

| loops | $\alpha_s(M_Z)$ | vs PDG (contemporary, $0.1180$) |
|---|---|---|
| 1 | 0.1195 | $+1.3\%$ |
| 2 | 0.12797 | $+8.45\%$ |
| 3 | 0.12795 | $+8.43\%$ |
| 4 | 0.12798 | $+8.46\%$ |

The loop expansion converges cleanly (2→3→4 spread $<10^{-3}$); the honest converged prediction is
$+8.4\%$, and the 1-loop $+1.3\%$ is a fortuitous partial cancellation against the missing scheme
constant. **Either way, this is a zero-parameter hit on the measured strong coupling from a Planck-scale
boundary value across sixteen decades** (F144 A2).

$$\boxed{\Lambda^{(3)}_{\overline{\rm MS}}=529\text{ MeV (vs FLAG }343(12)\text{, }\times1.54); \quad N_\text{pred}=\Lambda^{(3)}/\mu_0=2.9\times10^{-19}\text{ vs F119's measured hierarchy }5.5\times10^{-19}\ (\times1.9)}\tag{R13b.2}$$

F119's own sharp negative — "the gap mechanism can't make the fermion-mass hierarchy $N$ from $O(1)$
couplings; no running channel exists" — is answered directly: the channel is asymptotic freedom itself,
$N\sim e^{-1/(2b_0\alpha_0)}$ at $\alpha_0=1/(16\pi)$, and it lands the 19 decades *because* the rule fixes
$\alpha_0$ where it does (F144 A3). Running the *measured* $\alpha_s(M_Z)$ back up to $\mu_0$ isolates the
entire discrepancy in one number, $\Delta(1/\alpha)=0.64\Leftrightarrow\Lambda_\text{scheme}/\Lambda_
\text{rule}=1.78$ — near-continuum, sixteen times closer than the Wilson lattice-action value of $28.81$
(F144 A4; this is the number Group C's whole narrative attacks).

### 13b.2.3 Route C: the NJL coupling as an induced coupling, and a bare-coupling no-go (F145)

F116 had identified the mechanism (integrating out the dielectric/dual-Meissner gluon induces the NJL
four-fermion coupling) but left the exact coefficient open, quoting $G\sim\tfrac49g_s^2/M_g^2$. F145
computes it exactly and finds the picture is sharper, not merely more precise. **The exact Fierz
identity**, worked in the full $24$-dimensional one-quark space (Dirac$_4\times$colour$_3\times$flavour$_2$),
gives

$$\boxed{c=\tfrac29\text{ exactly, in all four chiral channels}\ (8\times10^{-17})}\tag{R13b.3}$$

which is exactly $\tfrac49_\text{colour}\times1_\text{Dirac}\times\tfrac12_\text{flavour}$ — a factor 4
below NJ4's quote, and it fixes the induced contact term as $G=\tfrac{g^2}{9M_g^2}$. Two consequences: the
induced interaction is exactly $U(2)_L\times U(2)_R$ symmetric (the pion's Goldstone structure is thereby
traced to the gauge sector, not modelled independently), and — the decisive negative — with the
**derived** bare coupling $g_s^2=\tfrac14$ and the **measured** dual-Meissner mass ($m_D=0.532$–$0.727$,
F88/F117), the momentum-resolved gap kernel gives $R\equiv G/G_c=0.075$–$0.10\ll1$: **the bare rule
coupling cannot break chiral symmetry** (F145 N3, a decisive negative, not merely unverified). But
replacing $g^2\to g^2(\mu(q))$ with Route A's own running at the exchange virtuality gives
$R_\text{running}=2.6$–$15\gg1$ at both measured $m_D$ values: **chiral symmetry breaking is forced by the
same RG growth that produces the $\alpha_s$ hierarchy** — the condensate switches on at a derived rung of
the Route-A ladder, not by fiat (F145 N4). The F77 fit point ($G/G_c=1.277$) sits squarely inside the
running band, and the residual that fixes the exact point is the same nonperturbative IR coupling F151/
F152 develop next.

(F145: 5/5 PASS. N1 machine-exact, N3 decisive negative, N4 structural positive. `CL128`, `no_go`, `live`,
`falsifier: unset`.)

### 13b.2.4 The scheme/scale constant splits into two faces (F151, F152)

F151 determines the object F144-A4, F145-N5 and F124 §5 each met as "one open coefficient" and finds it
has structure. **S1 — the rule's coupling is the V-scheme (static-potential) coupling, exactly**: F110's
$\lambda=0$ potential is exactly $V(R)=\tfrac{g^2}2q^2R$ (re-verified, deviation $0.0$), and the model's
Gauss/constraint sector is spectral-exact so the tree-level Coulomb carries no lattice renormalisation —
a coupling defined through the static-source energy *is*, by definition, the V-scheme coupling. **S2 —
this is why the model's scheme constant is small**: the Wilson action's $28.81$ is dominated by the
compact-link tadpole, which the model's spectral-exact kinetic term structurally lacks (F155-A0,
$u_0\equiv1$ exactly). **S1 gives the exact one-loop $V\to\overline{\rm MS}$ conversion**,

$$a_1(n_f)=\frac{93-10n_f}9,\qquad a_1(6)=\frac{11}3\ \text{(exact rational)}\tag{R13b.4}$$

**S3 — the residual bracket, from the model's own geometric conventions alone, brackets the measured
value with zero fit**: $q_\ast a\in[1/\sqrt3,1]$ (cutoff-wavenumber vs rotation-rate conventions) gives
$\alpha_s(M_Z)\in[0.1143,0.1232]\ni0.1180$. **S4 — fixing $q_\ast$ by the measured value alone gives
$q_\ast=0.7327/a$**, and the corroboration is a second, independent observable landing close:
$\Lambda^{(3)}_{\overline{\rm MS}}=347$ MeV vs FLAG's $343(12)$ ($\times1.011$).

F152 develops the physical content of the object F151-S5 split off — the IR face of the coupling, distinct
from the UV scheme constant. **The self-consistent chiral gap equation requires $\alpha_\text{eff}^\ast=
0.376$ ($m_D=0.532$) / $0.411$ ($m_V=0.727$) $\approx0.39$**, and its scale is not free: the gap-massive
gluon propagator freezes the running once $\mu\lesssim m_D$, so $\alpha(0)$ is finite — the model sits on
the **saturating/decoupling branch**, the same branch real QCD's process-independent charge occupies
($\hat\alpha(0)/\pi=0.97(4)$, Cui–Zhang–Binosi–Roberts, gluon mass gap $m_g=0.50(20)$ GeV) — by mechanism,
not by fit, since the model *generates* its own gap ($m_D$, F88/F117) at the same $\sim0.5$ GeV scale.
$\alpha_\text{eff}^\ast\approx0.39$ sits squarely in the continuum frozen-coupling window ($0.3$–$0.5$,
MOM/V/APT schemes). F152 also corrects F150's earlier framing: $\lambda_6$ (the lepton-sector sextic
brake, Chapter 15) and $\chi$SB both belong to this IR face, not to the UV scheme constant that F151
determined.

$$\boxed{\text{UV face: }a_1=\tfrac{11}3\text{ exact}+q_\ast\text{ in a derived }\sqrt3\text{ band bracketing measurement}.\quad\text{IR face: }\alpha_\text{eff}^\ast\approx0.39\text{, the gap-saturated frozen coupling, on QCD's own branch}}\tag{R13b.5}$$

(F151: 5/5 PASS, S1/S2 exact/machine, S3/S4 PREDICTION/corroboration. F152: 5/5 PASS, an interpretive
consolidation on F151-S5, no independent claim card of its own.)

### 13b.2.5 Both residuals built and solved — Residual B closes, Residual A's shortcut fails (F154)

F154 builds the machinery both faces needed and reports honestly which closed. **Residual B (the IR gap,
solved).** The full **nonlinear** self-consistent gap equation — not F145's linearised $M\to0$ eigenvalue
— is built and solved by FFT convolution plus under-relaxed iteration. Fixing the coupling to reproduce
the physical constituent mass $M(0)=1.50$ (311 MeV, F77/F124) gives $\alpha_\text{eff}^\ast=0.3764$
($m_D=0.532$) / $0.4111$ ($m_V=0.727$) — **identical to F151-S5/F152 to three digits**, now as a
converged ($\sim130$-iteration), $L$-stable ($0.3764$ at $L=16,24,32$ to four digits) fixed point rather
than a stated number. The naive perturbative running **overshoots** to $M(0)\approx1400$–$1570$ MeV — a
factor $\sim5$ — confirming that $\alpha_\text{eff}^\ast$ is genuinely set by saturation, not by the
running evaluated at the gap scale (F152's branch statement, now quantified).

**Residual A (the matching scale $q_\ast$), cheap shortcut ruled out.** The obvious shortcut — reading
$q_\ast$ off a propagator log-moment over the BZ — fails cleanly: the converged moments are *UV* scales
($\langle\ln K\rangle=2$ exactly $\Rightarrow q_\ast^\text{bare}=e/a=2.72/a$, above F151's band), and the
only weight that dips into the band ($1/K^2$) is IR-divergent and grid-dependent (not converged,
$1.01\to0.65$ as $n:24\to64$). **The lesson is physical**: $q_\ast$ is the UV-*finite* lattice$-$continuum
subtraction — the genuine $d_1$ integral — which no bare moment can represent; the full one-loop
background-field computation is required, exactly as F151 §8 said.

$$\boxed{\text{Residual B: solved, converged, }L\text{-stable}\ (\alpha_\text{eff}^\ast\approx0.39).\quad\text{Residual A: cheap route excluded; the full loop integral is the last freedom in the whole strong sector}}\tag{R13b.6}$$

(F154: 5/5 PASS. B1–B3 solved/numeric/numeric. A1 an honest negative.)

### 13b.2.6 The SU(3) Casimir ladder and tree-gauge machinery (F111b), and F72's pre-history

F111b (2026-06-07, recovered and renumbered 2026-07-31 at a roadmap close-out) builds the two scope items
F110 had left open: **(I)** a genuine 3D tree-gauge Kogut–Susskind construction (Gauss's law solved exactly
by maximal-tree elimination, since the planar height trick does not extend past 2D), and **(II)** the
**SU(3) Casimir ladder**, $C_2(p,q)=\tfrac13(p^2+q^2+pq+3p+3q)$, giving Casimir scaling $\sigma_R/\sigma_3=
C_2(R)/C_2(3)$ against the $\mathbb Z_3$ centre theory's N-ality-only law — exactly the F98–F101 A-vs-C
dichotomy made computable rather than argued. The **SU(3) character rotor**
$H=(g^2/2)C_2-(\lambda/2)(\chi_F+\chi_{\bar F})$ extends F101's $U(1)$ rotor to SU(3) irreps, and its
strong-coupling law is *identical* to the $U(1)$ rotor's under F110's map $\chi=1/(4g^2)$. **This module
is the object that F294/F298/F299 needed to settle the Casimir-vs-centre reading and never cited** —
its own header records the correction, added at X1's resolution: the T7 "identical" comparison holds only
because $C_Fd_F=(N^2{-}1)/2=4$ coincides with the four boundary links at $N=3$, not because of anything
about the group, so it is **not** independent confirmation of $\chi=1/(4g^2)$ and carries no $N_c$
selector — F325 §§X3–X4 (cited in Chapter 13a §13a.3.3) is what actually resolves the matter using this
same module's genuine SU(N) Casimir apparatus.

**F72's pre-history, for context.** Three weeks before F91 forced the gluon's even propagation law
(§13a.2.2), F72 (2026-06-01) asked whether the paired/even-law photon propagator could be adopted
universally, retiring the chiral law for W/Z/gluon. Its answer — no, and specifically that the gluon
"as currently constructed" (a σ-vector bilinear, F43/F29) is chiral by construction, with an even-law
gluon flagged as "a possible future re-derivation, not a swap" — is exactly the question F91 (2026-06-04,
three days later) and F317 (2026-08-16) went on to *force* rather than leave open, as Chapter 13a §13a.2.2
narrates in full. F72 is not superseded in any formal ledger record (§13b.1), but its substance is
superseded by R13a.2's forcing chain; it is included here, per the plan's finding assignment, as the
last recorded state of the question before the forcing argument existed.

## 13b.3 The derivation — Group B: the lattice-technical corrections underlying every loop calculation here

Every number in Group A's scheme-constant discussion and every number Group C computes rests on a lattice
Feynman-rule apparatus. This group is the record of discovering that apparatus was built on the wrong
lattice, and fixing it — disclosed defects and corrections, not triumphs, per the plan's framing.

### 13b.3.1 The gauge action was cubic while the propagator was BCC (F265)

A 2026-07-29 audit reported "the gauge channels are cubic only, matter is BCC only" — F265 corrects this:
the split runs between **propagator and action**, inside each gauge sector, not between sectors. Every
gauge *propagator* (γ, W, Z, gluon) was already BCC, evaluating $\omega^\pm$ from the genuine BCC
dispersion; F91/F166/F250 (Chapter 13a's forcing chain) rest on this and are untouched. But every gauge
*action* was built by first collapsing the eight BCC links into three straight composite $\pm x,\pm y,\pm z$
links of length 2, then taking ordinary square plaquettes — a simple-cubic construction hiding inside a
BCC-labelled codebase.

**The defect is a real, measured no-go, not a cosmetic relabelling.** Three vectors with all-odd
components cannot sum to zero, so the BCC nearest-neighbour graph has **no 3-bond closed loop at all**;
the genuine minimal gauge loop is a **4-bond rhombus**, on 4 link axes, in 6 $\langle110\rangle$-normal
orientations — not 3 composite links with $\langle100\rangle$ normals. Setting the three composite links
to the identity requires only three of the four $\langle111\rangle$ axis fields to vanish; **the fourth is
completely free** — on such a configuration the composite action reads exactly $0$ while the genuine BCC
plaquettes are 100% non-trivial (Wilson density $0.999$). The composite construction resolves only
$2N_s$ of $3N_s$ curvature-carrying directions asymptotically — **one third of the field strength was
missing, at every field amplitude tested**, not merely at strong coupling.

$$\boxed{\text{The composite simple-cubic gauge action has an exact kernel — one }\langle111\rangle\text{ link axis is invisible to it — and misses asymptotically }1/3\text{ of the curvature; both actions share the identical classical continuum limit, which is why no weak-field check ever caught it}}\tag{R13b.7}$$

Every quantity measured off the composite or an SC/hypercubic action is re-scoped, not invalidated: the
$d_1$ chain (F144/F151/F152/F154/F155/F162/F163/F239, all pre-dating F265) is "measured on an action that
is blind to 1/3 of the curvature," which is exactly the motivation for Group B's remaining corrections.

(F265: 12/12 PASS. `CL231` — see §13b.1 on its `withdrawn` bookkeeping status.)

### 13b.3.2 The genuine BCC lattice Feynman rules, derived not transcribed (F305)

F305 executes F265's own named remedy: the rule's minimal loop is the 4-bond rhombus, not a square, so the
"vertices unchanged, only the propagator differs" premise `lpt_vertex`'s docstring stated was itself
false. Using the same multilinear-link-expansion method as the existing hypercubic generator (one code
path for both actions — the same enumeration parameterised by the loop word), the rhombic action's
2-point form reproduces $\delta_{ij}\sum_l\hat k_l^2-\hat k_i\hat k_j$ **exactly** (deviation $2\times
10^{-16}$), the 3-point vertex reaches the Yang–Mills continuum limit to $O(a^2)$ (deviation $4.6\times
10^{-9}$), and the lattice Ward identity holds to $<10^{-13}$ at finite $a$.

**A genuine, previously invisible physics question surfaces: one extra massless mode.** $\Gamma=S\delta-
\hat k\hat k^{\mathsf T}$ has one zero eigenvalue (the gauge mode) and **four** degenerate massless
eigenvalues, where continuum 4D Yang–Mills has three. The extra one is the unique redundant link-axis
combination $\hat n=\tfrac12(-1,1,1,1)$ with $\sum_in_id_i=0$; it is exactly transverse and massless to
$3.2\times10^{-15}$, and the 3-gluon vertex does *not* annihilate it. **The fork is resolved by an exact
isometry, not by fiat**: the Cartesian projector $P^a{}_i=d_i^a/2$ satisfies $PP^{\mathsf T}=\mathbb I$
exactly, so only the branch that projects $\hat n$ out has a continuum limit that is 4D Yang–Mills at all
— corroborated by a $b_0$ trend that lands on $11$ for the projected branch and on the *wrong sign*
for the unprojected one.

$$\boxed{\text{The rhombic BCC action's lattice Feynman rules reproduce the correct 2-point form exactly and the 3-point vertex to }O(a^2)\text{; a genuine extra massless mode is isolated and resolved by an exact isometry argument, corroborated (not merely argued) by a sign-correct }b_0\text{ trend}}\tag{R13b.8}$$

A genuine fundamental domain for the gauge side (the reciprocal-lattice Wigner–Seitz cell, cube/BZ$=4$
exactly by primitive-cell volume) falls out as a byproduct, removing rather than merely bounding the
F267-class domain hazard on this side. F305 also states, honestly, the gap this opens: the rhombic
action's own quadratic form and the F26 rotation-law propagator agree only to $1.4\times10^{-5}$ at
$|k|\sim10^{-2}$ and differ by up to $86\%$ at generic $k$ — which object is "the rule's gauge action" at
finite lattice spacing is a decision the model owes itself, and F337 (§13b.4.4) is where it gets made.

(F305: 9/9 PASS + control. Registry `F305-bcc-rhombic-vertices`, tier gate.)

### 13b.3.3 The estimator built, and a live refold defect found (F307, F308)

F307 assembles F305's vertices with F280's slope-normalised estimator (§13b.4.3) into an
**action-consistent** $d_1$ computation — vertices *and* propagator from the same action, on the same
side's own genuine fundamental domain. **The number is explicitly not quotable at $n\le20$**: the BCC
side's $b_0$ recovery ($0.41$–$0.49$) is still climbing, the two normalisations diverge with $n$ rather
than converging, and feeding the midpoint into the budget gives $\Lambda\approx14.27$ — outside F280's
own bracket — which F307 reads correctly as the estimator reporting non-convergence, not a falsification.

The unified path also surfaces a genuine defect: `lpt_selfenergy._pi_bgfield` wraps momenta into
$[-\pi,\pi)$, harmless for the $2\pi$-periodic propagator but flipping the sign of the ghost form
factor's $4\pi$-periodic $2\sin(k/2)$ — the fifth instance of the F272 refold class, invisible at small
$Q$ and coarse grids, i.e. exactly where a cheap sanity check would run.

**F308's audit finds the diagnosis was half right.** Careful re-measurement finds **two** independent
folds, not one, behaving oppositely: the branch F307 measured (`fp='leading'`) has a large effect (factor
2, from a sum of two $4\pi$-periodic terms folding into a difference), but is a branch nothing published
ever used; the branch every committed rule constant actually used (`fp='exact'`) is *immune* to that
mechanism entirely (a global sign cancels in the contraction) but carries a **second, smaller, genuinely
real** fold — F272's original defect, still resident four findings later, in the rule propagator itself
(which has no period at all under $2\pi$, $4\pi$, or $8\pi$ axis shifts, since it mixes an fcc-periodic
spatial dispersion with a continuum time leg). F308 derives the exact firing condition ($Q\ge\pi/n$),
repairs the module with a single documented switch, and confirms the repair changes committed numbers by
only three of twenty-four sweep rows, at the $10^{-4}$ level, not the factor-2 level the first diagnosis
implied.

$$\boxed{\text{The }d_1\text{ estimator is built action-consistently; its first live refold defect turns out, on audit, to be TWO independent defects on different branches, one large-but-irrelevant and one small-but-real; the repair moves published numbers negligibly, and the number is left explicitly unquotable at this grid}}\tag{R13b.9}$$

(F307: 8/8 PASS + control, S3 red by design. F308: R1–R6, repaired path agrees with F307's independent
reference to $6.8\times10^{-16}$.)

### 13b.3.4 The lattice anisotropy is derived, not chosen (F323)

A separate, standing convention — `beta_t = beta_s` on the 3+1D Monte-Carlo confinement sampler — is
derived rather than left as a flagged non-derivation. F313's proof that the update tick is the
**primitive**, unrefinable unit of `ker(det)` licenses treating $a_t$ as a fixed quantity to be computed
rather than a continuum limit to be taken (but supplies no value by itself — the previous session's
speculation that primitivity might *fix* $a_t$ is explicitly withdrawn here in favour of this weaker
statement). Its **value** comes from isotropy of the weak-field limit: expanding the two BCC loop classes
(6 rhombi, 4 mixed space-time rectangles) to $O(\Phi^2)$ using two exact closure identities of the BCC
geometry ($\sum_pm_pm_p^{\mathsf T}=4\mathbb I$ over the rhombus half-normals, and the identical identity
over the four $\langle111\rangle$ link axes) gives

$$\boxed{\beta_t/\beta_s=4\lambda^2/a_t^2=\frac4{3c_\text{lat}^2}=4,\qquad\xi=1/c_\text{lat}=\sqrt3}\tag{R13b.10}$$

— a factor $4/3$ away from the naive hypercubic relation $\beta_t/\beta_s=\xi^2$, traceable to the
rhombus's area $2\sqrt2$ against the mixed rectangle's $\sqrt3$; a naive hypercubic substitution would
have been wrong by a third. The result is measured, not merely derived, by placing a constant-field
abelian configuration on the lattice and reading $S_B/S_E$: the residual is exactly the closed-form
quartic term $1/16\,g^2$ to four digits over a factor-2 range in $g$, and one Richardson step gives
$3.99999999908$, residual $2.3\times10^{-10}$.

With the anisotropy fixed, F323 runs F299's own specified 3+1D d=4 Casimir-scaling successor (`sigma_6/
sigma_3` etc., against the SU(3) Casimir ratios $5/2$, $9/4$, $9/2$) for the first time — a genuinely new
capability (traces from an $R\times T$ loop matrix, checked against explicit representation matrices, not
just against the polynomials that produced them). **The result is explicitly labelled preliminary**:
three configurations, no error bars, small loops — the readings sit within a few percent of the exact
Casimir line at small $R$ and fall progressively below it at the largest loop tested, most steeply for
the decuplet, which is the *direction* screening would take (triality-0 representations must eventually
break from Casimir scaling), but the finding is explicit that this is not yet a measurement of where.

(F323: 28/28 PASS, five controls, each verified against a distinct measured red set.)

### 13b.3.5 A better mask is built and verified — and changes nothing about the convergence problem (F350)

Anticipating §13b.4.4's finding that $d_1$ leg 3 converges anomalously slowly, F337 named a specific,
checkable mechanism: the BCC side's sharp 0/1 Wigner–Seitz-cell mask is a textbook first-order "staircase"
discretisation of a smooth boundary, unlike the cube side's exact periodic domain. F350 builds the named
remedy — an adaptive-octree cut-cell mask with exact interval-bound voxel classification — and verifies it
**in isolation** to be genuinely, dramatically better: against the exact target volume fraction $1/4$
(F305's own G7 result), the sharp mask's error falls as $n^{-1.07}$ while the smoothed mask's error is
$500$–$2500\times$ smaller at every $n$ tested and already sits below the physics integral's own expected
$O(1/n^2)$-class floor without needing to shrink further.

**Swapped into the actual loop integral, it changes nothing measurable.** Re-run natively at $n=12$–$40$,
the fitted convergence exponent on the BCC side is $0.92$–$1.14$ — statistically the same as F337's
sharp-mask result ($1.11$–$1.35$), still more than a factor of two below the Wilson side's own $\approx2.5$–
$2.8$; the extrapolated $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3$–$34.1$ is statistically
unchanged from F337's own $31.3$.

$$\boxed{\text{The named remedy is built and independently verified to be far more accurate in isolation, but wired into the actual estimator it does not move the anomalous slow-convergence rate or the extrapolated value at all — F337's own stated exhaustion condition for the "still not converged" reading now fires}}\tag{R13b.11}$$

This is a genuine null result about a specific, checkable hypothesis — not a defect in the mask, and not
evidence the mask was unnecessary work; it is evidence that whatever is causing $d_1$ leg 3's slow
convergence is *something else* (candidates F350 names but does not investigate: the vertex form factors'
own behaviour near the BZ boundary, some other feature of the projection branch, or a genuine physical
breakdown of the monotonicity assumption F280 named as a live possibility). §13b.4.4 and §13b.7 return to
what this means for the honest state of $\alpha_s(M_Z)$.

(F350: gate-tier isolation PASS + one control; native re-run committed as a `result_dump`, not gate-tier,
matching F337's own convention for non-quotable numbers.)

## 13b.4 The derivation — Group C: the X1 Casimir-normalisation saga

This is the chapter's research-narrative centrepiece, in the sense Chapter 10 established for the
photon–fermion investigation: findings correcting each other over real time, presented in the order they
actually happened, ending — unlike Chapter 10's still-open story — in a genuine resolution.

### 13b.4.1 What came before: the S22 supersession record, read for context

`docs/theory/supersessions.yaml`'s **S22-F298-mixed-matching-C_F-and-the-X1-branch** (2026-08-18)
supersedes F298, F299 and F303 — none of them findings this chapter is assigned, and all routed to the
monograph's appendix A2, but they are the immediate prior chapters of the saga this chapter's own Group C
findings continue from, and the record must be read to understand why F172/F239/F280/F287/F163 needed
attacking in the first place. **What S22 records**: F298 (2026-08-05) evaluated the F110 C7 identity as
$\chi_k=s(k)^2/(4g^2C_2(\text{antisym }k))$ — the **abelian** rotor's $\mathbb Z_N$-symmetric residue
against the **$SU(N)$ gauge theory's** quadratic Casimir — a *mixed* matching between eigenvalues of
operators belonging to different theories, and the sole origin of a Casimir factor $C_F$ that created the
fork between two adopted $g_s$ values six decades apart. **Under either self-consistent evaluation** (both
sides abelian, or both sides $SU(N)$), $\chi=1/(4g^2)$ identically, for every $N$ and every irrep, exact
over $\mathbb Q$ — and the mixed evaluation is not even a self-consistent rival convention, since off the
$k$-string tower it is level-dependent at $N=3$ too (F324's sextet leg, $\chi_6=3/10$ against the tower's
$3/4$), and **undefined** for the adjoint, decuplet and 27 (the $\mathbb Z_3$ rotor's $s^2=0$ against
$C_2\ne0$ — assigning zero electric cost to a triality-0 link). S22's supersession is by **F325**,
which is Chapter 13a's R13a.5 and is cited, not re-derived, here (§13b.4.6).

### 13b.4.2 The framing question: is the shared residual algebraic or computed? (F172)

Before the Casimir/centre dispute above had crystallised into the sharp X1 fork, F172 (2026-06-29) asked a
broader structural question that turns out to bear directly on it: the roadmap had reduced a whole cluster
of open nonperturbative numbers ($\lambda_6$, the condensate angle, $G/G_c$, the scheme constant, the IR
coupling) to "one nonperturbative IR number." F172's audit finds this framing is wrong on its face — the
members are manifestly distinct values — and that what is actually shared is **one coupling** ($\alpha_
\text{eff}^\ast$) dressed by exact lattice geometry, with the algebraic-connection question splitting
cleanly into two halves with **opposite** prospects: the **shape** residual (the lepton condensate angle,
Chapter 15's territory) has a genuine path to an exact algebraic value (an exact $\pi/4$ anchor plus a
self-consistency structure the model has already solved elsewhere, F92); the **scale/scheme** residual —
this chapter's $q_\ast$/$d_1$ — looks **computed, not algebraic**: the model removes the *large*
transcendental piece (Wilson's tadpole, structurally absent) and even lands a rational $C_{\overline{\rm
MS}}=131/66$, but the residual digit lives in an action-specific finite vertex constant that a proven
moment-insensitivity theorem (F155) shows is not accessible to any closed-form moment integral, and the
closest physical analogue (the real-QCD frozen coupling) is itself a measured, not algebraic, quantity.

$$\boxed{\text{The shape and scale residuals are different objects with opposite prospects for exact closure: the model's own track record of solving self-consistency fixed points exactly is relevant to the SHAPE residual (Chapter 15) but gives no reason to expect the SCALE/scheme constant this chapter attacks to be anything but a computed }O(1)\text{ number}}\tag{R13b.12}$$

This framing is confirmed, not merely echoed, by everything that follows in this section: nobody in the
$d_1$/X1 saga ever finds an exact closed form for $q_\ast$ or $d_1$ — every genuine advance is either an
*exact* piece being split off cleanly (F239's $a_1=\tfrac{11}3$) or a bracket being tightened numerically
(F280's band, F307/F308/F337's convergence work).

(F172: 4/4 PASS, an analysis/reframing finding, no new physics input.)

### 13b.4.3 The scheme conversion factorises exactly (F239), and the apparatus is certified sound but restricted (F287)

F239 (2026-07-03) sharpens F235's earlier blanket claim that "the scheme conversion is the shared open
$d_1$" by showing the conversion **factorises exactly**:

$$\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}=\underbrace{\exp\!\Big(\frac{a_1(6)/4\pi}{2b_0^\alpha}\Big)}_{V\to\overline{\rm MS}\ =\ 1.299\ \textbf{(EXACT)}}\times\underbrace{\frac1{q_\ast a}}_{\text{rule}\to V\ =\ 1.365\ \textbf{(OPEN)}}=1.773\tag{R13b.13}$$

The first factor — the true renormalisation-*scheme* conversion the F110/F117 rotor structure the original
prompt pointed to actually determines — is **derived exactly**; only the second, a lattice-to-continuum
one-loop *matching*, is the genuinely shared open $d_1$. F239 further localises the open leg: using the
F162 subtracted transverse coefficient, the rule's own propagator-driven finite shift is only $\approx11$–
$16\%$ of Wilson's equivalent shift, so the open leg is **vertex-dominated**, not propagator-dominated —
pinning which diagram remains to be computed (the lattice 3-gluon+ghost vertex form factors).

F287 (2026-08-02) then certifies the underlying background-field apparatus itself, discharging a
prerequisite the completeness ledger had explicitly flagged rather than skipped. Every F162 gate passes;
the refold defect chased by F272/F277 is confirmed absent everywhere it could recur in this module, on a
**genuinely stronger** 4D statement than F277's own 3D one (the Euclidean-time leg carries $k_t^2$, which
has *no* period at all — a fourth direction the earlier 3D sweep could not have checked); and $b_0=11$ is
recovered *numerically* to 95%, not merely proven symbolically, with both the rule and Wilson deficits
falling as clean power laws in the grid spacing and the rule beating Wilson by $5.3$–$5.7\times$ at every
grid tested (an independent sighting of the model's own near-perfect-action property, F129/F130). **But
F287's central verdict is a restriction, not a green light**: the apparatus is sound *for subtracted
differences only*; the absolute normalisation needed for $d_1$ itself is not — the midpoint cube is not a
fundamental domain of the true $\sqrt3$-fcc-periodic function (the same F267-class hazard R2.16 names) —
and $d_1$ must instead come from a subtracted formulation against a known reference.

(F239: 3/3 PASS. F287: 6/6 apparatus checks PASS, F162's own 3/3 gates PASS.)

### 13b.4.4 $d_1$ formulated subtracted against Wilson: the three-leg budget (F280), and the Wilson-side transcription (F163)

F280 (2026-08-05) takes exactly the exit F287 named: rather than settling the fundamental-domain question,
formulate $d_1$ **subtracted against the known Wilson anchor** $\Lambda_{\overline{\rm MS}}/\Lambda_L=
28.8086$, so that no absolute lattice normalisation ever appears — every term in the master identity is a
difference. A slope-normalised estimator (dividing the loop integral's log-derivative by its own measured
slope rather than the analytic coefficient) is proven **exactly invariant** under an overall measure
factor, algebraically closing the F272-class hazard rather than merely avoiding it. With the model's
seagull sector exactly empty (F155-A0, $u_0\equiv1$), the required total shift from Wilson decomposes into
three legs:

| leg | $\Delta C$ | share | status |
|---|---:|---:|---|
| 1. Wilson seagull + Haar measure (structurally absent for the rule) | $-2.568$ | 46.1% | **structural**, exact by A0 |
| 2. propagator face | $-0.992\pm0.044$ | 17.8% | **measured**, $1/n^2$-convergent |
| 3. rule 3-gluon+ghost vertex form factors | $-2.016$ | 36.2% | **OPEN** |

$$\boxed{\frac{\Lambda_{\overline{\rm MS}}}{\Lambda_\text{rule}}\in[1,\ 7.980]\quad(\text{required }1.773,\text{ at }11.1\%\text{ of the band; Wilson's own }28.81\text{ excluded by }3.61\times)}\tag{R13b.14}$$

with a stated two-sided falsifier (below 1 falsifies the monotonicity assumption; above 7.98 falsifies the
lock, distinguishable by which edge is crossed). This is the bracket §13b.3.5's F350 and §13b.4.5's F337
measure against.

F163 (2026-06-18, chronologically the earliest of Group C's members) is the direct attempt to reproduce
Wilson's own $28.81$ literally, as the design plan's own named validation gate. It transcribes the lattice
3-gluon and ghost vertices with their $\cos(k/2)$ form factors and validates them to an exact $O(a^2)$
continuum limit; assembles the full Wilson self-energy including the tadpole; and — the hardest bookkeeping
step — completes the tadpole/measure transversality restoration to **machine precision** by deriving,
rather than positing, the seagull's longitudinal content from the Ward identity alone. **The literal
$28.81$ is not reproduced, for an increasingly sharp reason across three revisions of the same finding**:
first, combining the loop+transversality machinery with an analytically-computed $\overline{\rm MS}$
reference gives only $\approx7.7$, short by $3\times$, revealing that transversality plus the loops do
*not* fully determine the seagull's transverse-leg content (only its longitudinal leg is Ward-fixed); then
the full Kawai–Nakayama–Seo quartic-seagull expansion is validated symbolically at quadratic order but
exceeds the sandbox's compute budget at quartic order, leaving the literal digit a native-run deliverable.
**What F163 leaves usable is real and load-bearing for F280's budget**: the exact vertex transcription, the
machine-precision transversality restoration, and the analytic $C_{\overline{\rm MS}}=131/66$ — F280
imports the loops-only piece of this as its own leg-1/leg-3 split's anchor.

$$\boxed{\text{The Wilson-side literal-28.81 reproduction is a genuine, disclosed partial result: the vertex transcription and transversality bookkeeping are complete and machine-exact, but the seagull's full transverse content needs a native long-run computation not yet performed}}\tag{R13b.15}$$

(F280: 6/6 PASS + control. F163: 5/5 structural PASS; `CL145`, `no_go`, `status: open`.)

### 13b.4.5 After X1's resolution: L6 decided, and the tension sharpens instead of closing (F337)

**F325's resolution of X1 itself (2026-08-18) is Chapter 13a's R13a.5 and is cited, not re-derived, here**:
the Casimir-normalisation branch is excluded on two independent legs (the mixed-matching artefact, §13b.4.1;
and a quantitative exclusion $5.63$ decades outside F280's own bracket), and the centre (branch B) reading
— the reading Group A's whole $\alpha_s$ derivation already assumed — is adopted unconditionally. **CL022's
own contingency note is explicitly lifted by this resolution** (§13b.1's headline number never depended on
the branch choice; the note concerned whether the $2.1\sigma$ framing itself was conditional on branch B,
and it no longer is).

Twelve days later, with Group B's genuine BCC gauge-action machinery now in hand (§13b.3), F337
(2026-08-30) attacks a structurally separate, still-open question the ledger had named **L6**: which object
is "the rule's gauge action" at finite lattice spacing for the purposes of LPT — the rhombic action's own
quadratic form, or the F26/$\Omega_\text{even}$ rotation-law propagator (F305 §5's declared gap) — and is
F305's redundant link-axis mode dynamical? **Both are decided cleanly**, on both a structural and an
empirical leg each: the rotation-law candidate is disqualified independently of any numerics (F308 §3
already measured it aperiodic under $2\pi$, $4\pi$ *and* $8\pi$ shifts — not a well-defined function on the
Brillouin-zone torus the rhombic vertices are exactly periodic under), and the redundant mode's
divergence past the target on an extended $n=8$–$40$ ladder confirms F305's exact isometry argument rather
than contradicting it, resolving what a shorter $n\le20$ ladder had made look like a genuine tension.

**But the native $n=28$–$40$ sweep the ledger predicted would close $d_1$ leg 3 does not — it sharpens the
tension instead.** Fitting the *actual* convergence power (not assuming the module's built-in $1/n^2$)
gives the BCC/rule side converging as $n^{-1.1\text{ to }-1.35}$, against the Wilson side's own $n^{-2.5
\text{ to }-2.83}$ — a genuinely, measurably slower rate. Using the one series that does converge cleanly
under the fitted power:

$$\boxed{\widehat{d\text{Loops}}=-2.731\pm0.060\ \Rightarrow\ \Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=31.3\quad(\text{outside F280's own }[1,7.98]\text{ bracket by}\sim4\times)}\tag{R13b.16}$$

F337 reads this, per F307's own established caution on exactly this failure mode, as **non-convergence, not
falsification** — but names, in advance and precisely, the exhaustion condition under which that reading
stops being available: if the named remedy (a smoothed WS-cell mask) is built and re-run, and the result
either still lies outside $[1,7.98]$ or lies inside it but with a convergence exponent still more than a
factor of 2 below Wilson's, that "would be the falsification of the $g_s=\tfrac12$ lock or the monotonicity
assumption... not a third round of 'still not converged.'" §13b.3.5's F350 is exactly that test, and both
conditions of the exhaustion clause fire.

(F337: 4/4 PASS gate-tier + 1 control; the native sweep is a committed `result_dump`, not a gate-tier
assertion, per its own memory-constraint disclosure.)

### 13b.4.6 The strong-CP loose end closes on the same decision (F340)

Chapter 13a's R13a.16 (F321) proved $\theta_\text{QCD}=0$ as a theorem of the rule's minimal-loop set being
closed under reversal, but named two ways it could still be wrong: dependence on the then-undecided L6
fork, and whether a real action still leaves room for a hidden $\theta$ between topological sectors. F340
(2026-08-31, the day after F337) closes both, using L6's decision directly. **Item 1**: an exact
set-comparison shows F321's own 20-loop action word list is *identical* to `lpt_bcc_vertex`'s rhombic loop
set — F321 was, without anyone checking at the time, already evaluating the object L6 has now confirmed is
the rule's gauge action; F321's earlier "the conclusion survives both branches" strengthens to "the other
branch was never a candidate at all." **Item 2**: the reversal identity that makes the loop set closed
under reversal — $\text{holonomy}(U,\text{reverse}(w))=\text{holonomy}(U,w)^\dagger$ — is proven to hold
**exactly, for every word and every configuration**, not merely measured on a sample of Haar-random
configurations as F321's own T1a had done; composed with the trace identity, this makes the action's
reality a statement about the *construction* (no configuration, of any topological content, contributes a
phase) rather than a sampled fact.

$$\boxed{\theta_\text{QCD}=0\text{'s two named residuals both close: the action-fork dependency dissolves (F321 was always on the decided branch) and the reality argument upgrades from a measurement on a sample to an exact theorem over the full configuration space}}\tag{R13b.17}$$

What remains genuinely open, named precisely rather than folded into the closed part: whether this
lattice's naive clover-based topological charge $Q$ is a properly quantised invariant in the continuum
sense — a standard, well-documented subtlety in lattice gauge theory generally, not new to this model, and
logically separate from whether $\theta$ is zero (the reality proof never used $Q$'s quantisation).
`CL278`'s confidence is raised to `high` on this basis.

(F340: 3/3 PASS + 2 controls verified red-only-where-declared.)

## 13b.5 The derivation — Group D: the scale-setting cross-check

### 13b.5.1 $\sqrt\sigma/f_\pi$ reconciled to $\sim12\%$ from one locked lattice (F124)

A separate calibration debt from F123: the model carries two independent QCD scale calibrations — the
chiral scale $f_\pi$ (NJL) and the string tension $\sqrt\sigma$ (confinement) — whose ratio, empirically
$\approx4.56$, was left undetermined. Because neither the gauge coupling ($\chi=1$, locked, §13b.2.1) nor
the NJL cutoff ($\Lambda=$ the BZ edge, not fit) is a free knob in this model, $\sqrt\sigma/f_\pi$ factors
as a pure lattice number:

$$\frac{\sqrt\sigma}{f_\pi}=\underbrace{\frac\Lambda{f_\pi}}_{\text{chiral, exact}}\times\underbrace{\frac{\sqrt\sigma}\Lambda}_{\text{confinement, from the condensate}}$$

The chiral factor is exact (Pagels–Stokar, $\Lambda/f_\pi=7.037$, machine precision). The confinement
factor uses F86's exact BPS tension $\sigma=2\pi v^2$ with F88's *measured* condensate VEV $v=m_D/e=0.713$
(Chapter 13a §13a.4.3), giving $\sqrt\sigma/\Lambda=0.569$ against the empirical $0.645$ ($-12\%$):

$$\boxed{\frac{\sqrt\sigma}{f_\pi}=7.037\times0.569=4.00\ \text{(axis convention)}\quad\text{vs empirical }4.56\ (-12\%)}\tag{R13b.18}$$

The finding also isolates *where* the residual lives: taking $\sqrt\sigma$ instead from the rule's bare
weak-coupling rotor collapses the ratio to $\approx1.0$, a factor $\sim4$ below the condensed-vacuum value
— precisely the QCD scale-setting/dimensional-transmutation gap between the UV lattice cutoff and the
physical, strong-coupling condensed regime where confinement actually lives (Chapter 13a's own §13a.4.1
finding that "confinement lives in the disordered ensemble"). Pinning the single self-consistent lattice
spacing at which both $\chi$SB and the physical $\sigma$ hold simultaneously is named as the residual gap
— the analytic analogue of what lattice-QCD scale-setting does numerically. **This result connects
directly to Chapter 17's scale-setting programme** (the SI-unit lattice-constant closure) and is scoped
here as a QCD-internal consistency check, not re-derived as part of that larger programme.

(F124: 6/6 PASS. C1/C3 machine-precision identities; C2/C4/C5 zero-parameter predictions; C6 a
diagnostic.)

## 13b.6 A coda, honestly scoped: the confinement block-spin eigenvalue and cosmology (F362)

F362 is assigned to this chapter's finding list but its content is not part of the $\alpha_s$/X1 narrative
above, and presenting it as such would misrepresent it — this chapter says so explicitly rather than
forcing it into the mould. F362 (2026-09-04) tests a completely different question using the same
confinement block-spin machinery Group A's $\chi=1$ result rests on (F130's Kogut–Susskind link
Hamiltonian, `link_hamiltonian.sigma_strong_pt2`): whether **fluctuation corrections to F130's frozen
($\lambda=0$) confinement block-spin eigenvalue** can supply the non-integer critical exponent Chapter 21's
dark-energy dilution-exponent programme needs (open-derivations row G2/K3, target $\gamma=0.0136$–$0.0176$).
The answer is a clean, mechanism-backed negative: every order of the strong-coupling expansion around
$\lambda=0$, evaluated under F130's own bond-moving convention ($g^2\to bg^2$, $\lambda$ held fixed),
carries an **exact integer** eigenvalue $b^{1-2n}$ — not merely the leading (Gaussian) term, the whole
series — and the one composite "effective exponent" this route *can* define is provably scheme-dependent
(not $b$-independent, failing the basic definition of a universal critical exponent) regardless of where it
is evaluated. The model's own calibrated coupling sits one to two decades past this expansion's validity
radius in any case.

$$\boxed{\text{A specific, checkable route to a non-integer confinement-sector RG exponent is tested and excluded, with the negative priced in advance by the finding this closes as valuable in its own right — not a result about }\alpha_s\text{ or }X1\text{, and not evidence either way about them}}\tag{R13b.19}$$

This result belongs to Chapter 21 (the cosmological constant / dilution-exponent programme), which should
treat it as the closure of one named route (bond-moving with $\lambda$ frozen), not a closure of the
broader question — a genuine Migdal–Kadanoff decimation step letting $\lambda$ itself flow remains
untested and is named explicitly as the natural next attempt.

(F362: 4/4 PASS + 2 controls, cold-subagent-reviewed, CONFIRMED-NARROWER.)

## 13b.7 Results table

| # | Statement | Status | Exactness | Source |
|---|---|---|---|---|
| R13b.1 | $g_s=\tfrac12$ derived from rule circularity + F110's C7 identity; carries two inherited normalisation choices, not zero knobs | derived (one open normalisation) | exact (structure) | F144 |
| R13b.2 | $\alpha_s(M_Z)$ zero-parameter, +8.4% converged / +1.3% 1-loop; the 19-decade fermion-mass hierarchy reproduced to $\times1.9$ from the same running | zero-parameter PREDICTION | quantitative | F144 |
| R13b.3 | Exact Fierz $c=\tfrac29$ (all four chiral channels); bare coupling cannot break chiral symmetry (decisive no-go); the RG-running coupling forces it | derived + no-go + forced-positive | exact (Fierz) / quantitative | F145 |
| R13b.4 | The one-loop $V\to\overline{\rm MS}$ conversion is the exact rational $a_1(6)=\tfrac{11}3$ | derived | exact | F151 |
| R13b.5 | UV face (scheme constant, exact leg + geometric band bracketing measurement) and IR face ($\alpha_\text{eff}^\ast\approx0.39$, gap-saturated, QCD's own branch) are two distinct objects | determined (UV) / identified (IR) | exact + quantitative | F151, F152 |
| R13b.6 | Residual B (IR gap) solved, converged, $L$-stable; Residual A's cheap moment shortcut ruled out — the full loop integral is the last freedom in the sector | solved / excluded-shortcut | quantitative / negative | F154 |
| R13b.7 | The gauge action was a blind simple-cubic composite while the propagator was already BCC; the defect is exact and present at every field amplitude | corrected defect | exact | F265 |
| R13b.8 | The genuine rhombic BCC lattice Feynman rules are derived, not transcribed; a real extra massless mode is found and resolved by an exact isometry | derived + resolved fork | exact / $O(a^2)$ | F305 |
| R13b.9 | Action-consistent $d_1$ estimator built; a refold defect is found, then found to be TWO independent defects on different branches; repair moves published numbers negligibly | built + repaired | machine | F307, F308 |
| R13b.10 | Lattice anisotropy $\beta_t/\beta_s=4$ derived, not chosen (differs from naive hypercubic by $4/3$); F299's d=4 Casimir successor runs, preliminary | derived + measured | exact / preliminary | F323 |
| R13b.11 | The named WS-mask remedy is built, verified far more accurate in isolation, but changes nothing about $d_1$'s anomalous slow convergence — the exhaustion condition fires | tested and excluded | quantitative | F350 |
| R13b.12 | The shared "one residual" framing is wrong; shape and scale residuals are different objects with opposite prospects for exact closure | reframing (no new physics) | structural | F172 |
| R13b.13 | The scheme conversion factorises exactly into a derived $V\to\overline{\rm MS}$ leg and one open lattice-matching leg, which is vertex-dominated | derived + localised | exact (leg 1) | F239 |
| R13b.14 | $d_1$ formulated subtracted against Wilson; three-leg budget; bracket $[1,7.98]$ contains the required value | formulated + bracketed | exact bookkeeping / bracket | F280 |
| R13b.15 | Wilson-side literal $28.81$: vertex transcription and transversality restoration complete and exact; full seagull needs a native run, not yet done | partial (disclosed) | exact (partial) / open | F163 |
| R13b.16 | L6 decided (propagator = rhombic action's own quadratic form; redundant mode not dynamical); native sweep sharpens the tension to $\Lambda\approx31$, outside the bracket | decided + non-convergent | exact (L6) / non-quotable | F337 |
| R13b.17 | Strong-CP's two named residuals close: action-fork dependency dissolves; reality proven exactly over the full configuration space | closed (two items) | exact | F340 |
| R13b.18 | $\sqrt\sigma/f_\pi$ reconciled to $\sim12\%$: exact chiral factor $\times$ condensate-derived confinement factor | derived (partial) | exact (chiral) / quantitative | F124 |
| R13b.19 | A specific route to a non-integer confinement RG exponent (bond-moving, $\lambda$ frozen) is tested and excluded — not part of the $\alpha_s$/X1 chain | negative result | exact (power-counting) | F362 |

## 13b.8 Comparison with measurement

**This is the chapter's most important honesty point, and it does not resolve as a clean success.** The
model's zero-additional-parameter prediction, running $\alpha_s(\mu_0)=1/(16\pi)$ down from $\mu_0=\hbar
c/a$ with no scheme constant applied, gives $\alpha_s(M_Z)=0.11955$ (1-loop). Compared to the current PDG
world average $0.1175\pm0.0010$: **$+1.7\%$, $\approx2.1\sigma$ — the register's largest single open
tension, per `docs/claims/CL022-alpha-s-at-mz-open-tension.md`, `status: open`.** This is not a fit-quality
statement; the model derives $\alpha_s$ from a Planck-scale boundary value with one scheme-matching input,
so the residual is a genuine disagreement, disclosed as such rather than hidden inside a "close enough"
framing. The measurement, not the model, has moved once already in this direction: an earlier PDG average
of $0.1180$ made the same unchanged model number read $+1.3\%$; the current $0.1175(10)$ moves it to
$+1.7\%$ — CL022's own history records this explicitly.

**A weaker, complementary statement does succeed with zero fit.** Folding in F151's exact $a_1=\tfrac{11}3$
leg and scanning only the model's own *geometric* conventions for the matching scale $q_\ast$ (no use of
the measured $\alpha_s(M_Z)$ anywhere in setting the band) gives $\alpha_s(M_Z)\in[0.1143,0.1232]$, which
*brackets* $0.1175(10)$ comfortably. This is a real, if weaker, success, and it is honestly reported as
such: a band, not a point prediction, though the band's width itself is derived from the model's structure
rather than tuned to contain the answer.

**A genuine cross-check, not circular, corroborates the fitted point.** Using the measured $\alpha_s(M_Z)$
to fix $q_\ast=0.7327/a$ inside that band (a one-parameter fit) reproduces a *second*, independent
observable — $\Lambda^{(3)}_{\overline{\rm MS}}=347$ MeV against the lattice-QCD-community value
$343(12)$ MeV (FLAG) — to $1.1\%$. Separately, Group D's $\sqrt\sigma/f_\pi=4.00$ vs empirical $4.56$
($-12\%$) is a genuinely different QCD calibration reconciled from the same locked lattice, cross-checking
Group A's scale-setting chain from an independent direction.

**The single largest unresolved technical question bearing on this comparison is the state of $d_1$
itself**, and it is worth stating precisely how it relates to CL022's headline number: CL022's $2.1\sigma$
figure does **not** depend on $d_1$ at all (it applies no scheme constant), so nothing in Group B or
§13b.4.5's $d_1$ tension moves that number. What $d_1$ would do, if pinned, is *explain* the $+1.7\%$/
$2.1\sigma$ gap as a specific, computed lattice-to-continuum matching effect rather than leaving it as raw
tension — and the most recent, best-engineered attempt at pinning it (F337, on the genuine BCC action;
F350, testing and excluding the leading candidate explanation for its slow convergence) finds the
extrapolated value ($\Lambda\approx31$–$34$) sitting outside F280's own bracket by a factor of $\sim4$, not
inside it near the required $1.773$. Per F337's own stated protocol (§13b.4.5), this is now formally past
the "still not converged" exhaustion point — though no finding read for this chapter has yet drawn the
further conclusion that the $g_s=\tfrac12$ lock or its monotonicity assumption is thereby falsified; see
the Gap logged in §13b.9 for the documentation-layer consequence of this.

## 13b.9 What was excluded, and why

- **The bare rule coupling as the source of chiral symmetry breaking** (F145 N3, §13b.2.3). A decisive
  negative, not an unverified possibility: at the derived bare $g_s^2=\tfrac14$, $R\equiv G/G_c=0.075$–
  $0.10\ll1$ at both measured dual-Meissner masses, and the dielectric enhancement cannot rescue it. What
  survives is that the *running* coupling forces the condensate — asymptotic freedom run backwards, not the
  UV coupling itself.
- **The propagator-log-moment shortcut for the matching scale $q_\ast$** (F154 A1, §13b.2.5). Ruled out
  cleanly: every converged moment is a UV scale, above F151's derived band; the physical content is that
  $q_\ast$ is a UV-finite subtraction, not accessible to a bare moment integral.
- **The composite simple-cubic gauge action, as a faithful account of the model's own curvature** (F265,
  §13b.3.1). Excluded by an exact kernel — one $\langle111\rangle$ link axis is invisible to it — not a
  numerical approximation; both actions share the identical classical continuum limit, which is exactly why
  this went undetected for as long as it did.
- **The F26/$\Omega_\text{even}$ rotation-law propagator, as the object LPT should use for the gauge
  action's own quadratic form** (F337 leg 1, §13b.4.5). Disqualified structurally (aperiodic under the very
  reciprocal lattice the rhombic vertices are periodic under) independent of any numerics.
- **The Casimir normalisation of the model's bare colour coupling** ($g_s=\sqrt3/4$, $\alpha_s(M_Z)=0.0397$,
  a $-66\%$ miss). Cited from Chapter 13a's R13a.5/`CL282`: excluded on two independent legs, neither of
  which needed $d_1$. Not re-derived here.
- **The literal Wilson $28.81$, as a target this model's own coupling should reproduce.** Never the claim
  — the model's own tadpole-free structure requires an $O(1)$ scheme constant, and F280's bracket
  structurally excludes $28.81$ by $3.61\times$. F163's own attempt to reproduce $28.81$ on the *Wilson*
  side (as a validation gate for the vertex/tadpole machinery, not a claim about the rule) is a genuine
  partial result, disclosed as such (§13b.4.4), not a failed prediction of this model.
- **F350's WS-mask staircase-discretisation hypothesis, as the explanation for $d_1$ leg 3's slow
  convergence** (§13b.3.5). Built, verified accurate in isolation, and measured not to move the
  convergence rate when wired into the actual estimator — a specific, checkable candidate mechanism tested
  and excluded, with the true mechanism still unidentified.
- **Fluctuation corrections to F130's confinement block-spin eigenvalue, as a source of Chapter 21's
  non-integer dilution exponent** (F362, §13b.6). Excluded for the specific route tested (bond-moving with
  $\lambda$ frozen); not part of this chapter's $\alpha_s$ narrative and not evidence for or against it.

## 13b.10 What is still open

- **CL022's $2.1\sigma$ tension headlines this section, as it headlines the register.** It is a real,
  disclosed disagreement between a zero-additional-parameter prediction and the measured world average, not
  a fit-quality artefact — see §13b.8.
- **$d_1$ itself (equivalently the matching scale $q_\ast$) is the single largest open computation in the
  strong sector**, and it is not merely unfinished: the most recent, best-engineered attempt (F337, on the
  genuine BCC action; F350, ruling out the leading candidate explanation for the slow convergence) finds
  the extrapolated value sitting outside the model's own tadpole-free bracket by a factor of $\sim4$,
  triggering F337's own stated exhaustion condition for the "still not converged" reading.
- **The true mechanism behind $d_1$ leg 3's anomalously slow convergence is unidentified.** F337's
  candidate (the sharp WS-mask's discretisation order) is tested and excluded by F350; the vertex form
  factors' own near-BZ-boundary behaviour, some other feature of the projected branch, and a genuine
  physical breakdown of F280's monotonicity assumption are all named as untested candidates.
- **F163's literal Wilson-$28.81$ reproduction is incomplete on the Wilson side itself** — the full
  quartic-seagull expansion is validated symbolically but exceeds sandbox compute at the order needed for
  the digit; a native long-run computation is the specified remaining step.
- **F323's d=4 Casimir-successor measurement is explicitly preliminary** (three configurations, no error
  bars); locating where and how sharply Casimir scaling gives way to screening for triality-0
  representations is a production-run item, not yet performed.
- **Whether this lattice's naive clover-based topological charge is a properly quantised invariant**
  (F340 §4, cited from the strong-CP closure) — a standard lattice-gauge-theory subtlety, logically
  separate from $\theta_\text{QCD}=0$ itself, and not attacked by any finding this chapter reads.

> **Gap [G-11]:** The two claim cards most directly downstream of this chapter's $d_1$/scheme-conversion
> work — `docs/claims/CL022-alpha-s-at-mz-open-tension.md` and
> `docs/claims/CL252-d1-tadpole-free-band-subtracted-against-wilson.md` — both carry `last_verified:
> '2026-08-18'`, the date of F325's X1 resolution. Neither card's text engages with F337 (2026-08-30),
> F340 (2026-08-31) or F350 (2026-09-02), all three of which post-date that verification and none of which
> is listed in either card's `findings:` front matter. This matters specifically because F337 measures the
> extrapolated $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ at $\approx31$–$34$ — outside CL252's own
> committed bracket $[1,7.98]$ by a factor of $\sim4$ — and states its own explicit exhaustion condition
> (quoted in full at F337 §4 and reproduced in this chapter's §13b.4.5) for when the standing
> "non-convergence, not falsification" reading should be retired in favour of treating the result as
> evidence against the $g_s=\tfrac12$ lock or its monotonicity assumption; F350 (built specifically to
> test that condition) confirms both of its clauses fire. Neither CL022 nor CL252's own text states
> whether the project regards this exhaustion condition as met, contested, or not yet acted upon — the
> silence is the gap, not a specific wrong number in either card. This is not the same claims-layer
> bookkeeping artefact as CL069/CL084/CL160/CL231 (§13b.1) — those are mechanical seeding-pass
> misreadings of a finding's own header text; this is a genuine staleness of an `authored`,
> `review_state: authored` card against findings that postdate its last verification by one to two weeks
> and bear directly on its own stated bracket. Not fixed here, as this chapter is documentation-only;
> flagged for whoever next revisits CL022/CL252, and for Chapter 17 (scale-setting), which should not cite
> CL252's bracket as settled without reading F337/F350 first.

## 13b.11 Falsifiers

Most of this chapter's headline claim cards (`CL128`, F145) carry `falsifier: unset` — declared debt, not
an absence of a testable prediction; the findings' own algebraic identities are their own de facto
falsifiers (a measured counterexample to the exact Fierz $c=\tfrac29$, or to the $a_1=\tfrac{11}3$
rational, would falsify the corresponding construction outright).

Where a falsifier **is** stated:

- **CL022.** A tightened world-average $\alpha_s(M_Z)$ moving the residual past $3\sigma$ without a
  corresponding scheme-matching resolution would falsify the derivation route. The residual has already
  moved once, in the unfavourable direction, purely from the world average shifting.
- **CL252 (F280's bracket).** A completed rule vertex computation returning $\Lambda_{\overline{\rm MS}}/
  \Lambda_\text{rule}$ outside $[1,7.98]$ falsifies either the $g_s=\tfrac12$ lock or the monotonicity
  assumption, distinguished by which edge is crossed. §13b.9's Gap [G-11] records that F337's own
  extrapolation already sits outside this bracket, with the exhaustion condition for treating that as
  decisive (rather than as further non-convergence) explicitly stated and, per F350, both of its clauses
  measured to fire.
- **CL145 (F163).** No independent falsifier beyond reproducing the literal Wilson $28.81$ figure with the
  full seagull assembled — the named remaining computation.
- **CL278 (F321/F340, strong CP, cited from Chapter 13a).** Exhibiting one $SU(3)$ configuration with
  $\mathrm{Im}\,S\ne0$ at gate tolerance, or showing the rule's minimal-loop set is not reversal-closed,
  would falsify the theorem this chapter's F340 upgraded to full-configuration-space exactness.
- **R13b.19 (F362).** Not falsifiable in the ordinary sense — a negative result about one specific route;
  its own falsifier is superseded by a positive demonstration of a genuine Migdal–Kadanoff decimation
  step letting $\lambda$ flow, named as the natural next attempt and explicitly not this finding's content.

One new gap was logged in `docs/monograph/GAPS.md` by this chapter: **[G-11]** (§13b.10), a staleness of
CL022/CL252 against F337/F340/F350, distinct from the mechanical claims-layer bookkeeping artefacts this
chapter also found and did not re-log (§13b.1: CL069, CL231 — the same pattern Chapters 8, 12 and 19
already documented as G-6, G-7 and G-9).
