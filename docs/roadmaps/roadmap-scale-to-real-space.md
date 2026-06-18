# Roadmap — Running the lattice at a scale analogous to real space

`2026-06-11 - 00:47` *(last reviewed 2026-06-12 - 15:03, folded in F138–F147)*

**Purpose.** Lay out, in phases, what the project must accomplish to run CASIM at a
scale that is *physically meaningful* — i.e. large enough that the emergent objects
(a bound proton, a hydrogen atom, a correctly-dispersing photon, a weak-field metric)
appear at the right SI magnitudes and throw off predictions that extend the Standard
Model. This is a planning document, hand-maintained, sitting alongside
`next-steps.md`.

---

## 0. The scale reality (why "fill real space cell-by-cell" is not the plan)

The canonical cell is locked (F107):

$$a = \sqrt{8\pi}\,3^{1/4}\,\ell_P = 6.5978\,\ell_P = 1.0664\times10^{-34}\ \text{m},\qquad
\tau = \frac{a}{c\sqrt3} = 2.0537\times10^{-43}\ \text{s}.$$

Consequences for a literal real-space fill:

| object | physical size | cells across | cells in 3-D |
|---|---|---|---|
| proton | $1.7\times10^{-15}$ m | $\sim1.6\times10^{19}$ | $\sim4\times10^{57}$ |
| hydrogen atom (Bohr) | $5.3\times10^{-11}$ m | $\sim5\times10^{23}$ | $\sim1.2\times10^{71}$ |

Current reach: sandbox $L\!\le\!64$ (3-D BCC, ~3.4 GB); the CASIM GUI envisages
$\sim 10^4{}^3 \approx 10^{12}$ cells (~90 GB). That is **~45 decades short of one
proton**. Brute force is permanently off the table.

Therefore "analogous to real space" must mean a tractable lattice in which a
**renormalised / coarse-grained** cell stands in for many physical cells, while the
emergent dynamics (speed of light, the $K$-dielectric, the propagator classes,
bound-state spectra) are provably preserved. The whole programme below rests on that
substitution being legitimate — which is **Phase 1**, the one with no prior result.

---

## Phase 1 — A proven coarse-graining / block-spin RG scheme  *(✅ DONE — F129–F133; updated 2026-06-11 - 19:32)*

**Goal.** A renormalisation-group (block-spin) transformation $\mathcal{R}_b$ that
groups $b^3$ cells into one super-cell and is shown to preserve the rotation rule:
$c_\text{lat}$, the F64 dielectric $K=e^{2u}$, and the F91 even/chiral propagator
classes. Then a coarse simulation of $N$ super-cells faithfully represents a patch of
$\,(bN)^3$ physical cells.

**Target theorems / checks.**
1. **$c_\text{lat}$ is an RG fixed point** — the $k\!\to\!0$ slope of the dispersion is
   invariant under $\mathcal{R}_b$, to machine precision, for all $b$.
2. **The LIV / lattice-artifact operators are irrelevant** — the leading dispersion
   correction's RG eigenvalue is $b^{1-n}<1$ for $n\ge2$; the continuum law
   $\Omega=c_\text{lat}|k|$ is the attractive IR fixed point.
3. The dielectric $K$ and Gauss-law constraints survive block-averaging (extend the
   scheme from the free photon to the F64/F106 gravity channel and the F110 link
   Hamiltonian).

**Status.** Free-photon sector attacked in F129 (this push). **Gauge + gravity
channels done in F130** (`ca_blockspin.py`, 30/30): T1 $c_\text{lat}$ fixed point,
T2 LIV operators irrelevant ($\lambda_n=b^{-n}$, leading $g_2=-1/162$ = F30), T3a
Gauss's law integer-exact under blocking (F110 convention), T3b dielectric lock
$AB\equiv1$ preserved by log-averaging (F64/F106), T3c even/chiral propagator
class preserved ($[R_b,R(\Omega)]=0$). **Confinement flow done (F130-C1):** the
string tension is the one *relevant* direction, eigenvalue $\lambda_\sigma=b$
(bond-moving $g^2\!\to\!b\,g^2$), a coarse F110 run on $b\times$ fewer plaquettes
reproduces the fine $V(b\cdot R)$ exactly, and the deconfining $\lambda$ is
irrelevant ($\sim b^{-2}$). **Phase 1 complete (2026-06-11):** the last Phase-1
item — the CASIM block-spin engine kernel — landed in **F133 (Phase 4, 11/11)**.

