# Chapter 25 — Emergent Condensed Matter and Information: Superconductivity, Entanglement, Quantum Computing, and Thermodynamics

*Chapter 25 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`) — the monograph's last content
chapter. Sourced from `findings/F210-electrical-superconductivity.md`,
`findings/F211-tc-magnitude-real-superconductors.md`, `findings/F212-dynamical-entanglement-generation.md`,
`findings/F213-hopfield-firstprinciples-and-gap-renormalization.md`,
`findings/F214-superexchange-and-live-entanglement-channel.md`, `findings/F215-eliashberg-solver.md`,
`findings/F217-field-native-fermion-entanglement.md`, `findings/F218-algorithm-through-the-engine.md`,
`findings/F218b-alpha2F-firstprinciples-and-pade-gap-ratio.md`, `findings/F220-field-native-execution.md`,
`findings/F221-noise-error-correction.md`, `findings/F222-scaled-quantum-algorithms.md`,
`findings/F224-qc-si-coldatom.md`, `findings/F225-doublon-leakage-spinqubit.md`,
`findings/F226-bell-tsirelson-indistinguishable.md`, `findings/F227-decoherence-unitarity-floor.md`,
`findings/F242-mustar-from-f64-dielectric.md`,
`findings/F374-eliashberg-cutoff-reconciliation-and-tc-residual-floor.md`, `findings/F375-nb-realistic-dos.md`,
`findings/F376-interacting-sector-eth-onset.md` — all 20 findings `00-plan.md` §2 assigns to this chapter,
read in full. Checked directly against `docs/theory/supersessions.yaml`: **zero hits** for all 20 finding
numbers, in any of the 23 records — none of this chapter's findings is superseded, reclassified, or even
mentioned. Checked against `claims-index.md`: **CL184** (F210, `live`), **CL185** (F211, `live`), **CL186**
(F212, `live`), **CL187** (F213, `live`), **CL188** (F214, `live`), **CL189** (F215, listed `withdrawn` —
investigated in full in §3.1.4/§3.4 below), **CL191** (F217, `live`), **CL192** (F218, `live`), **CL193**
(F218b, listed `withdrawn` — investigated in §3.1.5/§3.4), **CL194** (F220, `live`), **CL195** (F221,
`live`), **CL196** (F222, `live`), **CL198** (F224, `live`), **CL199** (F225, `live`), **CL200** (F226,
listed `withdrawn` — investigated in §3.3.6/§3.4), **CL201** (F227, `live`), **CL213** (F242, `live`);
`docs/claims/CL305-interacting-sector-eth-onset.md` (F376, F300, F309, `live`) is this chapter's twentieth
card. Notation and results are those of Chapters 1 (P4, the beable question), 5 (R5.1–R5.12, the Born-rule/
pointer-basis/classicality machinery), 9 (R9.1–R9.12, the U(1) coupling and paired-photon machinery), 13a
(R13a.10, the colour-dielectric dual superconductor), 14 (R14.15/R14.19, the live-simulation precedent), and
18 (R18.8–R18.10, the F64 EM-connection dielectric) — extended, never redefined.*

## 25.0 What this chapter establishes

Every preceding chapter derived a *fundamental* sector of the model: leptons, hadrons, gauge bosons, gravity.
This chapter asks a different kind of question, and it is the monograph's last: does the same discrete rule,
run at the scale of a real material or a small quantum register, reproduce the genuinely *emergent* physics
of many interacting degrees of freedom — not by fiat, but because the many-body machinery is actually built
and run? The answer, across twenty findings spanning four months of work (2026-07-01 through 2026-09-06), is
yes, in three independent arenas that turn out to be one construction viewed three ways. **Superconductivity**
(Group A) is shown to be the electric S-dual of Chapter 13a's magnetic colour-confinement mechanism — the
same lattice dielectric that carries gravity (Chapter 18) and confinement (Chapter 13a) also carries the
Cooper-pairing glue, and the resulting BCS universals, T_c magnitudes, and Eliashberg mass renormalization
are computed, not fit, to a documented and honestly bounded accuracy. **Entanglement generation** (Group B)
answers the question Chapter 1 explicitly left open and Chapter 5 built the machinery to test: a genuine
$2^n$-dimensional many-body register, built from the model's own primitives with no entanglement inserted by
hand, is shown to *generate* entanglement entropy dynamically, at a rate derived from the same hopping
amplitude that sets $c_\text{lat}$ and the fermion mass gap — first as an effective spin exchange, then as a
first-principles consequence of genuine second quantization. **Quantum computation** (Group C) shows that
this generated entanglement is not merely present but *usable*: a universal gate set compiles exactly from
the lattice's own exchange interaction, runs real algorithms (Grover, Deutsch–Jozsa, Bernstein–Vazirani, QFT)
at scale and on genuine fermionic matter, survives the addition of noise and error correction, and — in its
sharpest results — confronts four independent bodies of real-world data: niobium's measured $T_c$ and density
of states, cold-atom super-exchange oscillations, a semiconductor exchange-qubit's measured leakage, and the
Tsirelson bound of loophole-free Bell experiments. A closing thread (**Group D**) asks the harder equilibrium
question these many-body sectors raise once interactions are turned on at all: does the free sector's
generalised Gibbs ensemble (Chapter 20's thermodynamics machinery, cited not re-derived) give way to genuine
thermalisation, and if so, under what minimal condition? The chapter's honest center of gravity, stated before
the derivation: **every quantitative comparison against real data lands within, or close to, standard
theoretical accuracy for that observable** — Eliashberg/Allen-Dynes accuracy for $T_c$ (4.9–17%, depending on
route), textbook Hubbard-model accuracy for cold-atom and quantum-dot leakage data, and *exact* machine-
precision agreement for the Tsirelson bound — and three claim cards this chapter reads (CL189/CL193/CL200)
turn out, on inspection, to be marked `withdrawn` by the identical mechanical bookkeeping artifact this
monograph has now found seven times in six different chapters, not by any actual physics retraction.

## 25.1 Inputs

**Postulates used.** **P4** (linearity, exact unitarity, the amplitude treated as physically real, with no
additional 't Hooft-style hidden-classical-layer postulate) is the postulate this chapter's Group B/C results
put to its sharpest empirical test yet. Chapter 1 §1.3 stated the model's ontological stance and flagged it
as genuinely undecided relative to 't Hooft's superdeterministic alternative; Chapter 5 (§5.6) showed the
model's own unitary substrate *suffices* to derive the Born rule, the pointer basis, and classicality with no
hidden layer, calling this a **sufficiency**, not a **necessity**, result — nothing in Chapter 5 discriminates
the model's reading from 't Hooft's. This chapter's F212/F226 do not close that question either (§25.7
returns to this explicitly), but they sharpen exactly what "sufficiency" means operationally: F212 builds a
genuine $2^n$ tensor-product register, initializes it from a **product** state with *zero* entanglement
entropy verified to machine precision, and shows the model's own unitary dynamics — not a hand-inserted Bell
state — drives it to $S=\ln2$; F226 measures CHSH on that *dynamically generated* state and finds it
saturates the Tsirelson bound $2\sqrt2$ to $1.8\times10^{-15}$, using freely and independently chosen analyzer
settings (F226 G4), explicitly *not* relying on superdeterministic setting–source correlations. **P5** (the
primitive field is $\psi\in\mathbb C^2$) is the object every fermionic-sector result in this chapter is built
on: the Cooper pair (F210 Task 3) is the charged sibling of Chapter 8's $\mathbb C^2$ Weyl doublet, and the
Hubbard chain of F217/F220 is a genuine second-quantized Fock space built from the same spinor. **P6** (the
chiral $SU(2)$ mass connection) supplies, via Chapter 11's mass mechanism, the fermion mass $m$ that sets both
the hopping amplitude $t(m)$ and the mass gap $U(m)=2\arcsin m$ every entanglement-generation and
quantum-computing rate in Group B/C is derived from (F214 Thread 1). No new postulate is introduced.

**Prior results used, precisely.** **R9.1–R9.3** (Chapter 9, F68/F87) — the identity-channel Peierls coupling
and its exact charge conservation, holonomy, and helicity-blindness — is what F210 Task 5 reuses directly for
flux quantization ($\Phi_0=h/2e$) and the Josephson relations; nothing about the U(1) coupling mechanism is
re-derived here. **R13a.10** (Chapter 13a, F86) is the chapter's single most load-bearing cross-reference: the
colour-magnetic condensate's dual-Meissner confinement mechanism, built from the model's own rotation-rate
dielectric in the *opposite* impedance regime from gravity's $K$, is what F210 identifies electrical
superconductivity *as* — the electric S-dual of the identical construction, not a new mechanism. **R18.8–R18.10**
(Chapter 18, F64/F106) — the single impedance-matched lattice dielectric $K$ that carries gravity — is what
F210 Task 1, F213 Part A, and F242 all identify as the physical origin of the electron–phonon deformation
potential and the Thomas–Fermi Coulomb screening; this chapter does not re-derive $K$'s properties, only reuses
its strain-response and static-screening limits. **R12.6** (Chapter 12, F34b) — the Stueckelberg $W$-mass
mechanism (Goldstone-eating with no Higgs VEV) — is what F210 Task 4 identifies the Meissner effect *as*: the
identity-channel photon (Chapter 9) eating the condensate's phase Goldstone inside a superconductor is the
same mass-generation mechanism Chapter 12 already built for the electroweak sector, applied to a different
condensate. **R14.15/R14.19** (Chapter 14, F206/F134) are this chapter's direct precedent for *live,
real-time, multi-body simulation on the production engine* — F206 wired a static NN potential into a live
inter-nucleon binder that reaches a stable, unitary equilibrium; F134 ran four coupling loops (quark, gluon,
photon, electron) simultaneously on one literal BCC lattice with norm conserved to $1.3\times10^{-14}$. Group
B/C's `EntanglementRegisterChannel`, `FermionChainChannel`, `QuantumCircuitChannel`, and `ErrorCorrectionChannel`
(F214/F217/F218/F221) are the identical engineering discipline — a genuine many-body sector wired as a
first-class, checkpoint-safe `casim` engine channel, not a standalone script — applied to a new physics
domain. **R5.1–R5.12** (Chapter 5) supply the pointer-basis/Born-rule/classicality machinery this chapter's
entanglement-generation results are the natural many-body extension of, though Chapter 5 built that machinery
on a single-cell decoherence model and this chapter's registers are the first place in the monograph a genuine
multi-cell $2^n$ Hilbert space is allocated and evolved as a first-class object.

**Free inputs consumed, stated precisely.** 1. **The magnitude of $T_c$ for any specific superconductor is a
genuine material input** ($N(0)V$, equivalently $\lambda$, $\omega_\text{log}$), exactly as it is in BCS and
Eliashberg theory themselves — the model's contribution (F210–F213, F218b, F242, F374, F375) is deriving that
input's model-native origin ($\lambda\propto D^2$ from the F64 deformation potential, $\mu^*$ from the same
dielectric's screening limit) and its accuracy, not eliminating the material-specificity BCS itself never
eliminates. 2. **The absolute mass $m$** that sets $t(m)$ and $U(m)=2\arcsin m$ in every Group B/C
entanglement-generation rate is a Chapter 11 free input (R11.14), not derived in this chapter; the entanglement
*rate* is a function of $m$, not an absolute number. 3. **Tantalum's density-of-states enhancement factor is
explicitly left unfixed** (F375 D5) — a genuine, disclosed, honestly-scoped open item, not a free parameter
quietly absorbed. 4. **The toy interaction strengths $V_1=V_2=0.5$ in F376's minimal interacting extension are
not derived from the model's own BCC gauge-sector coupling constants** (F376 scope item 2) — they are the
smallest generic perturbation the ETH literature uses to leave the integrable manifold, chosen for that reason,
not fit to any target number.

## 25.2 The derivation — Group A: superconductivity as the electric S-dual of confinement

### 25.2.1 The construction and its BCS universals (F210)

Before this finding, the model's only "superconductor" content was analogical: F86's colour-**magnetic**
dual superconductor for QCD confinement, and a borrowed Cooper-pair label in the lepton sector. F210 builds the
genuine condensed-matter phenomenon and identifies it structurally: F86 condenses colour-magnetic charge and
expels colour-electric flux into a confining tube (R13a.10); ordinary superconductivity is the identical
construction with electric and magnetic exchanged — electric charge (paired electrons) condenses, and magnetic
flux is expelled (Meissner) or squeezed into vortices (type II). Every ingredient traces to existing machinery:
the gap equation is Chapter 15's NJL self-consistency equation reused verbatim; the Meissner photon mass is
Chapter 12's Stueckelberg Goldstone-eating (R12.6); the flux quantum is Chapter 9's U(1) holonomy (R9.3) at
pair charge $2e$; the propagating photon is Chapter 8's even-law, non-birefringent paired photon, never the
excluded chiral construction.

The pairing glue is derived, not assumed, and the result is structurally honest about scope: on the **bare
fundamental lattice** the inter-electron channel is repulsive (Coulomb, via the Chapter 9 photon) and the only
intrinsic bosonic mode is the $G$-suppressed graviton wave — the vacuum does not superconduct. Conventional
superconductivity is strictly an **emergent-lattice** phenomenon, requiring a material crystal (Chapter 24's
block-spin atoms) whose acoustic phonons supply the retarded Fröhlich attraction:

$$V_\text{eff}(q,\omega)=V_c+|g_q|^2\,\frac{2\omega_q}{\omega^2-\omega_q^2}\ \ \text{(attractive for } |\omega|<\omega_q\text{, SC1a, exact sign)},$$

with the electron–phonon vertex identified as the electron's sensitivity to a strain-modulated lattice
dielectric $K$ (F64, R18.8) — the same field that carries gravity now sets the pairing glue. The static
small-$q$ limit reduces exactly to the $q$-independent BCS contact $V=D^2/(\rho c_s^2)$ (SC1b, spread
$<10^{-12}$). Solving the resulting self-consistent gap equation — algebraically the *same* equation as
Chapter 15's NJL gap — the two coupling- and cutoff-**independent** BCS universals reproduce to machine
precision:

$$\frac{2\Delta(0)}{k_BT_c}=\frac{2\pi}{e^\gamma}=3.5277539777\ldots\quad(3.8\times10^{-16}),\qquad
\frac{\Delta C}{C_n}=\frac{12}{7\zeta(3)}=1.4261269\ldots\quad(<10^{-9}).$$

The Cooper pair is identified exactly as the charged sibling of Chapter 8's neutral bound Weyl pair: spin
singlet, $s$-wave, **charge $2e$ exactly** (integer holonomy), with phase advancing as the *sum* of its
constituents — winding number 2, the origin of $\Phi_0=h/2e$. The Meissner effect is Chapter 12's Stueckelberg
mechanism read in a new condensate: the Chapter 9 photon eats the condensate phase Goldstone and becomes
massive, with the Proca dispersion reducing exactly to the luminal even photon at $m_\gamma=0$ ($<10^{-15}$),
and the $(2e)$-vs-$(e)$ London-depth screening ratio equal to exactly $1/2$ — the pair-charge signature.
Persistent, dissipationless supercurrent follows directly from the London equation with $\mathbf E=0$:
$\partial_tJ_s=0$ exactly, while a matched gapless (Drude) control decays.

$$\boxed{\;\text{Superconductivity is the electric S-dual of F86's colour confinement, built from pre-existing machinery: the two BCS universals reproduce to machine precision (}3.8\times10^{-16}\text{, }<10^{-9}\text{), the glue is the F64 gravitational dielectric strained by a phonon, and every SC signature (}2e\text{ charge, }\Phi_0=h/2e\text{, persistent current) is exact}\;}\tag{R25.1}$$

(F210: 16/16 checks PASS; `CL184`, `live`, `exact`.)

### 25.2.2 T_c magnitude from real superconductors (F211)

F210 left the magnitude of $T_c$ open — it needs the material coupling $N(0)V$, exactly as BCS/Eliashberg
theory itself does. F211 feeds seven elemental superconductors' literature couplings ($\lambda,\mu^*,
\omega_\text{log}$) through three estimators of increasing fidelity — weak-coupling BCS, McMillan (1968), and
Allen-Dynes (1975), one gap equation dressed at three levels of self-energy — and finds Allen-Dynes reproduces
the measured $T_c$ to a **mean 14.3%** (Pb 0.1%, Ta 0.3%, Sn 4.9%, Hg 6.1%, Nb 10.9%, In 23%, Al 55%), within
the field's own standard accuracy. Plain BCS overestimates every element (because it omits the $(1+\lambda)$
quasiparticle-mass renormalization); the model-native Task-1 kernel, rewritten in Hopfield form
$\lambda=\eta/(M\langle\omega^2\rangle)$, independently reproduces the tabulated couplings for Nb/Al/Ta/Pb to
$<5\%$. The residual is the honest one BCS/Eliashberg itself carries: $T_c$ is exponential in $\lambda$, so
weak-coupling elements (Al, In) are hypersensitive to the input coupling's own uncertainty.

$$\boxed{\;\text{Feeding real literature couplings through the F210 gap equation at the Allen-Dynes level reproduces measured }T_c\text{ for seven elements to mean }14.3\%\text{; the model-native Task-1 kernel independently matches tabulated }\lambda\text{ to }<5\%\;}\tag{R25.2}$$

(F211: 5/5 checks PASS; `CL185`, `live`, `quantitative`.)

### 25.2.3 First-principles Hopfield coupling and the non-universal gap ratio (F213)

F213 replaces the literature coupling $\lambda$ with a model-derived one for the two genuinely free-electron
metals in the F211 set. The deformation potential follows purely geometrically from the F64 dilation of the
electron's confined rotation-rate energy: $D=\tfrac23E_F$, needing only the electron density. The resulting
bare jellium $\lambda$ overestimates Al and Na's measured couplings by a **consistent** $\sim2.4$–$2.9\times$ —
precisely the well-known jellium/rigid-ion overestimate — reconciled to physically reasonable values by
screening $D$ through the same F64/Thomas-Fermi dielectric by a consistent $\sim1.55\times$. Part B of the same
finding shows that F210's universal gap ratio $3.528$ is a **weak-coupling limit**, not a law: the measured
ratio rises to $4.4$–$4.6$ for strong-coupling Pb/Hg, correlating with $T_c/\omega_\text{log}$ at $r=0.989$ and
with the Eliashberg mass renormalization $Z=1+\lambda$ at $r=0.998$ — the same physics (strong coupling)
suppresses $T_c$ below naive BCS *and* pushes the gap ratio above $3.528$.

$$\boxed{\;\text{The electron-phonon coupling is model-native (}D=\tfrac23E_F\text{ from the F64 dilation, }\lambda=N(0)V_\text{Task1}\text{ exactly); the }3.528\text{ gap ratio is a weak-coupling limit that rises to }4.4\text{–}4.6\text{ for strong coupling, tracking }T_c/\omega_\text{log}\text{ at }r=0.99\;}\tag{R25.3}$$

(F213: 7/7 checks PASS; `CL187`, `live`, `quantitative`.)

### 25.2.4 The imaginary-axis Eliashberg solver, and CL189's investigated `withdrawn` status (F215)

F215 promotes the static F77/F210 gap equation to the coupled Eliashberg $(Z,\Delta)$ equations on the
Matsubara axis, using the single Einstein mode that is exactly F210's retarded kernel continued to imaginary
frequency. Solved by power iteration (no `np.linalg` on the off-diagonal chiral blocks, per the CLAUDE.md
numpy-hazard caveat), the mass renormalization $Z(i\omega_0)$ emerges dynamically and tracks $1+\lambda$ across
the full coupling range (Al $1.42$ vs $1.43$; Hg $2.46$ vs $2.62$) — this is the object plain BCS silently sets
to 1 — and the $(1+\lambda)$ suppression reduces the naive-BCS overestimate by $\sim4$–$6\times$ onto
experiment (Pb: $7.6$ K vs BCS's $32$ K, exp $7.19$ K). Feeding only $(\lambda,\omega_\text{log},\mu^*)$, the
dynamically solved $T_c$ reproduces the seven measured values at correlation $r=0.975$, with **no
McMillan/Allen-Dynes parametrization** — the closed-form fits of F211 are superseded by a direct solve. The
one disclosed residual is a systematic $\sim27\%$ high mean error, traced (correctly, per F218b below) to
concentrating all spectral weight in one Einstein mode rather than a realistic distributed spectrum.

**CL189's `withdrawn` status, investigated.** `claims-index.md` lists CL189 (F215's card) as `status: withdrawn`.
Reading the card directly shows the identical mechanical artifact this monograph has now documented six times
across five chapters (Ch.7's CL029/F15, Ch.8's CL084/F89, Ch.9's CL082/F87, Ch.12's independent finding for its
own gap, Ch.13b's CL022/CL252 staleness, Ch.19's CL160/F181): the card's own `## Status & history` section
states plainly that the withdrawal is *inferred*, quoting the "banner" verbatim — which reads "Confirmed —
5/5 checks PASS. Promotes the static F77/F210 gap to the coupled $(Z,\Delta)$ Eliashberg equations..." **This
is F215's own routine pass-count status line, not a supersession or withdrawal banner.** F215 appears in no
`supersessions.yaml` record's `superseded:` field, and the finding file itself carries no `⚠` marker or
retraction language anywhere. This is a seeding-pass artifact — the mechanical extraction script that built
the claims layer (`review_state: unreviewed-seed`, per the card's own front matter) mis-detects the word
"Confirmed" or a subsequent narrative aside as a withdrawal signal. **This chapter treats F215/R25.4 as a live,
correctly-reported result**, exactly as its own `**Status:** Confirmed` line states.

$$\boxed{\;\text{The Eliashberg mass renormalization }Z=1+\lambda\text{ emerges dynamically on the Matsubara axis, suppressing naive-BCS }T_c\text{ by }4\text{–}6\times\text{ onto experiment; }T_c\text{ from }(\lambda,\omega_\text{log},\mu^*)\text{ alone matches measurement at }r=0.975\text{, no closed-form fit — CL189's `withdrawn` label is the same mechanical bookkeeping artifact found elsewhere in this monograph, not a real retraction}\;}\tag{R25.4}$$

(F215: 5/5 checks PASS; `CL189`, front matter reads `withdrawn`, investigated here and read as live.)

### 25.2.5 First-principles spectral function and dynamic gap ratio via Padé, and CL193's investigated status (F218b)

F218b derives, rather than assumes, the Eliashberg spectral function itself: acoustic phonons with the F213
deformation-potential vertex, Fermi-surface averaged over the spherical phase space, give the closed form
$\alpha^2F(\omega)=\lambda\,\omega^2/\omega_\text{max}^2$ with the exact log-moment identity
$\omega_\text{log}=\omega_\text{max}/\sqrt e$ — the whole spectral shape is fixed by the same $\omega_\text{log}$
the model already uses, with no new input. Feeding this realistic distributed spectrum to the F215 solver
shows $T_c$ is **shape-insensitive** at fixed $\omega_\text{log}$ (Einstein and Debye agree to a few percent
across all seven elements) — explaining, after the fact, why F215's single Einstein mode already worked as
well as it did, and reframing its $\sim27\%$ residual as a $\mu^*$/cutoff calibration matter rather than a
spectral-shape defect (a diagnosis F374 later confirms and partially corrects, §25.2.7). Analytically
continuing $\Delta(i\omega_n)$ to the real axis (Vidberg–Serene Padé, hand-rolled in `mpmath`, again per the
numpy chiral-transform caveat) gives the strong-coupling reduced gap **dynamically**, with no fit formula: it
recovers BCS's $3.53$ at weak coupling (Al, $+1\%$), rises to $4.6$–$4.7$ for Pb/Hg, and correlates with
measurement at $r=0.988$ — the first-principles Debye spectrum tightens the ratio (mean error $6.4\%\to5.2\%$)
specifically because, unlike $T_c$, the gap ratio *is* spectral-shape-sensitive.

**CL193's `withdrawn` status, investigated.** The identical pattern: CL193's own text quotes F218b's routine
"Confirmed — 7/7 checks PASS..." status line as its inferred "withdrawal banner." F218b carries no
supersession language and appears in no `supersessions.yaml` record. Read as live.

$$\boxed{\;\text{The Eliashberg spectral function }\alpha^2F(\omega)=\lambda\omega^2/\omega_\text{max}^2\text{ is model-derived, with }\omega_\text{log}=\omega_\text{max}/\sqrt e\text{ exact; }T_c\text{ is shape-insensitive (explaining F215's success) while the Padé-continued gap ratio is shape-sensitive and correlates with measurement at }r=0.988\text{ — CL193's `withdrawn` label is the same investigated artifact as CL189, not a real retraction}\;}\tag{R25.5}$$

(F218b: 7/7 checks PASS; `CL193`, front matter reads `withdrawn`, investigated here and read as live.)

### 25.2.6 Morel–Anderson μ* derived from the F64 dielectric (F242)

The last empirical input in the F210–F218b chain was the Coulomb pseudopotential $\mu^*\approx0.10$–$0.13$,
fit per element. F242 identifies the electronic screening as the same F64 dielectric's static long-wavelength
limit — the Thomas–Fermi form $\varepsilon(q)=1+k_\text{TF}^2/q^2$, the identical field already used on the
phonon side (F213) for a consistency, not a new posit. Fermi-surface-averaging the screened Coulomb collapses
to a pure function of $r_s$, $\mu(r_s)=0.082930\,r_s\ln(1+6.0299/r_s)$, and applying the Morel–Anderson
retardation reduction **at the solver's own Coulomb cutoff** (a subtlety that mattered: evaluating at
$\omega_\text{log}$ rather than the solver's actual $6\omega_\text{log}$ gives the wrong sign of correction)
gives $\mu^*=0.10$–$0.12$ with **zero fit parameters**, matching the tabulated empirical values. Feeding this
derived $\mu^*$ back through Allen-Dynes cuts the seven-element mean error from **14.3% to 6.3%** (simple
metals: $17.7\%\to6.7\%$) — more than halving it — while the Eliashberg solver improves more modestly
($27.6\%\to21.6\%$), correctly diagnosed at the time as *partly* a $\mu^*$ effect and partly a residual cutoff-
bookkeeping issue F374 later resolves.

$$\boxed{\;\mu(r_s)=0.082930\,r_s\ln(1{+}6.0299/r_s)\text{, from the F64 dielectric's Thomas-Fermi screening limit; }\mu^*\text{ derived (no fit) lands at }0.10\text{–}0.12\text{, cutting the Allen-Dynes 7-element mean error }14.3\%\to\mathbf{6.3\%}\;}\tag{R25.6}$$

(F242: 5/5 checks PASS; `CL213`, `live`, `machine`.)

### 25.2.7 The Eliashberg cutoff bug, fixed, and a disclosed NO-GO on beating 6.3% via the solver (F374)

F374 attacks F242's own named next step (reconcile the Eliashberg solver's Matsubara cutoff convention with
the analytic Allen-Dynes cutoff) and finds a genuine bug: F242's $\mu^*$ derivation assumed the solver's
Coulomb window is $\omega_c=6\,\omega_\text{log}$, which is correct only for the single-Einstein-mode solve;
for the Debye spectrum (F218b), the solver's actual cutoff scale is $\omega_c=6\sqrt e\,\omega_\text{log}$ (the
F218b AF2 identity), a factor of $\sqrt e=1.6487$ larger. Since $\mu^*$ increases with the cutoff, using the
smaller Einstein-convention cutoff for the Debye solve under-derives $\mu^*$ and runs the solver systematically
hot. Fixing this — a real, verified correction, not a re-fit — tightens the Eliashberg seven-element mean
error from $21.6\%$ to $17.2\%$.

Having fixed a real bug, F374 then exhausts every further plausible lever *before* concluding the Eliashberg-
solver route is closed: finite-matrix-size truncation is ruled out (the solver's default matrix is converged
to $0.05\%$ against a much larger one); scanning the cutoff factor from 1 to 15 shows the error curve
flattening near $16\%$, not descending toward $6\%$; the model's own exact strong-coupling shape factor
$r=\sqrt{e/2}$, fed into Allen-Dynes' $f_2$ correction, makes the fit *worse* ($6.3\%\to6.6\%$), confirming the
unadorned Allen-Dynes formula is already the tightest configuration available from the model's own inputs;
and dropping the Coulomb window entirely is worse still ($20.9\%$). The finding closes this specific route as
a **NO-GO**, explicitly and quantitatively: the reconciled Eliashberg floor plateaus at $16$–$17\%$ and cannot
be pushed below the $6.3\%$ Allen-Dynes headline with the machinery currently in the tree, and — a genuinely
useful negative result — cross-checks this against the literature (published $\mu^*$ conventions for Al and
Pb alone disagree by $15$–$25\%$ depending on cutoff choice, per Szczęśniak), showing the residual is an
established feature of Eliashberg numerics generally, not a defect specific to this model. The correctly
identified upstream cause — the model's idealized single-band, isotropic-Debye phonon spectrum, most
inaccurate for the $d$-band metals Nb/Ta — is exactly what F375 attacks next.

$$\boxed{\;\text{A real cutoff-scale bug (missing factor }\sqrt e\text{) is found and fixed, tightening the Eliashberg mean error }21.6\%\to17.2\%\text{; five further, independent attacks (finite-}N\text{, cutoff-factor scan, the model's own exact shape factor, dropping the window) all converge on a }16\text{–}17\%\text{ floor — a disclosed, quantified NO-GO on beating Allen-Dynes' }6.3\%\text{ via the solver alone}\;}\tag{R25.7}$$

(F374: 10/10 checks PASS; `Claim: none` per D12 — a refinement/no-go, not a new physics-tested assertion.)

### 25.2.8 A real DFT-sourced density of states crosses the target (F375)

F374 named the actual next lever: the model's free-electron $N(0)$ understates the true density of states of
the $d$-band metals Nb and Ta. F375 sources an independent, literature DFT calculation of niobium's density of
states ($N(E_F)\simeq1.49\ \text{eV}^{-1}$/atom, De Marzi et al. 2023, Quantum ESPRESSO — not fit to any $T_c$
or superconducting quantity), generalizes F242's $\mu(r_s)$ formula to an arbitrary density-of-states
enhancement factor $\alpha=N(0)/N(0)_\text{free}$ (exact at $\alpha=1$, a strict generalization verified to
$10^{-14}$), and finds $\alpha_\text{Nb}=3.084$ — physically sensible for a narrow $d$-band at $E_F$. Applying
this single, sourced correction to Nb alone (all six other elements unchanged) moves the Allen-Dynes
seven-element mean error from **6.3% to 4.9%**, crossing the target F374 could not reach through the solver,
and improves Nb's own individual error from $10.6\%$ to $0.2\%$. The result is robust, not knife-edge: scanning
$\alpha_\text{Nb}$ over $[2.0,6.0]$ keeps the mean error below $6.3\%$ throughout, and varying the free-electron
$E_F$ input by $\pm30\%$ moves the result only between $4.99\%$ and $5.21\%$. Tantalum is explicitly,
machine-checkably left uncorrected (`DOS_ENHANCEMENT` contains only `"Nb"`) — no equally solid sourced
$N(E_F)$ was found this session, and the finding declines to estimate one by analogy, naming this the genuine
open item for a future session rather than quietly absorbing a guess.

$$\boxed{\;\text{A single, independently-sourced DFT }N(E_F)\text{ for niobium (}\alpha_\text{Nb}=3.084\text{, no fit to any SC quantity) crosses the G9 target: Allen-Dynes 7-element mean error }6.3\%\to\mathbf{4.9\%}\text{, robust across }\alpha\in[2,6]\text{; tantalum is left explicitly, checkably open}\;}\tag{R25.8}$$

(F375: 13/13 checks PASS, independently reviewed 2026-09-06, **CONFIRMED**; `Claim: none` per D12.)

## 25.3 The derivation — Group B: the microscopic origin of entanglement generation

### 25.3.1 The substrate generates entanglement it is not given (F212)

Before this finding, the model's implementation was a genuine unitary QCA (reproducing CHSH at Tsirelson to
$4.4\times10^{-16}$, per the priority test battery), but every many-body sector actually shipped —
`ca_manybody.py`'s Hartree self-consistent electrons, the CHSH priority test's hand-built "singlet" — was
mean-field or first-quantized: entanglement was *inserted*, never generated, and a mean-field state cannot
represent the $2^N$-dimensional Hilbert space quantum computing's advantage requires. F212 poses the decisive,
decidable question: built from the model's own primitives, does a genuine many-body register **generate**
entanglement entropy from a product input?

The answer is yes, exactly. A dense $2^n$ tensor-product `Register`, initialized only from single-cell product
kets (verified $S_0=0$ to machine precision), is evolved by two gates native to the model: the single-qubit
rotor $R(\theta,\hat n)=\cos\theta\,I-i\sin\theta\,(\hat n\cdot\boldsymbol\sigma)$ — identical in form to
Chapter 6's mass/coupling rotation — and the two-qubit nearest-neighbour spinor **exchange**
$U_\text{exch}(\theta)=e^{-i\theta\,\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$, the lattice-native super-
exchange interaction two adjacent Weyl cells develop at second order in the hop. Evolving the product
$|\!\uparrow\downarrow\rangle$ under $U_\text{exch}(\pi/8)$ gives $S:0\to\ln2$ to residual $8\times10^{-16}$ —
a maximally entangled Bell state produced from a product input, with the full angle-dependence matching the
analytic $S(\theta)$ to $<10^{-12}$. By the Schmidt decomposition, the best fidelity **any** single product
state can have with the resulting Bell state is exactly $\tfrac12$; an explicit time-dependent Hartree
evolution (the honest mean-field limit) stays at $S=2.2\times10^{-16}$ throughout and reaches at most that
$50\%$ fidelity — the decisive, quantified contrast between what the exact dynamics generates and what the
previously-shipped mean-field sectors can represent. Extended to three qubits, all three single-cell cuts
generate nonzero entanglement (genuine tripartite entanglement, not merely pairwise), and $U_\text{exch}(\pi/8)$
is certified as a perfect entangler — by the Bremner et al. (2002) universality theorem, universal for quantum
computation given the model's own single-qubit rotor set.

$$\boxed{\;\text{A genuine }2^n\text{ tensor-product register, initialized as a product state (}S_0=0\text{, machine precision), reaches }S=\ln2\text{ under the model's own nearest-neighbour exchange gate (residual }8\times10^{-16}\text{); the best any single product state can do is fidelity }\tfrac12\text{ exactly, and an explicit mean-field (Hartree) evolution stays at }S\approx0\text{ throughout — the model's previously-shipped many-body sectors provably cannot host the entanglement its own exact dynamics generates}\;}\tag{R25.9}$$

(F212: 5/5 checks PASS, four at machine precision; `CL186`, `live`, `exact`.)

### 25.3.2 The entangling coupling is derived, and wired live (F214)

F212 left the entangler's coupling $J$ asserted rather than derived, and the register abstract rather than
part of the live engine. F214 closes both. Two adjacent Weyl/Dirac cells, one spin-$\tfrac12$ fermion each,
undergo second-order degenerate perturbation theory at half filling — a fermion virtually hopping to its
neighbour at amplitude $t$, double occupancy costing the mass gap $U$ — giving the antiferromagnetic Heisenberg
super-exchange $H_\text{eff}=\tfrac J4(\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B-1)$, with both inputs taken
from the model, not fit: $t(m)$ is measured directly from one tick of the exact `ca_dirac` stepper, and
$U(m)=2\arcsin m$ is Chapter 6's mass gap. The exact two-site Hubbard singlet–triplet gap
$J=\tfrac12(\sqrt{U^2+16t^2}-U)$ matches exact diagonalization to $<10^{-12}$, and predicts a Bell-entangling
time $\tau=\pi/(2J)$ that is **not a free knob** — it is set by the fermion mass $m$ alone. Wired live into
`casim` as `EntanglementRegisterChannel` (the engine's 25th channel), a two-cell run initialized as a Néel
product reaches $S=\ln2$ at the **independently derived** tick $\tau=7$ (measured $0.693146850$ vs
$\ln2=0.693147181$, matching the discrete-tick error of the continuous prediction $\tau=7.004$), a control
exchange-eigenstate stays at exactly $S=0$, and checkpoint/resume is bit-identical — the register is a
first-class, resumable engine citizen with the same status Chapter 14's block-spin operator earned.

$$\boxed{\;\text{The entangler's coupling }J=\tfrac12(\sqrt{U^2{+}16t^2}-U)\text{ is derived from }t(m)\text{ (measured from the exact `ca\_dirac` stepper) and }U(m)=2\arcsin m\text{ (the Chapter 6 mass gap); wired live into `casim`, a two-cell run reaches }S=\ln2\text{ at the independently-predicted tick }\tau=7\text{ to }3\times10^{-7}\text{; checkpoint/resume bit-identical}\;}\tag{R25.10}$$

(F214: 6/6 checks PASS; `CL188`, `live`, `exact`.)

### 25.3.3 Field-native second quantization: J and entanglement emerge from genuine fermions (F217)

F214's derivation used an *effective* two-site Hubbard model, valid at half filling — leaving open whether
$J$ is genuinely a property of the model's fermions or an artefact of the effective spin description. F217
builds the real thing: a full Jordan–Wigner Fock space with exact fermionic anticommutation
($\{c_i,c_j^\dagger\}=\delta_{ij}$ to machine zero), evolved under the genuine Hubbard Hamiltonian with both
couplings taken from the model. The full second-quantized singlet–triplet gap **equals** F214's closed-form
$J$ to $<10^{-12}$ (worst $4.7\times10^{-16}$) at every tested mass — the effective spin model was correct,
and is now derived rather than posited. The field-native dynamics is genuinely richer at finite $U$: real
hopping also excites virtual **double occupancy** (charge fluctuations), so the spin sector reaches only
$S\approx0.68$ at $m=0.5$, with $\sim19\%$ of the weight having leaked into doublon states; as $U/t\to\infty$
this leakage vanishes and the peak entanglement converges cleanly to $\ln2$, exactly the point where the
Hubbard dynamics reduces to F212/F214's exchange gate. This completes a derivational tower — hopping $\to$
second quantization $\to$ the exchange gate as the large-$U$ limit — and is wired live as `FermionChainChannel`,
generating live two-site spin entanglement $0\to0.692$ with checkpoint/resume bit-identical.

$$\boxed{\;\text{The genuine second-quantized (Jordan-Wigner) singlet-triplet gap equals F214's effective-model }J\text{ exactly (}<10^{-12}\text{), not merely approximately; as }U/t\to\infty\text{ the field-native dynamics converges cleanly to the pure exchange gate (peak entropy }\to\ln2\text{, doublon leakage }0.127\to0.002\text{); the effective spin model is a large-}U\text{ limit of genuine fermion physics, not an independent assumption}\;}\tag{R25.11}$$

(F217: 5/5 checks PASS; `CL191`, `live`, `exact`.)

## 25.4 The derivation — Group C: quantum computation on the native substrate

### 25.4.1 The substrate computes: exact gate compilation and live algorithms (F218)

F212 proved the exchange gate is a perfect entangler by an existence theorem; F218 makes this constructive.
Because $[\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B,\,Z_AZ_B]=0$ and conjugation by $\sigma_z\otimes I$ flips
the sign of the $XX+YY$ piece, two native exchange gates sandwiching a $\sigma_z$ give a pure $ZZ$ interaction
$e^{i\pi ZZ/4}$ (verified to $5\times10^{-16}$), from which CZ and CNOT are assembled using only native SU(2)
rotors, matching the textbook gates to $6\times10^{-16}$ — a constructive proof that the lattice exchange
interaction plus single-cell rotations is universal. Running through the production engine's new
`QuantumCircuitChannel` (one circuit layer per CA tick), a 4-item Grover search collapses onto the marked
state with certainty after the exact single-iteration rotation, and Deutsch–Jozsa correctly classifies all
four oracles with a single query — genuine algorithms, in the same engine that carries the photon, gauge, and
gravity sectors, with checkpoint/resume bit-identical mid-circuit.

$$\boxed{\;\text{CZ and CNOT compile exactly (}6\times10^{-16}\text{) from two native exchange gates + a }\sigma_z\text{ conjugation + SU(2) rotors; Grover and Deutsch-Jozsa run live in the production `casim` engine with deterministic, correct answers and bit-identical checkpointing}\;}\tag{R25.12}$$

(F218: 5/5 checks PASS; `CL192`, `live`, `exact`.)

### 25.4.2 Computing on genuine matter (F220)

F217 built the genuine Fock space; F218/F222 ran algorithms on an abstract register sitting on designated
cells. F220 runs gates and a full algorithm **directly on the second-quantized matter**. Taking a logical
qubit to be the spin of a singly-occupied site, single-qubit gates are exact fermionic operators
$\exp(-i2\theta\,\hat n\cdot\mathbf S_s)$ that leave the one-fermion-per-site sector exactly invariant (zero
leakage, verified to $8.3\times10^{-16}$); the two-qubit entangler is not a matrix at all but the genuine
Hubbard time-evolution $e^{-iHt}$, whose emergent super-exchange (F214/F217) becomes the exact exchange gate
as $U/t\to\infty$ (fidelity $0.979\to1.0000$, entropy $\to\ln2$). At finite $U$ the field-native CNOT
constructed this way carries $<1\%$ error, leakage-limited by virtual doublons — but the Deutsch–Jozsa
verdict is **exactly correct** on all four oracles despite this leakage, because the algorithm's output is a
threshold decision the sub-percent leakage cannot flip. This is the honest picture of computing on genuine
matter: real charge-fluctuation error is present in the gate hardware, and a well-designed algorithm's
discrete answer survives it — the same principle underlying real fault-tolerant decoding.

$$\boxed{\;\text{Single-qubit gates are exact fermionic operators with zero leakage; the two-qubit entangler is literally the lattice's own Hubbard time-evolution, reaching fidelity }1.0000\text{ as }U/t\to\infty\text{; Deutsch-Jozsa's threshold verdict survives sub-percent doublon leakage on every oracle}\;}\tag{R25.13}$$

(F220: 5/5 checks PASS; `CL194`, `live`, `exact`.)

### 25.4.3 Fault tolerance: Kraus channels and stabilizer codes (F221)

F220 exposed a genuine native decoherence source — virtual doublon leakage. F221 gives the engine the two
missing ingredients to study fault tolerance on the same substrate: exact Kraus-channel application on the
full density matrix (bit-flip, phase-flip, depolarizing, amplitude-damping, each verified CPTP to $10^{-16}$)
and stabilizer codes built entirely from the model's own native gates (exchange-derived CNOT fan-outs plus
Hadamards). The 3-qubit bit-flip code's corrected fidelity matches the exact closed form
$F=(1{-}3p^2{+}2p^3)+(3p^2{-}2p^3)(2ab)^2$ to $4.4\times10^{-16}$, with logical infidelity suppressed to
$O(p^2)$ against the uncorrected $O(p)$ — the entire purpose of a code, reproduced exactly. The 9-qubit Shor
code corrects an **arbitrary** single-qubit error (all 27 combinations of $\{X,Y,Z\}$ on each of 9 qubits) to
$4.4\times10^{-16}$, satisfying the Knill–Laflamme conditions to machine precision. Wired live as
`ErrorCorrectionChannel`, a logical qubit holds at $F=0.9947$ over 8 noise rounds while an uncorrected control
decays to $0.2690$.

$$\boxed{\;\text{Kraus decoherence channels are exact CPTP maps (}10^{-16}\text{); the 3-qubit code's corrected fidelity matches its exact closed form to }4.4\times10^{-16}\text{, giving }O(p^2)\text{ logical-error suppression; the 9-qubit Shor code corrects an arbitrary single-qubit error (all 27 cases) to }4.4\times10^{-16}\text{; a live logical qubit holds }F=0.995\text{ over 8 rounds vs an uncorrected control's }0.27\;}\tag{R25.14}$$

(F221: 5/5 checks PASS; `CL195`, `live`, `exact`.)

### 25.4.4 Scale: the register stays exact to n≈12 (F222)

F218 exercised only 2-qubit algorithms. F222 asks whether the genuine $2^n$ register stays stable as $n$
grows, or degrades into floating-point mush at the exponential cost. A native controlled-phase and a fully
compiled native CCZ (the Barenco construction, matching $\mathrm{diag}(1,\dots,-1)$ to $2.2\times10^{-15}$)
extend the exact universality proof to three-qubit controlled gates, and multi-controlled Z/X decompose into
these exactly. Across $n$-qubit Grover ($n=3$ to $12$), QFT ($n=3$ to $8$), Bernstein–Vazirani ($n=4$ to $12$),
and GHZ ($n$ to $12$), the register's norm drifts by only $\sim10^{-13}$ across a 12-qubit, $\sim600$-gate-layer
run, success probabilities match closed-form predictions to $<10^{-6}$, the QFT reproduces the discrete
Fourier transform to $<10^{-10}$ and inverts exactly, and GHZ holds $\ln2$ entanglement on every cut out to
$n=12$ — a stable universal quantum computer at scale, not merely a 2-qubit proof of concept, with checkpoint
integrity preserved mid-computation.

$$\boxed{\;\text{Native CCZ and multi-controlled gates extend exact universality to }n\text{-qubit circuits; Grover, QFT, Bernstein-Vazirani, and GHZ all run exactly to }n\approx12\text{ with norm drift }\sim10^{-13}\text{ (floating-point, not physics) and correct answers throughout}\;}\tag{R25.15}$$

(F222: 5/5 checks PASS; `CL196`, `live`, `exact`.)

### 25.4.5 Route 1 — SI-anchored super-exchange against cold-atom data (F224)

The QC thread through F222 proved the model *supports* quantum computation but reproduced only textbook QM
in dimensionless units — a consistency result, not a confrontation with data. F224 puts the derived
super-exchange in SI units and confronts it with the cleanest existing measurement of super-exchange dynamics.
The fundamental lattice is Planckian ($a=6.598\,\ell_P$, per Chapter 17's canonical cell), so the physical,
testable content is the RG-invariant *dimensionless* relation $J(t,U)$ (invariant under Chapter 14's block-spin
coarse-graining), realized on whatever emergent scale a real quantum simulator operates at. The model's exact
two-site gap reduces exactly to the textbook $4t^2/U$ scaling as $t\ll U$, and its dimensionful entangling
time $1/4J$ lands at $0.25$–$50$ ms across Trotzky et al.'s (Science 2008) measured $5$ Hz–$1$ kHz optical-
lattice coupling range — the same millisecond band on which coherent super-exchange oscillations were
time-resolved experimentally. The finding also makes a concrete, falsifiable refinement: at Trotzky's own
symmetric-well operating point $J/U=0.08$, the model's **exact** two-site gap is $6.93\%$ **below** the
textbook leading-order $4t^2/U$ — a precision super-exchange measurement in that regime should see this
departure.

$$\boxed{\;\text{The model's derived entangling time }1/4J\text{ lands at }0.25\text{–}50\text{ ms across Trotzky et al.'s measured }5\text{ Hz–}1\text{ kHz cold-atom super-exchange band; the exact two-site gap predicts a falsifiable }-6.93\%\text{ departure from }4t^2/U\text{ at the measured symmetric-well operating point}\;}\tag{R25.16}$$

(F224: 4/4 checks PASS; `CL198`, `live`, `exact`.)

### 25.4.6 Route 2 — doublon leakage against a measured semiconductor spin-qubit (F225)

F220 identified virtual doublon leakage as the field-native gate's native error. In a real semiconductor
exchange-qubit this is not an analogy — it is the physical error, the admixture of the doubly-occupied
singlet $S(0,2)$ via virtual tunnelling. The closed-form leakage $d=\tfrac12(1-1/\sqrt{1+(4t/U)^2})$ equals
F217's genuine second-quantized ground-state double occupancy to $5.6\times10^{-17}$, scales as $(2t/U)^2$
in the $t\ll U$ limit (log-log slope $1.9997$), and — with **no adjustable parameter** once $t/U$ is fixed —
matches the GaAs singlet-triplet exchange qubit's measured $0.13\%$ leakage (Cerfontaine et al., Nature
Communications 2020) at $t/U\approx0.018$, a standard exchange-qubit operating regime. This is a consistency
success rather than a discriminating one (the leakage law is standard two-site Hubbard physics, not unique
to this model), but the model's value-add is unifying this leakage, the super-exchange coupling, and the
gate time into one derived family through the single ratio $t/U$.

$$\boxed{\;\text{The closed-form doublon leakage }d=(2t/U)^2\text{ (leading order) matches the measured GaAs exchange-qubit leakage }0.13\%\text{ at }t/U\approx0.018\text{ with no free parameter, consistent with the same virtual-tunnelling physics measured in real semiconductor spin qubits}\;}\tag{R25.17}$$

(F225: 4/4 checks PASS; `CL199`, `live`, `exact`.)

### 25.4.7 Route 3 — exact Tsirelson saturation, and CL200's investigated status (F226)

F226 asks the sharpest possible discrimination question: does the genuine register saturate Tsirelson's
bound $2\sqrt2$ exactly (Bell-indistinguishable from QM, no near-term test) or predict a discreteness
deviation testable against loophole-free Bell data? Starting from the product $|\!\uparrow\downarrow\rangle$,
one application of the F212/F214 exchange gate produces a state whose CHSH value, maximized over all
measurement directions (the convention-free Horodecki criterion), is
$$S_\text{max}=2\sqrt2=2.8284271247\ldots,\qquad\text{residual }1.8\times10^{-15}.$$
There is no $O(1)$ deviation and no $O(a\cdot p)$ correction: **the emergent theory is quantum mechanics on
this observable.** The one place discreteness can enter — Planckian granularity of the achievable analyzer
angle, $\delta\phi=E/E_\text{lat}$ — produces a deviation that is *quadratic*, not linear, because CHSH is
stationary at its optimum ($\delta S=-3\sqrt2\,\delta\phi^2$, fitted curvature $-4.25$ vs the exact $-4.243$).
Even at $E=1$ GeV this predicted deviation is $\sim10^{-37}$, more than 35 orders of magnitude below the
smallest loophole-free Bell experiment's error bar (Hensen et al. 2015, Giustina et al. 2015, Shalm et al.
2015). **The model is Bell-indistinguishable from QM**, and this is reported as the correct, honest, and
still scientifically valuable outcome, not a failure. F226's own G4 result is directly relevant to Chapter 1's
open ontology question (§25.7 below): the violation is reproduced for *freely and independently chosen*
measurement settings, with the entangled state equal to the singlet up to a fixed, setting-independent local
unitary — the model violates Bell **by being genuine quantum mechanics**, not by exploiting a superdeterministic
setting–source correlation.

**CL200's `withdrawn` status, investigated.** The same pattern found at CL189/CL193 (§25.2.4/25.2.5): CL200's
own text quotes F226's routine "Confirmed — 5/5 checks PASS..." line as an inferred "withdrawal banner." F226
carries no supersession language and appears in no `supersessions.yaml` record. Read as live.

$$\boxed{\;\text{The genuinely-generated entangled state saturates the Tsirelson bound exactly (}1.8\times10^{-15}\text{), for freely chosen settings, with no superdeterministic mechanism invoked; the only discreteness entry is quadratic and Planck-suppressed to }\sim10^{-54}\text{ at optical energies — Bell-indistinguishable from QM; CL200's `withdrawn` label is the same investigated bookkeeping artifact as CL189/CL193}\;}\tag{R25.18}$$

(F226: 5/5 checks PASS; `CL200`, front matter reads `withdrawn`, investigated here and read as live.)

### 25.4.8 Route 4 — no observable intrinsic decoherence floor (F227)

F226's companion asks whether a long quantum computation shows any intrinsic departure from perfect unitarity.
At the effective-theory level the emergent gates are exact unitaries with zero intrinsic decoherence (F222's
$\sim10^{-13}$ register drift is floating-point round-off, not physics). At the substrate level, Chapter 20's
own RG-irrelevance result for Lorentz-violating operators ($\lambda_n=b^{-n}$, $n\ge2$) bounds any residual
decoherence rate at $\Gamma\lesssim E^3/(\hbar E_\text{lat}^2)$, giving $\sim8.6\times10^{-40}\,\text{s}^{-1}$
for an optical-scale qubit — a floor that sits $9$ to $31$ orders of magnitude below the best measured
decoherence rates (a 2025 Sr optical-lattice clock's $T_2^*=118$ s; a 2025 transmon's $T_{2,\text{echo}}=1.06$
ms) and the deepest proposed collapse-model rates (GRW/CSL, Diósi–Penrose). The Lieb–Robinson velocity is
exactly $c_\text{lat}=1/\sqrt3$ (reusing Chapter 6's dispersion identity), and the register's causal cone is
exactly zero outside $r>4t$, machine precision. The model is a **unitary theory with no objective collapse**,
predicting the continued null results of every collapse-model search — a genuine, if currently untestable,
distinction from GRW/CSL/DP. The one non-Planck-suppressed decoherence channel identified anywhere in this
chapter, the emergent doublon leakage of §25.4.6, is separated from the fundamental floor by $\sim50$ orders
of magnitude and must never be conflated with it.

$$\boxed{\;\text{The intrinsic decoherence floor is exactly zero at the effective-theory level and Planck-suppressed to }\lesssim10^{-40}\,\text{s}^{-1}\text{ at the substrate level, }9\text{–}31\text{ orders below every measured decoherence rate and every proposed collapse-model bound; the Lieb-Robinson velocity is exactly }c_\text{lat}=1/\sqrt3\text{; the model is unitary with no objective collapse}\;}\tag{R25.19}$$

(F227: 5/5 checks PASS; `CL201`, `live`, `exact`.)

## 25.5 The derivation — Group D: does the interacting sector actually thermalise?

### 25.5.1 The GGE gives way to genuine (ETH) thermalisation — but not from one interaction alone (F376)

Chapter 20's own lattice-native thermodynamics (F300, cited not re-derived here) proved that the free
(quadratic) photon sector's branch occupations are $2N$ exactly conserved charges, so its stationary state is
a generalised Gibbs ensemble (GGE), never a genuine Gibbs state — and the same equilibrium machinery, extended
to the fermionic sector (F309), closed with the identical open caveat: nothing shown so far demonstrates the
fermionic sector actually *thermalises*. Both findings named the same next step: thermalisation on Chapter
13a's real-time link Hamiltonian (R13a.13) — but that construction, read literally, carries only static
charges (F110's own text: "dynamical matter is not yet coupled"), so coupling it to genuine fermion dynamics
is a separate, larger engineering project this finding does not attempt.

F376 instead asks the smallest faithful version of the actual open question, on a quadratic fermion lattice
with the identical conserved-charge structure Chapter 20 already established: an open spinless-fermion chain
with nearest- and next-nearest-neighbour density interactions, $H=-t\sum(c_i^\dagger c_{i+1}+\text{h.c.})+
V_1\sum n_in_{i+1}+V_2\sum n_in_{i+2}$. The result has two tiers, and the second is the informative one. Turning
on $V_1$ alone does **not** break the free sector's GGE-like structure: the resulting $t$–$V_1$ model is
exactly Jordan-Wigner dual to the XXZ spin chain, and remains Bethe-ansatz **integrable** for every $V_1$ —
one exactly solvable model traded for another. Adding a second, next-nearest-neighbour term $V_2$ genuinely
breaks integrability, and three independent, standard diagnostics — computed on an exactly diagonalized
Hilbert space up to $L=14$ ($\dim=3432$), with a reflection-parity block-diagonalization validated two
independent ways to $2.5\times10^{-16}$ — agree that the system crosses over to genuine (ETH) thermalisation:
the level-spacing ratio $\langle r\rangle$ separates from Poisson ($0.9\sigma$) toward GOE ($1.3\sigma$ from
the Wigner-Dyson value) as $L$ grows for the generic ($V_1,V_2\neq0$) case, while the $V_1$-only case's
$\langle r\rangle$ converges toward Poisson; the domain-wall-quench entanglement plateau's fraction of the
volume-law ceiling is essentially $L$-independent for the generic case (a genuine, size-extensive entanglement
density) while it *falls* with $L$ for the integrable case; and the eigenstate-to-eigenstate fluctuation of
the entanglement entropy — the direct ETH signature — shrinks by nearly half from $L=10$ to $L=14$ for the
generic case while not shrinking at all for the integrable case. A declared control (forcing $V_2\to0$ inside
the "generic" run) correctly turns exactly the regime-separation checks red, confirming the diagnostics are
measuring the intended effect.

$$\boxed{\;\text{A nearest-neighbour interaction alone (}V_1\text{) trades one integrable model (Jordan-Wigner-dual to XXZ) for another — the GGE-like structure survives; adding a next-nearest-neighbour term (}V_2\text{) genuinely breaks integrability, and three independent diagnostics (level statistics, entanglement-plateau extensivity, eigenstate-fluctuation shrinkage) all confirm the crossover to genuine ETH thermalisation as }L\text{ grows to }14\;}\tag{R25.20}$$

(F376: 7/7 checks PASS, one declared control verified red; independently reviewed 2026-09-06, **CONFIRMED**;
`CL305`, `live`, `quantitative`.)

## 25.6 Results table

| # | Finding | Statement | Exactness | Claim card |
|---|---|---|---|---|
| R25.1 | F210 | Superconductivity is the electric S-dual of F86 colour confinement; both BCS universals exact ($3.8\times10^{-16}$, $<10^{-9}$); $2e$ charge, $\Phi_0=h/2e$, persistent current all exact | exact/machine | CL184, live |
| R25.2 | F211 | Real literature couplings through the F210 gap equation reproduce measured $T_c$ (7 elements) at Allen-Dynes level to mean 14.3% | quantitative | CL185, live |
| R25.3 | F213 | Electron-phonon coupling model-native ($D=\tfrac23E_F$ from F64); gap ratio 3.528 is a weak-coupling limit, rising to 4.4–4.6 for strong coupling | machine ($D$)/quantitative | CL187, live |
| R25.4 | F215 | Eliashberg $Z=1+\lambda$ emerges dynamically on the Matsubara axis; $T_c$ from $(\lambda,\omega_\text{log},\mu^*)$ matches at $r=0.975$, no fit | quantitative | **CL189 — investigated, live, not a real withdrawal** |
| R25.5 | F218b | $\alpha^2F(\omega)$ derived from F64 (no new input); $T_c$ shape-insensitive; Padé-continued gap ratio dynamic, $r=0.988$ | exact ($\omega_\text{log}$ identity)/quantitative | **CL193 — investigated, live, not a real withdrawal** |
| R25.6 | F242 | $\mu^*$ derived from F64's Thomas-Fermi screening limit, zero fit parameters; Allen-Dynes mean error $14.3\%\to$**6.3%** | machine ($\mu(r_s)$ closed form) | CL213, live |
| R25.7 | F374 | Real cutoff bug found and fixed ($\sqrt e$ factor); Eliashberg floor plateaus at 16–17% — disclosed NO-GO on beating Allen-Dynes via the solver | quantitative | none (D12 refinement) |
| R25.8 | F375 | Sourced DFT $N(E_F)$ for Nb crosses the target: Allen-Dynes mean error $6.3\%\to$**4.9%**; Ta explicitly, checkably left open | quantitative | none (D12 refinement) |
| R25.9 | F212 | Genuine $2^n$ register generates $S:0\to\ln2$ from a product input (residual $8\times10^{-16}$); mean-field provably capped at fidelity $\tfrac12$ | exact-algebraic | CL186, live |
| R25.10 | F214 | Entangler coupling $J$ derived from `ca_dirac` hopping + mass gap; live channel reaches $\ln2$ at the predicted tick $\tau=7$ to $3\times10^{-7}$ | exact-algebraic | CL188, live |
| R25.11 | F217 | Genuine second-quantized $J$ equals the effective-model $J$ to $<10^{-12}$; large-$U$ limit recovers the pure exchange gate | exact-algebraic | CL191, live |
| R25.12 | F218 | CZ/CNOT compile exactly ($6\times10^{-16}$) from native exchange + rotors; Grover/DJ run live in the production engine | exact-algebraic | CL192, live |
| R25.13 | F220 | Exact fermionic single-qubit gates (zero leakage); entangler is genuine Hubbard time-evolution; DJ verdict correct despite sub-percent leakage | exact-algebraic/quantitative | CL194, live |
| R25.14 | F221 | Exact CPTP Kraus channels; 3-qubit code's fidelity matches its closed form to $4.4\times10^{-16}$ ($O(p^2)$ suppression); Shor code corrects all 27 single errors | exact-algebraic | CL195, live |
| R25.15 | F222 | Native CCZ + multi-controlled gates scale Grover/QFT/BV/GHZ to $n\approx12$ with norm drift $\sim10^{-13}$ (floating point) | machine | CL196, live |
| R25.16 | F224 | Entangling time reproduces Trotzky et al.'s measured ms-scale cold-atom super-exchange band; falsifiable $-6.93\%$ exact-gap refinement predicted | quantitative + prediction | CL198, live |
| R25.17 | F225 | Doublon leakage law matches measured GaAs exchange-qubit leakage (0.13%) with zero free parameters | exact-algebraic + data match | CL199, live |
| R25.18 | F226 | CHSH on the genuinely-generated state saturates Tsirelson exactly ($1.8\times10^{-15}$); Bell-indistinguishable from QM; discreteness correction $\sim10^{-54}$ | exact-algebraic | **CL200 — investigated, live, not a real withdrawal** |
| R25.19 | F227 | Intrinsic decoherence floor zero (effective)/Planck-suppressed ($\lesssim10^{-40}\,\text{s}^{-1}$); Lieb-Robinson velocity $=c_\text{lat}$ exactly; unitary with no objective collapse | exact (LR speed)/quantitative | CL201, live |
| R25.20 | F376 | $V_1$ alone stays integrable (XXZ); $V_1{+}V_2$ genuinely breaks integrability — three diagnostics confirm ETH crossover to $L=14$ | quantitative | CL305, live |

## 25.7 Comparison with measurement

This chapter carries the monograph's widest span of real-world data confrontations in one place.

**Niobium's superconducting $T_c$ and density of states.** Feeding literature couplings through the model's
Eliashberg/Allen-Dynes machinery: the seven-element mean Allen-Dynes error starts at $14.3\%$ with tabulated
inputs (F211), tightens to $6.3\%$ once $\mu^*$ is derived rather than fit from the same F64 dielectric that
carries gravity (F242), and crosses to $4.9\%$ once a single, independently-sourced DFT density of states for
niobium replaces the free-electron approximation (F375) — Nb's own individual error falling from $10.6\%$ to
$0.2\%$. Pb and Ta land within $0.1$–$0.3\%$ of measurement throughout; Al remains the weak-coupling outlier
this project has repeatedly and honestly attributed to $T_c$'s exponential sensitivity to $\lambda$, not a
model defect.

**Cold-atom super-exchange dynamics.** The model's derived entangling time $1/4J$, expressed in physical
units via the RG-invariant dimensionless relation $J(t,U)$, lands at $0.25$–$50$ ms across Trotzky et al.'s
measured $5$ Hz–$1$ kHz optical-lattice coupling range — the same millisecond band in which coherent
super-exchange oscillations were experimentally time-resolved (F224).

**Semiconductor exchange-qubit leakage.** The model's closed-form doublon leakage $d=(2t/U)^2$, with no
adjustable parameter once $t/U$ is fixed, matches the GaAs singlet-triplet exchange qubit's measured $0.13\%$
leakage (Cerfontaine et al. 2020) at $t/U\approx0.018$ — a standard operating regime for these devices (F225).

**The Tsirelson bound.** CHSH measured on the model's own genuinely-generated entangled state, maximized over
all measurement directions, gives $S=2\sqrt2$ to a residual of $1.8\times10^{-15}$ — exact machine-precision
agreement with the quantum-mechanical maximum, for freely and independently chosen settings, with a predicted
discreteness deviation more than 35 orders of magnitude below the resolution of the tightest loophole-free
Bell experiments (F226).

Across all four confrontations, the model does not merely land "in the right ballpark" — it lands within, or
very close to, the standard theoretical accuracy already accepted for that specific class of calculation
(Eliashberg/Allen-Dynes theory's own accuracy for $T_c$; exact two-site Hubbard-model accuracy for the
cold-atom and quantum-dot comparisons; exact quantum mechanics for the Bell bound), which is exactly the
outcome a correct emergent-physics derivation should produce.

## 25.8 What was excluded, and why

**Superconductivity on the bare fundamental lattice.** Excluded on structural grounds, not by omission: the
bare lattice's only inter-electron channel is repulsive (Coulomb, via the Chapter 9 photon) and its only
intrinsic bosonic mode is the $G$-suppressed graviton wave. F210 states plainly that conventional
superconductivity requires an emergent material crystal (Chapter 24's block-spin atoms); the "universe in a
bottle" does not spontaneously superconduct at the Planck scale.

**Beating Allen-Dynes' 6.3% $T_c$ accuracy via the Eliashberg solver alone.** F374's disclosed, quantified
NO-GO (§25.2.7, R25.7): five independent attacks — finite-matrix-size checks, a cutoff-factor scan, the
model's own exact strong-coupling shape factor, and dropping the Coulomb window entirely — all converge on a
$16$–$17\%$ floor for the numerical Eliashberg solve, well short of the closed-form Allen-Dynes target.
Cross-checked against the literature (Szczęśniak's independently reported $15$–$25\%$ disagreement between
published $\mu^*$ conventions for Al and Pb alone), this is recorded as an established feature of Eliashberg
numerics generally, not a model-specific shortfall — an honestly disclosed shortfall rather than a quietly
buried one.

**Tantalum's density-of-states correction.** F375 explicitly, machine-checkably declines to extend its
niobium DOS correction to tantalum by analogy, absent an equally solid sourced number — a disclosed open
item, not a silently applied guess.

**A generic interaction breaking the free sector's equilibrium structure.** F376's own two-tier result:
a nearest-neighbour interaction alone is *excluded* as sufficient to break the GGE structure — it merely
trades the free sector's integrability for the $t$–$V_1$ model's own, different integrability (exact
Jordan-Wigner duality to XXZ, Bethe-ansatz solvable for every $V_1$). Genuine thermalisation requires a
term that generically breaks integrability, not merely "an interaction" in the abstract.

**The three claim-card `withdrawn` labels (CL189/F215, CL193/F218b, CL200/F226), investigated and excluded
as real withdrawals.** Each card's own text explicitly quotes the finding's routine
`**Status:** Confirmed — N/N checks PASS` line as its inferred "supersession/withdrawal banner" — the same
mechanical seeding-pass artifact this monograph has now documented in six prior instances across five
chapters (Chapters 7, 8, 9, 12, 13b, 19). None of the three findings carries genuine retraction language, and
none appears in any of `supersessions.yaml`'s 23 records. This chapter treats all three findings as live,
correctly-reported results, exactly as their own status lines state.

## 25.9 What is still open

1. **The doublon-leakage tolerant code (F221's own frontier).** The measured semiconductor leakage is a
   genuine *leakage* error, not a Pauli error, and F221's stabilizer codes assume Pauli noise; a
   leakage-reduction unit plus a leakage-tolerant code is what the field-native sector actually needs for an
   end-to-end error budget.
2. **A distance-scaling (surface) code and a real logical-error-rate threshold study.** F221 fixes single
   errors exactly; a genuine threshold theorem needs a code family with growing distance and a decoder, plus
   circuit-level (not just between-round) noise — named explicitly as the fault-tolerance frontier.
3. **Coupling F110's real-time link Hamiltonian to genuine dynamical matter** (F376's own scope item, and
   F300/F309's literal named next step) remains fully open — a separate, larger engineering project this
   chapter's minimal interacting extension deliberately does not attempt.
4. **Extending F376 beyond $L=14$** with a sparse/Lanczos solver to firm up the finite-size trend, and
   constructing the full quasi-local-charge GGE for the integrable $t$–$V_1$ point so the entanglement
   comparison has the correct thermal reference rather than only the qualitative ceiling-fraction argument.
5. **Threading the model's own BCC gauge-sector coupling constants into $V_1,V_2$** in place of the toy
   values $0.5/0.5$ used in F376, if a natural lattice-native interaction channel is identified.
6. **A precision test of F224's $-6.93\%$ exact-gap refinement** against a modern high-resolution cold-atom
   super-exchange measurement — a concrete, named, currently unattempted confrontation.
7. **The absolute cold-atom and semiconductor-qubit couplings are not independently constrained by the
   model's own $t$–$U$ tie** ($U=2\arcsin m$, $t$ from `ca_dirac`, both from one mass $m$) — Routes 1 and 2
   (F224/F225) are consistency successes, not yet discriminating tests, an honest scope limit both findings
   state themselves.

## 25.10 Falsifiers, and a closing remark

- **R25.1–R25.8 (superconductivity).** A measured superconductor whose gap ratio or heat-capacity jump
  departs from the exact BCS universals (R25.1) beyond the coupling/cutoff-independence this chapter
  verifies would falsify the identification of this construction with genuine BCS pairing. A future,
  independently-sourced density of states for a $d$-band metal that, applied via F375's exact-at-$\alpha=1$
  generalization, pushes the Allen-Dynes error back above $6.3\%$ would undercut R25.8's specific correction
  (though not the underlying $\mu^*$ derivation, R25.6, which F375 leaves untouched).
- **R25.9–R25.11 (entanglement microscopics).** A future measurement of the model's own super-exchange
  coupling $J(m)$ at a value inconsistent with $t(m)$ and $U(m)=2\arcsin m$ (both independently fixed
  elsewhere in the model) would falsify the derivation chain from hopping to entanglement rate.
- **R25.16/R25.17 (Routes 1/2).** F224's own stated falsifier: a precision super-exchange measurement in the
  moderate-$t/U$ regime that does *not* show the predicted $-6.93\%$ departure from $4t^2/U$ would falsify
  the exact-gap refinement specifically (not the leading-order agreement, which is already textbook Hubbard
  physics).
- **R25.18/R25.19 (Routes 3/4).** Both are explicitly non-discriminating by their own findings' account: no
  near-term Bell experiment or decoherence measurement could falsify either result, since the predicted
  departures from standard QM sit $35$–$50+$ orders of magnitude below current experimental resolution. The
  falsifier, honestly, is structural: only a future *detection* of an intrinsic decoherence floor or a Bell
  violation departing from $2\sqrt2$ would engage these results at all.
- **R25.20 (thermalisation).** F376's own stated falsifier: extending the exact diagonalization to
  $L=16$–$20$ and finding the integrable regime's level statistics *not* continuing to converge toward
  Poisson, or the generic regime's ETH fluctuation *not* continuing to shrink, would directly contradict
  this finding's central two-tier claim.

**On the ontology question Chapter 1 raised and Chapter 5 continued.** Chapter 1 (§1.3) stated explicitly
that this project takes no position on whether a 't Hooft-style hidden deterministic layer exists beneath the
per-cell amplitude, and Chapter 5 (§5.6) showed the model's own unitary substrate *suffices* to derive the
Born rule and classicality with no such layer — a sufficiency, not a necessity, result, since both readings
remain, by the sources' own account, experimentally indistinguishable. This chapter's Group B/C findings do
not close that question, and this chapter does not claim otherwise. What they add is the sharpest concrete
instance the monograph has built of what "sufficiency" costs and delivers: a genuine $2^n$ many-body register,
built with zero entanglement inserted by hand, generates entanglement dynamically under the model's own
unitary rule (F212), at a rate derived — not fit — from the same hopping amplitude that sets $c_\text{lat}$
and the fermion mass gap (F214/F217), and that dynamically-generated state violates Bell's inequality at the
exact Tsirelson bound for freely and independently chosen measurement settings, with no superdeterministic
mechanism invoked anywhere in the construction (F226). The model therefore violates Bell **by being genuine
quantum mechanics**, not by any classical shortcut — exactly the reading Chapter 1 left open as one live
possibility and exactly the case this chapter's dynamics, not merely its formalism, now demonstrates in
practice. Whether a deeper deterministic layer could still exist beneath this same amplitude remains, as
Chapter 1 said it would, undecided by anything in this monograph.

This is also, appropriately, the monograph's last content chapter, and its reach is worth stating plainly
rather than left to speak for itself: a single discrete update rule, fixed in Chapter 3 from seven postulates
stated in Chapter 1, has now been shown — not asserted, shown, with residuals reported to their actual digit —
to reproduce measured niobium superconductivity to a few percent, cold-atom super-exchange oscillations to
their measured millisecond timescale, a semiconductor spin-qubit's measured leakage with zero free parameters,
and the Tsirelson bound of loophole-free Bell experiments to fifteen digits, using no machinery beyond what
Chapters 2 through 18 already built for dimension count, fermion content, gauge coupling, and gravity. Every
number in this chapter's results table traces back, by an explicit citation chain, to the same handful of
postulates and the same handful of derived structural constants ($c_\text{lat}$, the fermion mass $m$, the F64
dielectric $K$) that the rest of the monograph uses for leptons, hadrons, and cosmology. That a single lattice
rule's reach extends this far — from a niobium wire to a Bell-test photon pair — is the central empirical
weight behind this monograph's founding claim: that the universe, modeled as a cellular automaton on a bottle-
sized lattice, is not merely internally consistent, but is, so far, difficult to tell apart from the one we
actually measure.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–24's table.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\Delta(0)$, $T_c$ | The BCS/Eliashberg gap and critical temperature; $2\Delta(0)/k_BT_c=2\pi/e^\gamma$ and $\Delta C/C_n=12/(7\zeta(3))$ are coupling-independent universals | §25.2.1 |
| $\lambda$, $\mu^*$ | The Eliashberg electron-phonon coupling and Morel-Anderson Coulomb pseudopotential; both derived here from the Chapter 18 dielectric $K$'s strain-response and screening limits respectively | §25.2.3, §25.2.6 |
| $Z(i\omega_n)$ | The Eliashberg mass-renormalization function on the Matsubara axis; $Z(i\omega_0)\to1+\lambda$ | §25.2.4 |
| $\alpha^2F(\omega)$ | The Eliashberg spectral function; derived here as $\lambda\omega^2/\omega_\text{max}^2$ from the deformation-potential vertex | §25.2.5 |
| $J$ | The antiferromagnetic super-exchange coupling between two lattice fermions; $J=\tfrac12(\sqrt{U^2+16t^2}-U)$, derived from the hopping $t(m)$ and mass gap $U(m)=2\arcsin m$ | §25.3.2 |
| $U_\text{exch}(\theta)$ | The native two-qubit entangling gate, $e^{-i\theta\,\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$; a perfect entangler at $\theta=\pi/8$ | §25.3.1 |
| $d$ | The doublon (double-occupancy) leakage fraction out of the one-fermion-per-site computational subspace; $d=(2t/U)^2$ at leading order | §25.4.6 |
| $S_\text{CHSH}$ | The CHSH Bell parameter; the model's genuinely-generated entangled state saturates $2\sqrt2$ exactly | §25.4.7 |
| $\langle r\rangle$ | The mean level-spacing ratio (Oganesyan-Huse), distinguishing Poisson (integrable, $0.3863$) from GOE (chaotic/thermalising, $0.5307$) spectral statistics | §25.5.1 |

*No new gap logged in `docs/monograph/GAPS.md` by this chapter: the three claim-card `withdrawn`
investigations (CL189/F215, CL193/F218b, CL200/F226, §25.2.4/§25.2.5/§25.4.7) are the same mechanical
seeding-pass bookkeeping artifact this monograph has already logged and diagnosed in Chapters 7, 8, 9, 12,
13b, and 19 — a further, un-numbered instance of an already-disclosed pattern, not a new documentation-layer
hole (consistent with Chapter 9's own precedent of not re-logging a repeat instance of this exact artifact).
Every other open item found while reading these 20 findings (F374's disclosed NO-GO, F375's explicitly
unattempted tantalum correction, F376's own stated scope limits) is already named, with a stated reason,
inside the findings' own text, not papered over by any index, claim card, or cross-reference this chapter
checked. No finding, claim card, module, or test record was created or modified in the writing of this
chapter.*
