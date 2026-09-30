# Chapter 24 — Atoms and Matter: Bound Electrons, Many-Body Atoms, Ionization Energies, Block-Spin Elements

*Chapter 24 of 25 in the Physics Notes monograph (`docs/monograph/00-plan.md`). Sourced from
`findings/F125-p5-hydrogen-atom-em-bound-state.md`, `findings/F148-modular-element-assembler.md`,
`findings/F156-realspace-em-bound-electron.md`, `findings/F157-manybody-nuclei-and-electron-clouds.md`,
`findings/F158-realspace-neutral-hydrogen-atom.md`, `findings/F159-u4-blockspin-multigrid-scale-separation.md`,
`findings/F160-live-two-grid-multigrid-atom.md`, `findings/F161-atomic-photon-emission.md`,
`findings/F195-blockspin-element-atom.md`, `findings/F208-relativistic-scf-ionization-energies.md`, and
`findings/F371-medium-z-relativistic-scf-ionization-energies.md` — the eleven findings `00-plan.md` §2
assigns to this chapter, all read in full. Checked directly against `docs/theory/supersessions.yaml`:
**zero hits** for all eleven finding numbers — none of them is named in any `superseded:` list of any of
the 23 records. Checked against `claims-index.md`: **CL111** (F125, `kind: prediction`, `status: live`,
`exactness: machine`, `falsifier: unset`), **CL131** (F148, `derivation`, `live`, `unset`, `unset`),
**CL139** (F156, `prediction`, `live`, `unset`, `unset`), **CL140** (F157, `derivation`, `live`, `unset`,
`unset`), **CL141** (F158, `derivation`, `live`, `unset`, `unset`), **CL142** (F159, `derivation`, `live`,
`unset`, `unset`), **CL143** (F161, `derivation`, `live`, `unset`, `unset`), **CL169** (F195,
`derivation`, `live`, `unset`, `unset`), **CL182** (F208 + F371, `derivation`, `live`, `unset`, `unset`).
F160 issues no claim card of its own — its own header states plainly "**Claim:** none — the live wiring
of F159's two-grid multigrid, whose physics is CL142's; the finding states its own case ('the channel is
wiring, not new physics')," consistent with D12's bar (an engine-capability wiring exercise, not a new
physics assertion). Notation, postulates and results are those of Chapters 1, 9, 14 and 23 —
$P=e^{i\theta}\mathbb I_2$, $\rho(\mathbf x)/\mathbf J(\mathbf x)$, $\alpha_\text{em}$ and the lepton
masses as free external inputs, the F262 bound-state machinery, R14.1–R14.21 (the confined baryon and the
model-native NN one-boson-exchange potential) — extended, never redefined; Chapter 23's own F262 treatment
(hydrogen/positronium/21 cm bound-state QED) is cited here, not re-derived.*

## 24.0 What this chapter establishes

Chapter 9 built the model's $U(1)_\text{EM}$ coupling; Chapter 14 built a genuine, confined, colour-singlet
nucleon and a model-native nucleon–nucleon force; Chapter 23 spent both of those, plus the measured
$\alpha_\text{em}$ and lepton masses, on a perturbative QED programme culminating in F262's bound-state
machinery (positronium, hyperfine splitting, 21 cm). This chapter asks the question none of those three
answer on its own: does the model produce a genuine, real-space, real-time bound electron cloud around a
nucleus — an actual atom, not a spectral eigenvalue problem — and does that construction scale from
hydrogen to a general element $(Z,N)$? The answer, built up in five stages across eleven findings: yes to
a single bound electron, both as a spectral Dirac–Coulomb solve (F125) and as a genuinely stationary
real-space cloud (F156/F158); yes to defeating the proton-to-orbit scale-separation wall with a two-grid
block-spin multigrid, first staged (F159) then run live inside one engine tick loop (F160); yes to a
modular element assembler that composes any $(Z,N)$ from the model's own confined nucleons and Coulomb
electrons with zero new parameters (F148), extended to genuinely multi-nucleon nuclei and multi-electron
Hartree clouds (F157) and then to a fully live, Pauli-antisymmetrized block-spin atom carried through
carbon (F195); and yes, with an honestly quantified and growing shortfall, to first ionization energies
across $Z=1$–$30$ (F208, F371) — where the dominant, correctly-diagnosed error is the *absence of
exchange* in the Hartree mean field, not relativity, which the model's own Dirac–Coulomb operator (F125)
shows to be negligible at the valence level through zinc. F161 closes the chapter with the atom's first
dynamical process: spontaneous photon emission, with line positions and Einstein-$A$ rates derived, not
assumed, from the same bound states.

## 24.1 Inputs

**Postulates used.** No new postulates. **P4** (exact unitarity) underwrites every norm-conservation and
charge-conservation claim in this chapter — the split-step electron propagator's unitarity to the FFT
floor (F156, F195), the block-spin charge-transfer identity (F159), and the two-grid engine's per-tick
norm conservation (F160) are all direct consequences of it, the same way it underwrote Chapter 14's
coarse-graining programme (Group D, R14.17–R14.20) this chapter's multigrid machinery reuses. **P5** (the
massless Weyl-spinor primitive) and **P6** (the chiral $SU(2)$ mass mechanism) are the fields every
constituent quark, gluon and electron in this chapter's atoms descends from, exactly as Chapter 14 already
inherited them (§14.1) — this chapter adds no new field content, only a new *composition*.