**Why first.** Without it, every later phase is a bigger toy, not a smaller universe.

---

## Phase 2 — Emergent bound states must actually form

"Real space" with nothing in it is pointless; the payoff is atoms.

- Confinement → a stable proton/neutron (F86 colour condensate, F94 LGT confinement,
  F97 baryon $Z_3$ centre-phase closure; matter-binding roadmap phases p1–p4).
- EM binding → the hydrogen atom is already demonstrated as an electromagnetic bound
  state (F125, Rydberg + Dirac fine structure). Extend to multi-electron / multi-nucleon.
- Couple Phase 1: show a *coarse-grained* bound state reproduces the fine-grained
  spectrum (the RG must commute with binding, at least in the long-wavelength sector).
  **Done (F131):** the block-spin RG commutes with binding in the IR — a coarse
  harmonic/Coulomb bound state on $b^d\times$ fewer cells reproduces the fine
  spectrum (low levels $<1\%$, $O_h$ triplet degeneracy preserved, ground overlap
  $0.9999$, both → analytic $E_N=\omega(N+\tfrac32)$); coarse error is the
  irrelevant $O((ka)^2)$ operator. Confined flux-string bound state covered by
  F130-C1. **Dynamical bound states done (F132):** the pion (F74/F103 CONTACT
  coupling is RG-relevant — runs as $g/g_c$, the Watson threshold), the deuteron
  (F104 finite-range coupling irrelevant — fixed, $O(h^2)$), and the baryon (F122
  mass = the C1-covariant string scale, $E_\text{rel}\propto\sigma^{2/3}$) all
  coarse-grain. Unification: relevant couplings = $\sigma$ + contact; irrelevant
  = LIV + deconfining $\lambda$ + smooth potentials. **Real-time wave-packet
  dynamics done (F135):** the static-eigenstate result is upgraded to genuine
  real-time dynamics — a moving, spreading massive Dirac packet satisfies
  $R_b\circ\text{evolve}_\text{fine}^{bN}=\text{evolve}_\text{coarse}^{N}\circ R_b$
  at every coarse tick ($1.4$–$2.5\times10^{-15}$), velocity + spreading
  reproduced, and **mass is the matter sector's relevant operator** (rest-gap
  eigenvalue $b$, like $\sigma$; physical Compton wavelength invariant) — completing
  the RG class table (relevant = mass/$\sigma$/contact, marginal = $c$, irrelevant =
  LIV/smooth). **Remaining Phase-2 items:** (i) a *real-space confined proton* —
  **DONE (F135, 2026-06-11, 3/3):** the non-perturbative confining string is now
  built into real-time lattice dynamics as a Lorentz-**scalar** position-dependent
  mass $m_\text{eff}(x)=m+\sigma|x-R_\text{cm}|$ (the MIT-bag / F86 colour-dielectric
  mechanism — vector confinement Klein-tunnels and was excluded), and a three-body
  cluster stays bound in real space; closes the F134-U1 null. Extended since: the
  scalar string now binds a genuine SU(3) colour-triplet `uud` proton (F136), the
  proton digs its own live colour-dielectric bag (F137) with a self-consistent
  dual-Ginzburg-Landau back-reaction that cures the pinch-off (F139), and the
  confining σ is now **measured from the model's own 3D SU(3) gauge dynamics** and
  fed into the bag (F146, emergent — β and the lattice the only inputs), leaving
  only the U4 gauge↔Dirac lattice-spacing scale carry. (ii) **DONE (F140, 9/9):**
  the confined baryon is coarse-grained on an actual lattice (the K=0 hyperradial
  element block-spins; $E_\text{rel}$ rel-err 0.01–0.13% at $b=2/4/8$), supplying
  what F132 handled only by ingredient-covariance. (iii) multi-electron /
  multi-nucleon (helium needs the Pauli antisymmetriser) and their coarse-graining
  — **STILL OPEN** (untouched by F134–F147; the one un-started Phase-2 item).

---

## Phase 3 — Close the remaining free inputs (parameter-free predictions)

From the 2026-06-06 open-inputs audit, three clusters; status:

- **SI ruler $a$** — CLOSED (F107).
- **Generation count** — CLOSED (F75 = 3 from $O_h$).
- **QCD calibration block** — PARTIALLY CLOSED; routes reviewed 2026-06-12
  (`docs/theory/qcd-calibration-derivation-routes.md`). **Route A executed
  (F144):** $g_s=\tfrac12$ derived, zero-parameter $\alpha_s(M_Z)$ converged
  $+8.4\%$, F119 hierarchy landed ×1.9 — remaining: one scheme constant
  (bounded ≈1.8 vs Wilson 28.8). **Route C executed (F145):** exact Fierz
  $c=\tfrac29$, bare-coupling no-go, χSB forced by the F144 running; fit
  bracketed, residual = the same IR-coupling number. **σ now emergent (F146):**
  the string tension is measured from the model's own 3D SU(3) gauge dynamics
  (β + lattice the only inputs) and fed into the F135 bag — only the U4
  gauge↔Dirac lattice-spacing scale carry (~1.5×) remains on the σ side.
  Route D ($g_A$ from F122) remains an unblocked build. **Net residual:** ONE
  nonperturbative IR-coupling number (shared by F124/F144/F145) + the U4 scale
  factor.
- **$E_g$ sextic-brake $C/W$** — OPEN, and now the *pacing* item: F143 §5 (and
  F147) relocated the last NDA→exact step for the EWSB matching scale $\mu_\star$
  to the $E_g$ condensate stiffness $f_{E_g}$ (the F118 $\kappa_E<0$ sector),
  because the fermion sea induces **zero** gauge stiffness (transverse
  conjugation no-go F143, one-tick rigidity theorem F147). So this single
  coefficient now gates an *exact* $\sin^2\theta_W$ as well.
- **$\sin^2\theta_W$** — CLOSED numerically (F138): F41's kinetic-term-free
  hypercharge makes $\tfrac14$ the matching value at $\mu_\star=4\pi v=3.094$ TeV,
  and 1-loop Higgs-free running gives $\sin^2\bar\theta_W(M_Z)=0.23173$ vs PDG
  $0.23122$ — the +12 % gap (F115) drops to **+0.22 %** with no new knob. F143/F147
  *derived* F138's premise (gauge-rigidity no-go, all channels). F141 reframed
  F49's $2/9$ as the on-shell endpoint ($m_Z/m_W=3/\sqrt7$, −0.063 %); F147 closed
  its dynamical ratio (U2 = 1). Remaining: the *exact* $2/9$ assignment (F141 U1
  universality + U3 quadratic-form assembly) and the exact $\mu_\star$ (→ the
  $E_g$ brake above) — sub-percent exactness tails, not the gap.

A prediction is only "beyond-SM" in a sector once that sector is knob-free.

---

## Phase 4 — A compute core that survives the scale and the chiral transforms

- **Block-spin kernel in CASIM** — **DONE (F133):** $\mathcal{R}_b$ is a first-class
  engine op. `LatticeSpec.block` lets a run declare a physical patch
  (`physical_L=L·block`, `cell_factor=block^d`; scenario `physical_patch`/`block`);
  `Simulation.block_spin(b)` coarse-grains a live run in place (schedulable via a
  scenario `blockspin:` field), with the renormalised rule $\Omega(\kappa/b)$
  keeping the even-law channel faithful ($[R_b,\text{evolution}]=0$ on band-limited
  fields, $c_\text{lat}$ fixed). **All three propagator classes done (F134):**
  `renormalized_chiral_step` (W±) and `renormalized_weyl_step` (Weyl per-branch)
  reduce bit-for-bit to the fine kernels at $b{=}1$, stay unitary, and commute
  with $R_b$ ($\sim1.5\times10^{-15}$); the channels use them when block>1.