**Prior results used, precisely.** **R9.1–R9.9** (Ch.9) — the identity-channel U(1) Peierls coupling and
the paired photon it attaches to — is the electromagnetic binding channel every result in this chapter
uses; this chapter does not revisit the coupling's *form*, only its consequences for a genuine two-body
(and many-body) bound state. **R14.1–R14.6** (Ch.14, Group A) — the confined, colour-singlet, non-
dispersing proton (F71, F122, F136) — is the nucleus every atom in this chapter binds an electron cloud
to; **R14.9–R14.16** (Ch.14, Group C) — the model-native one-boson-exchange NN potential (pion tensor,
$\sigma$, $\omega$, the quark-Pauli core) — is the inter-nucleon force this chapter's multi-nucleon
solvers (F157) reuse without re-deriving; **R14.17–R14.20** (Ch.14, Group D) — the proof that block-spin
coarse-graining commutes with binding, and that mass is the matter sector's RG-relevant operator — is the
direct methodological precedent this chapter's own multigrid programme (F159/F160/F195) extends from a
single bound state to the full proton-orbit scale separation. **Chapter 23's F262 bound-state machinery**
(positronium, hyperfine splitting, hydrogen 21 cm — `23-qed-precision.md` §23.2.7) is cited directly, per
this chapter's own instruction, rather than re-derived: F125's own hydrogen Coulomb/Dirac solver is the
object F262 reuses "at reduced mass" for positronium, and this chapter's ionization-energy work (F208,
F371) is a distinct extension of the *same* F125 radial solver into the multi-electron SCF, not a
duplicate bound-state construction. **F370's two-class Lamb-shift residual** (Ch.23 §23.7) — Class 1
(vacuum polarization/Källén–Sabry, tractable but unclosed) and Class 2 (two-loop self-energy, larger and
structurally harder) — is not itself consumed by any construction in this chapter (this chapter's fine
structure is the tree-level Dirac–Coulomb splitting, F125, not the radiative correction), but is recorded
here as the standing precedent for how this chapter's own §24.6/§24.7 discloses a quantified, unclosed
residual (the Hartree/no-exchange underbinding) rather than describing it vaguely.

**Free inputs consumed.** **The electron mass $m_e$ and the electromagnetic coupling $\alpha_\text{em}$**
are consumed throughout this chapter exactly as Chapters 9 and 23 already disclosed they must be: read in
from measurement (the F120/F121 anchors), not derived from the lattice rule. F125's own accounting is
explicit that $\alpha$ is "the one empirical EM number" and everything downstream of it and $m_e$ is a
prediction. **The proton mass $m_p$** enters only as the $0.05\%$ reduced-mass correction to the hydrogen
Rydberg (F125 §6); the *absolute* baryon mass in MeV is Chapter 14's own honestly disclosed open item
(overshooting the physical $m_p/\sqrt\sigma$ ratio by $2.3$–$3.6\times$, §14.9), inherited here rather than
re-litigated — every result in this chapter that needs an absolute baryon mass (the He-4/A-body binding
energies of F157) is scoped, as Chapter 14 scopes its own analogous results, to structure and to string-
tension units, not to a chapter-original absolute-MeV claim. **Nothing else is free in the sense of an
unexplained fitted constant**: the Hartree self-consistent field (F157, F195, F208, F371) introduces no
tunable screening constant — screening is computed live from the actual electron density — and the
block-spin factor $b$ that carries the proton-to-orbit scale ratio (F159, F160, F195) is a *representation
choice* (how much of the true $\sim10^4$–$10^5$ scale separation to represent on a tractable lattice), not
a fitted physical parameter.

## 24.2 The derivation

### 24.2.1 The single bound electron, spectrally: Rydberg series and Dirac fine structure (F125)