- **GPU / distributed FFT + local-update kernels** — the backend **seam is
  validated** (F134: a `numpy_fft` backend is identical to `ca_fft` to round-off
  through `casim.lattice.backend`; a GPU backend is the same drop-in but needs
  hardware). The FFT round-off floor is characterised as $\sim1$ ulp/step and
  L-stable (F134). Still open: an actual GPU/distributed kernel + local-update
  stencils for huge $L$ (hardware / optimisation).
- **Verified hand-rolled linear algebra for chiral steps** — **DONE (F134):**
  `casim.lattice.chiral_core` does every chiral 2×2 mix on explicit real/imag
  pairs (no `np.linalg`), matches the audited kernels bit-for-bit, and routes
  through the backend `chiral_transform` seam. (Original note:) per the standing CLAUDE.md
  caveat, numpy/scipy can silently drop real/imag parts on chiral transforms. The even
  (real $E,B$) photon is safe; the W/gluon chiral sectors need an audited core before
  large runs are trusted.
- **FFT floor / resolution** — characterise the spectral floor as $L$ grows.

---

## Phase 5 — New-prediction targets (where "build on the SM" lives)

Once 1–4 hold, the model predicts quantities the SM takes as input:

- Charged-lepton + fermion spectrum from one mass scale (F120 — already 0.1 %).
- Koide-chain mass relations (F92/F93); see-saw neutrino mass.
- $\sin^2\theta_W$ tightened (Phase 3).
- **LIV time-of-flight** — F30 even law $\delta v_g/c=-k^2/54$ ⟹
  $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.1\,E_P$. Falsifiable *now* with no
  scale-up: any $n{=}2$ bound above $1.4\times10^{19}$ GeV kills the cell (F107).
- Gravitational-sector corrections: exponential-metric shadow +4.6 % (F114), exact
  $-4$ lensing coefficient (F107/L4).

---

## Dependency order

```
Phase 1 (RG scheme) ──► Phase 4 (block-spin kernel in CASIM) ──► large faithful runs
        │                                                              │
        └──► Phase 2 (bound states, coarse-grained) ──────────────────┤
Phase 3 (close inputs) ───────────────────────────────────────────────┴──► Phase 5 (predictions)
```

Phase 1 was the gate — **now closed (F129–F133)**. Phase 4's block-spin kernel is
also done (F133); all three propagator classes, the hand-rolled chiral core, and
the FFT floor landed in F134. The real-space confined proton (Phase 2 item i)
landed in F135 and was extended to a colour-triplet proton with a self-sourced,
back-reacting, emergent-σ bag (F136/F137/F139/F146); the lattice coarse-grained
baryon (Phase 2 item ii) landed in F140; the Weinberg gap (Phase 3) closed in
F138.

**Remaining open work (as of 2026-06-12):**
- **Phase 2 (iii)** — multi-electron / multi-nucleon (helium + Pauli) and their
  coarse-graining. The one un-started bound-state item.
- **Phase 3 — $E_g$ sextic-brake $C/W$.** Now the pacing item: gates an exact
  $\mu_\star$ and hence an exact $\sin^2\theta_W$ (F143/F147).
- **Phase 3 — QCD calibration residual.** One nonperturbative IR-coupling number
  + the U4 lattice-spacing scale factor; Route D ($g_A$) unblocked but unbuilt.
- **Phase 4** — true GPU/distributed kernels + local-update stencils for huge $L$
  (hardware / optimisation, not structural).

*(content updated 2026-06-12 - 15:03; supersedes the 2026-06-11 - 19:32 revision)*

---

### Update 2026-06-15 - 01:50 — F148–F155 + the production A-NP runs folded in

Status changes since the 2026-06-12 fold (no item flips to *fully* closed; two are
materially sharpened and one is consolidated):

- **Phase 2 (iii) — multi-electron — still OPEN, but the composition layer now
  exists.** F148 (`ca_element.py`, 13/13) built the modular assembler
  `atom(Z,N) = NUCLEUS(Z,N) + ELECTRON CLOUD(Z)` and verified it on ¹H; the
  heavier-element / multi-electron paths are *wired but not yet exercised* (no
  helium + Pauli antisymmetriser demonstration). So the framework is in place;
  the actual multi-electron bound state and its coarse-graining remain the
  un-started item.
- **Phase 3 — $E_g$ brake — source & kind CLOSED, magnitude CONSOLIDATED (F150).**
  The brake $C$ is now proven to be a condensate self-coupling (two-route no-go:
  F95 per-axis scaling/sign ⊕ F147 exact one-tick rigidity), its *kind* is fixed
  as an induced coupling with an exact Fierz projection (F145), and its *magnitude*
  $\lambda_6$ is shown to be the **same single nonperturbative IR-coupling
  normalisation** that owns the F124/F144/F145 residuals. Consequence: the brake
  is **no longer a separate open input** — it merges into the one shared IR residual
  below. Target sharpened to $\cos3\delta^\star=\cos Q$ ($3\delta^\star=Q=\tfrac23$,
  $1.7\times10^{-5}$). Still open: the first-principles value of that one shared
  number.
- **Phase 3 — QCD/IR-coupling residual — SHARPENED, still OPEN (now genuinely ONE
  number).** Residual **B solved** (F154: the gap fixes $\alpha_\text{eff}^\ast$,
  converged & L-stable) and its freeze value **bracketed anchor-free** to
  $[0.31,0.38]$ (F155). Residual **A bracketed** (F155): the tadpole sector is
  *exactly* empty (Wilson 28.81 structurally absent), the lattice−continuum
  subtraction machinery is convergent, and $q_\ast a\in[0.577,0.979]\ni0.733$ with
  $\Lambda$-ratio $O(1)$ — **not** pinned to the digit. The gauge-fixing-free
  **A-NP production runs now exist** (`su3_static_potential_b9/b12.json`, L=24,
  β=9 & 12, native ~3.5 h each): emergent $\sigma a^2 = 0.264$ (β=9) / $0.132$
  (β=12) confirm the F146 confinement scale is **not a single-β artifact** and
  trend correctly ($\sqrt\sigma/g_3^2 = 0.77\to0.73$ toward the continuum), but the
  static potential is **pure-linear within these statistics** — the Coulomb/$\alpha_V$
  running is not resolved, so the two β do **not** pin $q_\ast$ (they confirm $\sigma$
  and bracket, consistent with F155). Pinning $q_\ast$ still needs either the gluonic
  3-gluon+ghost finite part (F155 §6) or a higher-statistics / wider-β-lever A-NP
  run. Route D ($g_A$) still unbuilt.
- **Phase 4 — GPU/distributed kernels — unchanged (hardware).**

Net: the two formerly-separate Phase-3 open inputs ($E_g$ brake + QCD residual)
are now **one** shared nonperturbative IR-coupling number; everything else
(B, the freeze, the tadpole-free $\Lambda$-ratio, emergent $\sigma$ at two β) is
closed or bracketed. *(See F148, F150, F154, F155, F146; runs
`test-results/su3_static_potential_b{9,12}.json`.)*

---

### Update 2026-06-17 - 20:23 — Phase 2(iii) CLOSED (F157)

The last un-started Phase-2 item — multi-electron / multi-nucleon and the
composition layer — is now **DONE** on the spectral/assembler side (F157,
`ca_manybody.py`, 5/5). The F148 assembler's A≥3 and Z≥2 hooks now COMPUTE:
a Hartree SCF electron cloud (helium IP 24.0 eV vs 24.59, model-only) and an
A-body variational cluster nucleus anchored to the model's own deuteron (alpha
−30.1 MeV vs −28.3). He-4 composes end-to-end as a neutral stable atom.
Remaining Phase-2 caveats: nuclear **saturation** (heavy A overbinds — needs the
spin-isospin/Pauli structure) and the **coarse-graining** of these many-body
states (ties into U4). The real-time real-space neutral atom (U3) landed
concurrently as F158 (`roadmap-unified-real-space.md`). **Net: Phase 2 is now
closed except saturation + coarse-graining; the open frontier is Phase-1-backed
U4 (block-spin multigrid) and the Phase-3 IR-coupling residual.**