The first and structurally simplest object this chapter builds is the spectral (not yet real-space)
hydrogen atom: an electron (Chapter 11's dynamical field) bound to a proton by the Chapter 9 electromagnetic
channel's long-range $-Z\alpha\hbar c/r$ Coulomb tail. The reduced radial Schrödinger problem, solved as a
real symmetric tridiagonal eigenproblem (the direct $1/r$ generalization of the model's own two-body
contact solver, F74), reproduces the exact Coulomb spectrum:

$$\boxed{\;E_n[\mathrm{Ry}]=-\frac1{n^2}\ \text{to the grid floor (worst deviation }1.6\times10^{-4}\text{ at the }1s\text{ cusp); exact }\ell\text{-degeneracy (accidental }SO(4)\text{) to}\lesssim10^{-5}\text{ Ry; node count exactly }n-\ell-1\;}\tag{R24.1}$$

(F125, checks A–E.) The absolute energy scale is not an additional input: the physical Rydberg
$\mathrm{Ry}=\tfrac12\mu c^2(Z\alpha)^2$, built from the model's own electron-mass anchor and
$\alpha_\text{em}$, gives $\mathrm{Ry}(\mathrm H)=13.598287$ eV — matching the reduced-mass CODATA value to
$1.1\times10^{-12}$ — with no further input. The two-body $\to$ relative-coordinate reduction is
independently certified by positronium, which collapses onto the *same* solver at $\mu=m_e/2$ and gives
$\mathrm{Ry}(\mathrm{Ps})/\mathrm{Ry}(\mathrm H_\infty)=0.5$ to $10^{-9}$ — the identical structural result
Chapter 23 (F262) cites and reuses for its own hyperfine and lifetime calculations, not re-derived a second
time here.

The relativistic fine structure is a genuine prediction of the Dirac kinetic operator, not fit to it: the
closed-form Sommerfeld spectrum matches its own $O((Z\alpha)^4)$ expansion to $5\times10^{-10}$, and is
independently reproduced by a hand-rolled numerical radial-Dirac integrator (RK4, Wronskian matching) to
$\le1.3\times10^{-6}$ relative to the binding — so the splitting is a genuine solve, not only a closed
form.

$$\boxed{\;2p_{3/2}-2p_{1/2}\text{ splitting}=45.28\ \mu\text{eV}=10.95\text{ GHz vs measured}\approx10.969\text{ GHz}(0.18\%);\ \alpha^4/\alpha^2\text{ scaling exact (slopes }4.0001/2.0000\text{); }2s_{1/2}=2p_{1/2}\text{ exactly degenerate in pure Dirac-Coulomb (to }10^{-14}\text{)}\;}\tag{R24.2}$$

(F125, checks F–I; `CL111`, `status: live`, `exactness: machine`.) The $2s$–$2p$ Lamb shift itself is
explicitly **not** a one-body Dirac effect — it is the radiative QED correction Chapter 23 computes in
full (F252/F257/F370); this chapter's Dirac–Coulomb solve reproduces the correct *degeneracy* the Lamb
shift then lifts, and this chapter does not re-derive that lift. With F125, the model's matter-binding
roadmap (P0 electron/quarks through P6 SI scale) is complete in the spectral sense: one electron carried
through to a hydrogen atom with the right ground-state energy, spectrum, and relativistic fine structure,
from a single EM coupling and two measured numbers ($m_e$, $\alpha$).

### 24.2.2 The real-space, real-time stationary bound electron — and why it succeeds where F134's Dirac probe did not (F156)

F125 is a spectral eigenvalue solve; the next question, genuinely new to this chapter's programme, is
whether the model produces a bound electron **as a real-space, real-time lattice object** — the actual
deliverable a cellular-automaton "universe in a bottle" is supposed to supply, not a basis-function
diagonalization. Chapter 14's own real-space unification run (F134, U0/U2) had already probed exactly this
question with the model's relativistic Dirac electron in a *vector* Coulomb well, and found the Coulomb
loop genuinely responsive — pulling the electron below its free-control separation — but **not yet a
stationary orbit**: at the compressed, non-scale-separated lattice available, the result was a scattering
quasi-orbit, with a physically-scaled stationary cloud named as future work (Chapter 14 §14.9, its own
forward flag to "the model's own U4 multigrid programme").

**F156 is exactly that future work, and it resolves the gap by a change of dynamical description, not by
brute-force scale separation.** Its own text is explicit about why: an atomic electron is genuinely
non-relativistic ($v\sim\alpha c\sim0.007c$), and a *relativistic* Dirac electron in a vector Coulomb well
on a tractable lattice does not give a clean stationary state at all — it Klein-tunnels, the $Z\alpha\to1$
Dirac–Coulomb collapse regime that F134's own probe and a companion finding (the vector-confinement null)
had already flagged. F156 diagnoses two specific failure modes of the vector-coupling route directly
before abandoning it: the static Wilson increment applied via wrap/unwrap is *pure gauge* (zero field
strength, no force on the density — the centroid does not move under it), while the accumulating-wrap
construction that *does* produce a real force over-accelerates a relativistic Dirac packet at lattice
coupling rather than settling it into an orbit. **Replacing the relativistic vector-Coulomb construction
with the correct non-relativistic Schrödinger orbital — itself an exactly-unitary split-step
$e^{-iV\,dt/2}\cdot\mathcal F^{-1}e^{-ik^2dt/2m}\mathcal F\cdot e^{-iV\,dt/2}$ — produces a genuinely
stationary bound cloud:**

$$\boxed{\;\text{RMS radius flat }2.45\to2.51\text{ over 400 ticks (spread}<0.5\%\text{) vs the matched free control's ballistic }2.45\to18.3\text{; norm conserved to}\sim10^{-14}\text{; correct attractive sign (}q=-1\text{ on a }+1\text{ source)}\;}\tag{R24.3}$$

(F156, 4/4 checks PASS; `CL139`, `status: live`.) This is not a retreat from the relativistic problem —
F125's own spectral Dirac–Coulomb solve already supplies the fine structure (R24.2) that a non-relativistic
real-space run cannot — it is the recognition, stated directly in the finding, that binding demonstration
and relativistic fine structure are two different questions answered by two different constructions, and
that a cellular automaton demonstrates the *former* well precisely because it is not forced through the
relativistic vector-coupling route F134's own real-time probe correctly identified as unstable for this
purpose. **F134's own forward flag is therefore not an unresolved gap this chapter inherits — it is closed
here**, by the non-relativistic-orbital construction F156 supplies, twelve days after F134.

### 24.2.3 Neutral hydrogen as one co-evolving real-space object (F158)

With a stationary bound electron (F156) and a confined, charged, colour-triplet proton already available
from Chapter 14 (R14.5, F136 — the same Lorentz-scalar Y-string confinement mechanism Chapter 13a derives
from the Klein paradox, R13a.14), F158 puts both on **one** BCC lattice and lets them co-evolve as a single
neutral atom:

$$\boxed{\;\text{net EM charge}=0\text{ exactly throughout (}<10^{-12}\text{); all four coupling loops live (colour, gluon, EM current, photon)}\;;\text{ proton confined (cluster RMS plateaus}\approx3.3\text{ vs the free control's monotonic dispersal); electron bound (cloud RMS}\approx4.0\text{–}4.4\text{, larger than the proton — the correct atomic ordering); electron tracks the proton (centroid separation}\ll\text{cloud radius); every channel norm conserved to}\sim10^{-13}\;}\tag{R24.4}$$

(F158, 6/6 checks PASS; `CL141`, `status: live`.) This is, per the finding's own framing, the first
composite-neutral atom exhibited as a single co-evolving real-space lattice object — the electron cloud
correctly surrounds and is larger than the confined nucleus, at the compressed scale the single-lattice
construction requires. The one honestly disclosed limitation, carried forward explicitly rather than
smoothed over, is scale: the physical proton-to-orbit size ratio is $\sim10^4$, and F158's own single
lattice cannot represent that ratio without either failing to resolve the proton or exceeding a tractable
box — restoring the true ratio is named as the next finding's job (U4, the two-grid multigrid).

### 24.2.4 The block-spin two-grid multigrid, staged (F159)

The proton is $\sim1$ fm; the Bohr orbit is $\sim5.3\times10^4$ fm, a $\sim6.3\times10^4$-fold size ratio no
single literal lattice resolves (a grid fine enough for the proton and wide enough for the orbit would need
$\gtrsim10^{12}$ cells). F159 defeats this wall the same way Chapter 14's own coarse-graining programme
(Group D) proved binding survives block-spinning: run the proton on its own fine patch, and let it enter
the atomic-scale coarse lattice as a block-spin ($R_b$) coarse-grained **point charge**, with the block
factor $b$ carrying the entire scale separation. Two facts license this, each verified directly rather than
assumed:

$$\boxed{\;R_b\text{ is charge-faithful: block-averaging the proton's charge over }b^3\text{ fine cells conserves total charge exactly (1.000000) and concentrates it to a point as }b\text{ grows}\;}\tag{R24.5}$$

$$\boxed{\;R_b\text{ commutes with the orbit binding: the point-vs-resolved binding-energy gap}\to0\text{ as }a_0/r_p\text{ grows (sandbox: }0.053\to0.010\text{); the ground state is invariant under the coarse spacing }a_c=b\cdot a_f\text{ (}E_0\text{ rel-spread }0.0027\text{ over }b=1,2,3\text{)}\;}\tag{R24.6}$$

(F159, 4/4 checks PASS; `CL142`, `status: live`.) The orchestrated two-grid atom reaches $b=63{,}000$,
representing a proton-to-orbit ratio of $4.28\times10^4$ ($4.63$ decades) — essentially physical hydrogen's
$6.3\times10^4$ — on two tractable lattices, with charge conserved exactly and the electron bound. This is
staged, per the finding's own scoping: an orchestrated fine$\to R_b\to$coarse computation, not yet a single
live engine run with the coupling applied every tick — that hand-off is F160's.

### 24.2.5 The live two-grid engine run — one `Simulation.run()` (F160)

F160 wires F159's staged construction into a single CASIM channel (`two_grid_atom`) that co-evolves both
grids inside one `Simulation.run()`: every tick, the fine proton patch (three colour Dirac quarks confined
by the F136 scalar Y-string) is stepped, block-spin-reduced to a point source on the coarse grid, and the
coarse electron orbital (F156's split-step) is stepped in that well.

$$\boxed{\;\text{net EM charge}=0\text{ throughout; norms conserved to}\sim3\times10^{-14}\text{ on both sub-evolutions; electron orbit stable (RMS}\approx6.2\text{ cells, flat); proton confined (RMS}\approx2.6\to3.3\text{, bounded); represented }a_0/r_p\approx6\times10^4\text{ (}\approx4.8\text{ decades) — physical hydrogen's ratio, produced }live\text{, in one run}\;}\tag{R24.7}$$

(F160, 5/5 checks PASS; issues no claim card of its own, per D12's scope bar — "the channel is wiring, not
new physics," its physics resting on `CL142`/F159.) The engine-level generalization this sidesteps — a
genuine per-channel multi-lattice framework with an explicit $R_b$ coupling operator, rather than one
channel privately owning two sub-grids — is named as future engineering, not a physics gap: the audited
kernels (the F136 proton, the F156 electron) are reused verbatim, so the physics is identical to F159's
staged result, only now genuinely dynamical in one run.

### 24.2.6 The modular element assembler: any element as NUCLEUS(Z,N) + ELECTRON CLOUD(Z) (F148)

Parallel to the real-space programme (§24.2.2–24.2.5), F148 builds the **composition layer**: a single
entry point $\text{atom}(Z,N)=\text{NUCLEUS}(Z\text{ protons}+N\text{ neutrons})+\text{ELECTRON
CLOUD}(Z\,e^-)$ that assembles any element from the model's already-published constituents — the confined
baryon (Chapter 14, F122), the model-native NN one-boson exchange (Chapter 14, F104/F113/F126/F128), and
the F125 Coulomb/Dirac electron solver — introducing **zero new fitted parameters**: every constant the
assembler uses is imported bit-identically from an already-published module (checked directly, not
asserted).

$$\boxed{\;\text{Hydrogen assembles as a stable, neutral atom from imported constituents alone: proton bound (}29.1\%\text{ constituent-mass fraction, the "mass is the string" signature), electron bound at }-13.598\text{ eV (reconstructed to }2.5\times10^{-5}\text{ from imported }m_e,m_p,\alpha\text{), ionization energy}=+13.598\text{ eV vs measured (rel. }3.6\times10^{-5}\text{); exact integer neutrality}\;}\tag{R24.8}$$

(F148, 13/13 checks PASS; `CL131`, `status: live`.) The framework composes any $(Z,N)$ at the
*instantiation* level — correct mass number and exact neutrality verified across H through U, correct
Aufbau noble-gas shell closures (He $1s^2$, Ne $2p^6$, Ar $3p^6$) — while the heavier $A\ge3$ nuclear-binding
and $Z\ge2$ electronic-SCF paths are deliberately wired as honest extension hooks that raise rather than
return an unverified number, so the finding never claims more than it has actually solved. Those two hooks
are exactly what F157 (§24.2.7) and F195 (§24.2.8) complete.

### 24.2.7 Multi-nucleon nuclei and multi-electron clouds (F157)

F157 lifts F148's two extension hooks from "wired" to "computing," strictly from the model's own building
blocks, no fitted semi-empirical (liquid-drop) coefficients.

**Multi-electron — Hartree self-consistent field.** Each occupied subshell is solved in the field of the
nucleus plus all *other* electrons, iterated to self-consistency; screening is computed live from the
actual electron density, not tabulated, with only $m_e$ and $\alpha$ entering.

$$\boxed{\;\text{Helium Koopmans ionization}=24.0\text{ eV vs CODATA }24.59\text{ eV; total}=-76.5\text{ eV (the Hartree limit); generalizes by Aufbau to Li, C (bound, ionizable valence)}\;}\tag{R24.9}$$

**Multi-nucleon — $A$-body variational cluster.** A translationally-invariant single-width Gaussian fed
the model NN interaction, with an effective $S{=}1,T{=}0$ attraction depth fixed **only** by reproducing
the model's own $A=2$ deuteron binding (pionless-EFT style, no experimental nucleus used as an external
anchor):

$$\boxed{\;\text{alpha particle (}A{=}4\text{) binds at}-30.1\text{ MeV (exp}-28.3\text{, within }6\%\text{); }A{=}3\text{ binds at}-12\text{ MeV; central OBE alone does }\textit{not}\text{ bind (verified positive}\langle V\rangle\text{ for }A{=}2\text{–}16\text{), faithfully reflecting that the model's own deuteron binds only via the pion tensor force (Ch.14, R14.9)}\;}\tag{R24.10}$$

(F157, 5/5 checks PASS; `CL140`, `status: live`.) The assembler now composes a full neutral, stable
multi-nucleon/multi-electron atom (He-4) end to end: nucleus bound ($-30.1$ MeV), electron cloud bound
($-76.5$ eV, IP $24.0$ eV), net charge $0$. The disclosed frontier — heavier $A$ overbinds because
spin-isospin/Pauli saturation is not yet enforced in the variational cluster — is carried into §24.6/§24.7
rather than hidden.

### 24.2.8 A fully live, Pauli-antisymmetrized block-spin atom for a general element (F195)

F195 generalizes F160's live two-grid hydrogen channel to a general element $(Z,N)$, adding exactly the
piece F148/F157 flagged as the genuinely new engineering: **Pauli antisymmetry among live electron
orbitals.** The fine patch now holds $A=Z+N$ nucleon charge blobs summing to exactly $+Z$, block-spin-reduced
to a single coarse point source (Tier A — the physically correct statement for the electron sector; Tier B
runs live confined quarks, smoke-certified on He); the coarse grid holds $Z$ distinct spatial orbitals
filled by Aufbau with Hund's rule, each an exactly-unitary F156 split-step packet evolving in the
self-consistent mean field of the nucleus plus the live Hartree repulsion of every *other* orbital, with
Pauli antisymmetry enforced by live Gram–Schmidt orthonormalization every tick.

$$\boxed{\;\text{Certified on H, He, Li, C (}\ge300\text{-tick runs): net charge}\equiv0\text{ to machine precision; norms conserved to}\sim10^{-15}\text{; Pauli orthogonality to}\sim10^{-15}\text{; every orbital radius bounded (bound-vs-free ratio }2.3\text{–}5.6\times\text{); cloud surrounds and tracks the nucleus; represented }a_0/r_\text{nuc}\approx4.5\text{–}5.1\text{ decades}\;}\tag{R24.11}$$

(F195, 9/9 checks PASS; `CL169`, `status: live`.) Tier B (He, 12 live confined quarks) is smoke-certified:
exact neutrality and norm conservation, the nucleus genuinely colour-loop-live, and — per the companion
Chapter 14 finding F206, cited here rather than re-derived — the initially-observed $\sim50\%$ nuclear
"breathing" is intra-nucleon (single-nucleon Y-string softening), not a failure of the inter-nucleon OBE
binding, which F206 separately certifies as bounded and core-limited. The live configurations reproduce
F157's own spectral structure (He closed-shell $1s^2$, Li opening $2s^1$, C's Hund-filled $2p^2$) as
*structure*, not a re-derivation of the absolute eV/MeV, which remain the F125/F157 spectral numbers.

### 24.2.9 Relativistic ionization energies in the multi-electron SCF, and where the accuracy actually breaks (F208)

With a working Hartree SCF (F157) and the F125 Dirac–Coulomb operator both in hand, F208 wires the scalar
(spin-averaged) Dirac–Coulomb $O((Z\alpha)^4)$ shift into the SCF per orbital, at the orbital's own screened
effective charge, and sweeps first ionization energies $Z=1$–$20$ against CRC/NIST to map, quantitatively,
where the construction's accuracy breaks down.

$$\Delta E_{n\ell}=-\frac{Z_\text{eff}^4\alpha^2}{2n^4}\Big(C(n,\ell)-\tfrac34\Big),\qquad C(n,0)=n,\ \ C(n,\ell\ge1)=\frac{n}{\ell+\tfrac12}$$

reproducing the F125 hydrogen $1s$ shift exactly ($-\alpha^2/8\ \text{Ha}=-0.181$ meV). The result is
unambiguous:

$$\boxed{\;\text{the valence relativistic shift never exceeds }0.6\text{ meV through Ca — four orders of magnitude below the eV-scale SCF error — while the SCF (Hartree, no exchange) underbinds the ionization energy by}-15\%\text{ to}-40\%\text{ from lithium onward (mean }27.7\%\text{, }Z=2\text{–}20\text{); the error is systematically negative (Hartree omits exchange self-interaction; Koopmans omits orbital relaxation), and relativity is }\textit{not}\text{ the light-element accuracy ceiling}\;}\tag{R24.12}$$

(F208, 7/7 checks PASS; `CL182`, `status: live`.) What *does* grow with $Z$ is the relativistic shift on
the deep $1s$ **core**, climbing from $-0.6$ eV (Ne) to $-5.7$ eV (Ca) — a $\sim Z^4$ fine-structure law
(log–log slope $3.38$) confirming the relativistic machinery is live and correct, just acting on a shell
that is not the valence electron this chapter's ionization comparison targets.

### 24.2.10 Extending the map to the full 3d series, and an honestly disclosed numerical caveat (F371)

F371 runs the **unmodified** F208/F157 machinery over Sc–Zn ($Z=21$–$30$), including the specifically
requested Fe ($Z=26$), against NIST first ionization energies.

$$\boxed{\;\text{every element Sc–Zn is underbound by }33\%\text{–}48\%\text{, still dominated by missing exchange (never relativity: valence shift }0.22\text{–}0.38\text{ meV through Zn, four orders of magnitude below the SCF error); Fe: model }4.669\text{ eV vs NIST }7.9024\pm0.0010\text{ eV (}-40.9\%\text{)}\;}\tag{R24.13}$$

(F371, mean $|{\rm err}|$ over $Z=21$–$30$: $38.2\%$; combined $Z=2$–$30$ mean: $31.3\%$; rolls into
`CL182` alongside F208 per D12's narrowed-not-rewritten convention.) F371 also discloses, rather than
hides, a second and genuinely new limitation found while doing this carefully: the default SCF mixing
(`mix=0.4, max_iter=60`) silently fails to converge from Ni ($Z=28$) onward, with the unconverged Zn
Koopmans IE ($7.37$ eV) wrong by $52\%$ against the properly converged answer ($4.85$ eV) — fixed by
tighter mixing, verified identical to the default on $Z=21$–$27$ where both converge. More fundamentally,
the fixed-$N{=}900$ uniform radial grid F208 used throughout is shown **not to be grid-converged above
roughly $Z\sim20$**: a spot check at $N=1200$ shifts the Fe valence IE by $+10.8\%$ and its $1s$ core
relativistic shift by $+65.9\%$; at Zn the shifts are $+12.6\%$ and $+81.4\%$ — a numerical uncertainty that
grows monotonically with $Z$ and, by Fe/Zn, rivals the physical exchange-correlation error in magnitude.
The qualitative conclusion (dominant exchange error, negligible valence relativity) is unchanged at
$N=1200$; the *precise* error percentages in the Z=21–30 table should be read as $N=900$-grid values with
a real, unclosed numerical uncertainty layered on top, disclosed as a named follow-on (a non-uniform radial
grid or Richardson extrapolation), not smoothed into the headline number.

### 24.2.11 The atom's first dynamical process: spontaneous photon emission (F161)

Closing the chapter, F161 turns F125's static levels into a rate and a spectrum: an excited electron drops
to a lower level and radiates a photon, computed from the model's own constants ($m_e$, $\alpha$) with no
new inputs.

$$\boxed{\;\text{Lyman-}\alpha=121.50\text{ nm (data }121.567\text{); Balmer series }656.1/486.0/433.9/410.1\text{ nm (data }656.3/486.1/434.0/410.2\text{); Einstein }A(2p\to1s)=6.27\times10^8\text{ s}^{-1},\ \tau=1.59\text{ ns (data }6.27\times10^8,\ 1.6\text{ ns); }2s\to1s\text{ and }3d\to1s\text{ dipole-forbidden (}A=0\text{, the correct selection rule)}\;}\tag{R24.14}$$

(F161, 4/4 checks PASS; `CL143`, `status: live`.) Line frequencies are exact given the F125 level formula;
the Einstein-$A$ rates inherit the F125 radial-wavefunction accuracy and match measurement to a few
percent. This is the first member of a dynamical-processes layer (emission $\to$ scattering $\to$
transport) this chapter opens but does not complete; §24.7 states what remains.

## 24.3 Results table

| # | Statement | Exactness | Source |
|---|---|---|---|
| R24.1 | Hydrogen spectral bound state: $-1/n^2$ series to grid floor, exact Coulomb $\ell$-degeneracy, correct node count | exact structure / grid-floor numerics | F125; `CL111` |
| R24.2 | Absolute Rydberg from $m_e,\alpha$ to $1.1\times10^{-12}$; Dirac fine structure ($2p_{3/2}$–$2p_{1/2}=10.95$ GHz, $0.18\%$); $2s_{1/2}{=}2p_{1/2}$ degeneracy machine-exact | exact algebra / quantitative | F125; `CL111` |
| R24.3 | Real-space, real-time stationary bound electron cloud (RMS flat over 400 ticks vs ballistic free control); resolves F134's own "not yet a stationary orbit" flag via the non-relativistic-orbital construction | Tier-3 (statistical) / machine (norm) | F156; `CL139` |
| R24.4 | Neutral hydrogen as one co-evolving real-space object on a single lattice: exact neutrality, bounded proton and electron, correct cloud-surrounds-nucleus ordering | machine (charge/norm) / Tier-3 (radii) | F158; `CL141` |
| R24.5/R24.6 | Block-spin two-grid multigrid, staged: $R_b$ exactly charge-faithful; commutes with orbit binding; $b=63{,}000$ represents the true $\sim6.3\times10^4$ scale ratio | exact (charge) / Tier-3 (binding invariance) | F159; `CL142` |
| R24.7 | Live two-grid engine run, one `Simulation.run()`: exact neutrality, norms conserved to $3\times10^{-14}$, represented ratio $\approx6\times10^4$ | machine / Tier-3 | F160 (no own claim card, physics = `CL142`) |
| R24.8 | Modular element assembler: hydrogen stable end-to-end, zero new parameters, ionization energy to $3.6\times10^{-5}$ | exact (neutrality) / quantitative | F148; `CL131` |
| R24.9/R24.10 | Multi-electron Hartree SCF (He IP $24.0$ eV vs $24.59$); multi-nucleon $A$-body cluster (He-4 $-30.1$ MeV vs $-28.3$, within $6\%$) | quantitative (Tier-3 variational) | F157; `CL140` |
| R24.11 | Fully live, Pauli-antisymmetrized block-spin atom, H/He/Li/C: exact neutrality/norm/orthogonality, bounded radii, represented scale $4.5$–$5.1$ decades | machine (charge/norm/orthogonality) / Tier-3 (radii) | F195; `CL169` |
| R24.12 | Relativistic SCF ionization energies $Z{=}1$–$20$: valence relativistic shift $<0.6$ meV through Ca; Hartree/no-exchange underbinding $15$–$40\%$ (mean $27.7\%$) | exact (shift formula) / quantitative (comparison) | F208; `CL182` |
| R24.13 | Extension to $Z{=}21$–$30$ (3d series): underbinding $33$–$48\%$ (mean $38.2\%$), valence relativity still sub-meV; grid-convergence caveat disclosed and quantified | quantitative, with disclosed unclosed numerical uncertainty | F371; `CL182` |
| R24.14 | Spontaneous photon emission: Lyman/Balmer lines to $<1\%$, Einstein-$A$ rates to a few percent, correct dipole selection rules | exact (frequencies, given levels) / quantitative (rates) | F161; `CL143` |

## 24.4 Comparison with measurement

**Rydberg series and fine structure.** $\mathrm{Ry}(\mathrm H)=13.598287$ eV vs the reduced-mass CODATA
value, agreement $1.1\times10^{-12}$; the $2p_{3/2}$–$2p_{1/2}$ splitting at $10.95$ GHz vs measured
$\approx10.969$ GHz ($0.18\%$), with the defining $\alpha^4$ (absolute) and $\alpha^2$ (relative) scaling
laws reproduced to four decimal places in the fitted slope. Positronium's exact half-Rydberg ratio
($0.5000000000$ to $10^{-9}$) is Chapter 23's own reused precedent (F262), not re-verified here.

**Atomic spectral lines and lifetimes.** Lyman-$\alpha$ at $121.50$ nm vs measured $121.567$ nm; the
Balmer visible series at $656.1/486.0/433.9/410.1$ nm vs measured $656.3/486.1/434.0/410.2$ nm — sub-percent
across the board. The $2p\to1s$ Einstein-$A$ coefficient, $6.27\times10^8$ s$^{-1}$ ($\tau=1.59$ ns), matches
the measured rate and lifetime to three significant figures; the $2s\to1s$ and $3d\to1s$ dipole-forbidden
transitions correctly vanish exactly.

**Ionization energies, $Z=1$–$30$.** Hydrogen is exact ($3.6\times10^{-5}$ relative error) and helium is
good ($-2.5\%$); every element from lithium onward underbinds, with the error rising through the light
elements (Li $-14.5\%$, C $-29.2\%$, Ar $-36.1\%$, Ca $-35.7\%$) and persisting through the entire first
transition-metal row (Sc $-35.9\%$ through the requested Fe at $-40.9\%$, worst-case Zn at $-48.3\%$). Mean
$|{\rm err}|$ is $27.7\%$ over $Z=2$–$20$ (F208) and $38.2\%$ over $Z=21$–$30$ (F371), combined $Z=2$–$30$
mean $31.3\%$. The valence relativistic correction, by contrast, never exceeds $0.6$ meV through calcium
and stays at $0.22$–$0.38$ meV through zinc — three to four orders of magnitude below the SCF error at
every $Z$ checked. **The comparison-with-measurement headline of this chapter's ionization-energy work is
therefore not "the model reproduces ionization energies" — it is "the model correctly diagnoses which
missing physics (exchange, not relativity) is responsible for the $15$–$48\%$ shortfall it honestly
reports," a different and more precisely falsifiable claim.**

## 24.5 What was excluded, and why

**A relativistic vector-Coulomb construction for the real-space bound electron.** Excluded directly by
F134's own real-time measurement and F156's own diagnosis (§24.2.2): a Dirac electron in a vector Coulomb
well on a tractable lattice Klein-tunnels rather than settling into a stationary orbit, and the two specific
mechanisms tried (a static Wilson increment, which is pure gauge and exerts no force; an accumulating wrap,
which over-accelerates) were each tested and found unsuitable before the non-relativistic Schrödinger
orbital was adopted instead. This is not a retreat from relativistic content — F125's spectral Dirac–Coulomb
solve supplies the fine structure a real-space non-relativistic run cannot — it is a considered choice of
the right tool for the binding-demonstration question specifically.

**The Hartree/no-exchange approximation, as a route to chemically accurate ionization energies.** F208 and
F371 are unambiguous, and this chapter reports the exclusion as plainly as they do: Hartree-plus-Koopmans
systematically underbinds every many-electron ionization energy by $15$–$48\%$ across the entire range
checked, because the mean field omits the exchange self-interaction correction and Koopmans omits orbital
relaxation on ionization — both push the ionization energy down, exactly as observed. A self-consistent
Dirac–Fock treatment is explicitly *not* the fix for this range (F208's own conclusion): it would only
matter for heavy/superheavy valence chemistry, where the valence relativistic shift finally grows large
enough to compete with the exchange error.

**Strict per-nucleon Cornell/absolute-MeV baryon-mass predictions, as inputs to this chapter's nuclear
binding-energy numbers.** Chapter 14's own disclosed $2.3$–$3.6\times$ overshoot on the absolute baryon
mass (§14.9) is inherited, not re-litigated: F157's He-4 binding energy ($-30.1$ MeV vs $-28.3$ MeV
measured) is reported as a genuine, close prediction of the *interaction* energy on top of an already-bound
nucleon, not as evidence that the absolute nuclear mass scale is independently closed.

**Heavy $A$ nuclear saturation and open $d$/$f$-shell live block-spin atoms beyond carbon.** F157's own
disclosed frontier — heavy $A$ overbinds in the variational cluster because spin-isospin/Pauli saturation
is not yet enforced — and F195's own disclosed frontier — $d$/$f$ angular seeds beyond carbon are wired but
not certified in the live block-spin channel — are both carried into §24.7 rather than treated as closed.

## 24.6 What is still open

- **The Hartree/no-exchange ionization-energy underbinding, quantified and growing.** F208 establishes
  $15$–$40\%$ underbinding for $Z=2$–$20$; F371 extends this to $33$–$48\%$ for $Z=21$–$30$, confirming the
  same missing-exchange diagnosis with no relativistic contribution (valence shift $<0.4$ meV throughout).
  The named remedy — Hartree–Fock exchange, plus an orbital-relaxation ($\Delta$SCF) or correlation term —
  is explicitly the next required step, not attempted in either finding.
- **A second, independently disclosed limitation: the fixed-$N{=}900$ radial grid is not grid-converged
  above $Z\sim20$.** F371's own $N=1200$ spot check shows a $+10.8\%$ shift on the Fe valence IE and
  $+65.9\%$ on its $1s$ core relativistic shift, with the sensitivity growing monotonically with $Z$ and, by
  Fe/Zn, rivaling the physical exchange-correlation error in magnitude. This means F208's own Z=18–20
  endpoint also carries an undisclosed-until-F371 numerical uncertainty (Ca: $+6.9\%$ valence,
  $+41.2\%$ core at $N=1200$ vs $N=900$), smaller than at Fe/Zn but non-negligible. No attempt to reach
  genuine grid convergence (a non-uniform/log radial grid, or Richardson extrapolation) has been made; F371
  names this explicitly as follow-on work on the same footing as the exchange-correlation gap itself.
- **A numerical, resolved oddity in the SCF configuration search.** F371 finds strict Madelung filling
  gives the wrong ground configuration for Cr and Cu specifically (`4s^2 3d^4`/`4s^2 3d^9` instead of the
  real `4s^1 3d^5`/`4s^1 3d^{10}`) — the same missing-exchange limitation surfacing in the configuration
  itself, not only its energy, for exactly the two elements where real-world exchange stabilization of
  half-filled/filled $d$-subshells is strongest.
- **Heavy-$A$ nuclear saturation in the variational $A$-body cluster (F157)** and **$d$/$f$-shell coverage
  in the live block-spin atom beyond carbon (F195)** are both named frontiers, not closed constructions.
- **The engine-level generalization of the two-grid multigrid** — a genuine per-channel multi-lattice
  framework with an explicit $R_b$ coupling operator, rather than one channel privately owning both
  sub-grids (F160's own scoping) — remains future engineering, though the physics it would generalize is
  already proven identical.
- **A genuinely gluon-self-sourced (rather than mean-field geometric) confining string for the live
  colour-triplet proton** this chapter's Tier-B constructions (F195) build on is Chapter 14's own disclosed
  open item (§14.9), inherited here without independent progress.

> **Gap [G-13]:** `findings/F148-modular-element-assembler.md` (2026-06-12, built after F104/F113/F126/F128,
> all of which independently tune the deuteron to the physical $E_b=2.224$ MeV — Chapter 14's own headline
> figure, R14.9–R14.12) reports its own `solve_deuteron()` call returning $E_b=2.234$ MeV (check G4). Five
> days later, `findings/F157-manybody-nuclei-and-electron-clouds.md` reuses the same function and reports
> the identical $2.234$ MeV, anchoring its own $A$-body cluster's effective $S{=}1,T{=}0$ depth to it. Both
> numbers are internally consistent with each other, but neither finding notes, or reconciles, the $0.45\%$
> discrepancy against the $2.224$ MeV value every one of F104/F113/F126/F128 (and Chapter 14's own §14.4
> account, built entirely from those four findings) reports as the deuteron's tuned, physical value. No
> source read for this chapter states which configuration (core radius, quark size $b$, or $\sigma$/$\omega$
> coupling) `solve_deuteron()`'s default call site uses, or why it differs from the fully-refined potential
> Chapter 14 presents as the model's own headline deuteron result. This is a small, physically inconsequential
> ($<0.5\%$) numerical inconsistency between two findings' own displayed numbers for a quantity the model
> computes exactly once per call — the same category of unreconciled small discrepancy Chapters 7, 19 and 20
> already logged (Gaps G-5, G-9, G-12) for other quantities — not a fabricated bridge over a real hole, but a
> genuine, disclosed loose end. Flagged here rather than silently resolved in either direction; not fixed in
> this chapter (documentation-only). Whoever next touches `ca-simulation/ca_nuclear.py`'s `solve_deuteron()`
> default parameters should either confirm F148/F157 call it with a stale (pre-F113/F126/F128) configuration
> and update the assembler's cross-reference, or confirm the $0.45\%$ gap is a genuine, disclosed
> parameter-tuning difference and say so in F148/F157's own text.

## 24.7 Falsifiers

From the relevant claim cards, at their actual status — every one of this chapter's nine claim cards
carries `falsifier: unset` (`CL111`, `CL131`, `CL139`, `CL140`, `CL141`, `CL142`, `CL143`, `CL169`,
`CL182`), which is declared debt per D12's own vocabulary (`tools/check_claims.py`'s closed vocabulary
distinguishes `unset` from an argued `falsifier: none`), not an absence of a testable prediction — the
findings' own algebraic and structural identities are, in every case, their own de facto falsifiers, the
same treatment Chapters 14 and 23 already gave their own `falsifier: unset` cards:

1. **R24.1/R24.2 (`CL111`).** A measured hydrogen spectrum inconsistent with the exact $-1/n^2$ series, the
   $\ell$-degeneracy, or the $\alpha^4$/$\alpha^2$ fine-structure scaling laws would falsify the Dirac–Coulomb
   construction directly — none is observed.
2. **R24.3 (`CL139`).** A real-space, real-time simulation of the model's own non-relativistic electron
   orbital in a genuine Coulomb well that fails to reach a bounded RMS radius (disperses like the free
   control) would falsify the stationary-cloud construction; the matched free-vs-bound contrast (R24.3) is
   the finding's own internal control.
3. **R24.5/R24.6 (`CL142`).** A measured (simulated) breakdown of the point-vs-resolved binding-energy gap
   — i.e. a case where the coarse-grained point-charge approximation fails to converge to the resolved
   proton's binding energy as $a_0/r_p$ grows — would falsify the block-spin multigrid's central licensing
   argument.
4. **R24.11 (`CL169`).** A live block-spin element run that fails to conserve the integer electron count,
   loses Pauli orthogonality among occupied orbitals, or fails to reproduce the correct Aufbau/Hund
   configuration for an element within the certified ladder (H, He, Li, C) would falsify the construction.
5. **R24.12/R24.13 (`CL182`).** The two live, quantified claims each carry a named threshold (F371's own
   §"Falsifier"): the "relativity is negligible for the valence IE through Zn" claim is falsified if a
   grid-converged recomputation pushes the valence relativistic shift above $\sim1$ meV (current margin:
   three to four orders of magnitude); the "missing exchange, not relativity, is the ceiling" claim is
   falsified if a grid-converged Hartree IE lands within $\sim10\%$ of NIST for any $Z=21$–$30$ element (it
   does not, at either $N=900$ or $N=1200$ checked); and the disclosed grid-sensitivity caveat itself is
   falsified if further refinement past $N=1200$ reverses or flattens the measured Na$\to$Ca$\to$Fe$\to$Zn
   growth trend (not checked past $N=1200$, named as follow-on work).
6. **R24.14 (`CL143`).** A measured hydrogen emission spectrum with line positions, relative intensities, or
   selection rules (in particular, a non-vanishing $2s\to1s$ or $3d\to1s$ dipole rate) inconsistent with the
   model's own F125-level dipole-matrix-element calculation would falsify the emission construction.

---

## Notation established or extended in this chapter

*Harvested into Appendix A5 at the end of the build. Continues Chs. 1–23's tables.*

| Symbol | Meaning | First fixed here |
|---|---|---|
| $\mathrm{Ry}=\tfrac12\mu c^2(Z\alpha)^2$ | The physical Rydberg energy, built from the model's own $m_e$/$\alpha$ anchors and the reduced mass $\mu$ | §24.2.1 (F125) |
| $R_b$ | The block-spin coarse-graining map (Chapter 14's own $R_b$, F130/F133) applied here to a nuclear charge density rather than a field strength or bound-state spectrum | §24.2.4 (F159) |
| $b$ (block factor) | The representation choice carrying the proton-to-orbit scale ratio on two tractable lattices; not a fitted physical parameter | §24.2.4–24.2.5 (F159/F160) |
| $\text{atom}(Z,N)=\text{NUCLEUS}(Z,N)+\text{ELECTRON CLOUD}(Z)$ | The modular element-assembler composition rule | §24.2.6 (F148) |
| $Z_\text{eff}=n\sqrt{-2\varepsilon}$ | The per-orbital hydrogenic effective charge used to evaluate the scalar Dirac–Coulomb shift in the multi-electron SCF | §24.2.9 (F208) |
| $\Delta E_{n\ell}$ | The scalar (spin-averaged) Dirac–Coulomb $O((Z\alpha)^4)$ ionization-energy shift, applied per orbital in the SCF | §24.2.9 (F208) |

---

*One new gap was logged this chapter: **[G-13]**, the unreconciled $2.234$ MeV vs $2.224$ MeV deuteron-
binding-energy figure between F148/F157 (the assembler and multi-body findings) and F104/F113/F126/F128
(Chapter 14's own headline deuteron chain) — a small ($<0.5\%$), physically inconsequential, but genuine
and previously undisclosed numerical inconsistency, in the same category as Chapters 7, 19 and 20's own
logged small-discrepancy gaps (G-5, G-9, G-12). The chapter's other main open items — the Hartree/no-exchange
ionization-energy underbinding (F208/F371) and F371's own disclosed grid-convergence caveat — are not
logged as new `[G-N]` entries because they are already disclosed honestly, with quantified magnitude and a
named remedy, inside their own source findings' text, the same treatment Chapters 9, 14 and 23 gave their
own sources' self-disclosed open questions. F134's own "not yet a stationary orbit" forward flag (Chapter
14 §14.9) is resolved, not merely carried forward, by F156's non-relativistic-orbital construction (§24.2.2)
— recorded here as a genuine resolution rather than a remaining gap. No finding, claim card, module, or
test record was created or modified in the writing of this chapter.*
