# Status of the Project — In-Depth Guide

**Generated:** 2026-07-15 - 19:15
**How this was generated:** run `/project-audit` (see `.claude/commands/project-audit.md`)
or the standalone prompt in `docs/audits/project-audit-prompt.md`. Rerun after each build
milestone to refresh this guide from the live indexes and ledgers.

**Scope at this snapshot** (file counts, not prose estimates):

| Artifact | Count |
|----------|-------|
| Findings | 246 (max `F246`) |
| Kernel modules (`ca-simulation/ca_*.py`) | 90 |
| Derivation modules (`derive_*.py`) | 6 |
| Fork modules (`ca-simulation/forks/`) | 46 |
| CASIM package files (`src/casim/**/*.py`) | 39 |
| Tests (`tests/**/*.py`) | ~320 |
| CASIM scenarios | 46 |
| Active papers | 12 (I–XII) |

> **Index note:** `findings-index.md` regenerates to F245 at times and can lag the newest
> finding file. As of this snapshot the newest findings are **F245/F246 (2026-07-15)**; if the
> index shows less, run `python3 tools/regen_indexes.py`.

---

## 1. Executive summary

This project asks a single question and pursues it with unusual discipline: **if our
universe is a lattice of cellular automata, can we reproduce known physics — special
relativity, quantum mechanics, the Standard Model gauge sectors, and general relativity —
from one simple local update rule, and derive the constants rather than fit them?** The
working substrate is a body-centered-cubic (BCC) lattice of Weyl quanta whose update is a
real rotation of an $(\mathbf{E},\mathbf{B})$-type vector pair. The guiding philosophy is
"elegant design": the universe is assumed to be both fully comprehensible and simple in
construction, so the standard of success is **algebraic exactness first, machine-precision
exactness second, quantitative percent-level agreement third** — and honest negatives count
as results.

The elevator claim is that a large fraction of twentieth-century physics has been
reconstructed on this one substrate with **no Higgs field** (mass comes from Ludwig's chiral
SU(2) complex-mass coupling) and **gravity as an emergent, induced effect** (the value of
Newton's $G$ is derived structurally). Across 246 findings and ~320 tests, the model has
reached the point where the remaining unknowns can be counted on one hand — most famously,
three separate open problems in the strong sector have been shown to collapse into **a single
undetermined one-loop constant $d_1$**.

Maturity by sector at this snapshot:

| Sector | Status | Landmark findings | What's still open |
|--------|--------|-------------------|-------------------|
| Lattice / foundational | Mature; core identities exact | F25, F26, F46, F129, F167, F246 | L2 subleading closed (F246); scale-setting seams |
| EM / photon | Mature; birefringence crisis resolved | F67, F68, F69, F91, F105 | none of substance |
| Electroweak (Higgs-free) | Mature | F27, F29, F45, F49, F138, F231 | E1 (weight→phase principle) |
| Strong / QCD / hadrons | Advanced; one constant from closing | F43, F71, F116, F144, F162, F240 | $d_1$ (= E3 = Q1 = Q2), Q3 refinement |
| Gravity / cosmology | Reclassified to GR-exact; origin of $G$ derived | F64, F79, F178, F180, F183, F196 | G1 ($\Omega_\Lambda$ O(1) factor, likely anthropic) |
| Fermion & lepton / Koide | Mature; spectrum to ~0.1% | F75, F76, F80, F120, F174, F175 | weight→phase (shared with E1) |
| Neutrino / dark matter | Mapped; candidate identified | F47, F200, F216, F223, F228, F236 | $\beta$ relic abundance (free initial condition) |
| Quantum-info & condensed-matter | Broad, exact | F210, F212, F218, F221, F226, F227 | applied refinements only |

**The single deepest open number** is the strong-sector one-loop background-field constant
$d_1$ ($\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$); computing it closes three
ledger items at once (F233/F235; the $b_0=\tfrac{11}{3}C_A$ leg is already exact, F162).

---

## 2. The theory in one page

The model deliberately deviates from the Standard Model in a small number of recorded places
(full detail and dates in `docs/theory/key-decisions.md`). The six core design decisions:

1. **SU(2) derivation, not the Standard Model.** The electroweak structure follows Ludwig's
   SU(2) construction rather than the SM presentation.

2. **The speed of light is a rotation rate, not a phase velocity (F25/F26).** $c_\text{lat}$
   is the angular rotation rate of the real $(\mathbf{E},\mathbf{B})$ pair per unit spatial
   wavenumber, $c_\text{lat}=\left.\tfrac{d\Omega}{d\lvert k\rvert}\right|_{\lvert k\rvert\to 0}$
   with $\Omega=2\omega(\lvert k\rvert/2)$. Numerically $c_\text{lat}=1/\sqrt3$ on the BCC lattice.

3. **Higgs-free mass via hypercharge on $U(x)$ (F27).** Chiral SU(2) from $\beta$-gauging the
   Dirac matrices yields complex mass directly; hypercharge lives on $U(x)$, so no Higgs field
   is posited.

4. **Gravity is the induced Einstein equation (F64 → F178).** The fundamental law is
   $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$ with a structurally derived
   $G=a^2c^3/(8\pi\sqrt3\,\hbar)$ (F79/F107). The single impedance-matched dielectric
   $K=\exp(2GM/rc^2)$ ($A=1/K$, $B=K$, $AB\equiv1$) is the **vacuum/weak-field representation**
   (PPN $\beta=\gamma=1$, GR-identical) — not the interior law, where the full-tensor source
   makes the dynamics GR/TOV and the exact vacuum solution Schwarzschild (F178 supersedes the
   F114 horizon-free black hole).

5. **The photon is the paired-spinor photon (F67/F68/F69).** It is a bound pair of two spin-½
   Weyl quanta on opposite chiral branches, so the pair rate is the helicity-symmetric even
   law $\Omega_\text{pair}=\Omega_\text{even}$: massless, luminal, transverse, and
   **non-birefringent** — the U(1) identity channel that minimal coupling forces. The old
   $\sigma$-bilinear photon (birefringent, excluded by GRB/AGN polarimetry) is retained only
   for the massive/non-Abelian W/Z/gluon sectors. Propagator classification (F91): γ even,
   W± chiral, Z mixed, gluon even — each forced by its coupling's branch structure.

6. **Elegant design.** The universe is assumed fully understandable and simple; derive before
   positing, and prefer exact algebra to fitted numbers.

---

## 3. Sector-by-sector status

### 3.1 Lattice / foundational & special relativity

The substrate is a BCC Weyl QCA (`ca_bcc.py`, `ca_core*.py`). The foundational identities are
established and mostly exact: the discrete-time real-rotation Maxwell law (F25), the
speed-of-light-as-rotation-rate reinterpretation (F26), the spherical-Pythagorean dispersion
$E^2=p^2c^2+m^2c^4$ (F46), rest mass as the unique zero-$k$ rotation rate of the rule's
generator (F167), and the block-spin RG confirmation that $c_\text{lat}$ is an exact fixed
point with Lorentz-violation irrelevant under coarse-graining (F129). Velocity addition and the
Lorentz-violation coefficient $\beta_\text{LV}$ are derived in closed form
(`derive_velocity_addition.py`, `derive_beta_LV.py`). The two subleading curl/dispersion
coefficients — long the last "foundational" open items — were closed on 2026-07-15: **F245**
gives closed forms for the composite-photon curl residual (the old $0.01883$ was a random-seed
artifact, mean zero), and **F246** shows the even-rotation law contains only odd powers of
$\lvert k\rvert$, so **all even-power dispersion corrections vanish identically** and the
leading Lorentz-violation signature is a CPT-even cubic $\lvert k\rvert^3$ term. The lattice
spacing is adopted at the parameter-free $a=\sqrt{8\pi}\,3^{1/4}\ell_P$ (F107), gated by the L4
lensing and GRB checks.

**Exact / machine-precision:** F25, F26, F46, F129 fixed point, F246 even-power vanishing.
**Open:** independent mass-blind pin of $a$ is a scale-invariance no-go (L3, closed negative).

### 3.2 EM / photon

The photon crisis — early composite-photon constructions were birefringent and excluded by
polarimetry — is fully resolved. The canonical photon is the paired-spinor photon
(`ca_photon_pair.py`, F69), the U(1) identity channel forced by minimal coupling (F68), with
helicity mapped to BCC chirality (F37/F65). The pairing-classification theorem (F91) fixes the
propagator of every gauge sector from its coupling. Axial photons are exactly dispersionless
(F105); the interacting two-body photon wavefunction is built (F168/F169). `ca_maxwell.py` /
`ca_maxwell_2d.py` are **historical** — the $\sigma$-bilinear field construction they hold
survives only for the massive/non-Abelian sectors.

**Status:** mature; no open items of substance.

### 3.3 Electroweak (Higgs-free)

Chiral SU(2) with complex mass from $\beta$-gauging (F27) is the cornerstone; the W-triplet
bilinear bridges the F26 rotation law to F27 (F29). The dynamical Z neutral-current sector
(`ca_z_field.py`), charged current (`ca_charged_current.py`), and hypercharge U(1)$_Y$
(`ca_hypercharge.py`, F41/F42) are wired. The Weinberg angle has two reconciled faces: the UV
matching value $\sin^2\theta_W=\tfrac14$ at $\mu^*=4\pi v$ (F138) and the on-shell endpoint
$\tfrac29$ from BCC counting (F49), reconciled by one-loop running × scheme conversion (F231),
with $m_Z/m_W=3/\sqrt7$ to $0.064\%$. Anomaly cancellation is exact (all six traces zero); W:Z
mass ratio follows from Wigner–Seitz face counting (F141).

**Open (E1):** the *number* $\delta^*=\tfrac29$ is derived exactly as the $E_g$ representation
weight (F174/F175); what remains is the **weight→phase principle** — why the saturated
condensate phase in radians equals the representation weight. This is the one genuinely-open EW
item and it is shared with the lepton sector.

### 3.4 Strong / QCD / hadrons

The largest code sector (~31 kernel modules). Dynamical SU(3) gluons (F43), gradient-flow
confinement (F70), and the first colour-singlet proton (F71) are established; confinement is
modeled two ways — colour-dielectric dual-superconductor (F86/F88) and 3+1D lattice-gauge Monte
Carlo (`forks/lgt_fork_A_mc.py`). The dynamical baryon (F122), pion as Goldstone (F103), and
the nucleon at $3m_c\approx938$ MeV (F123) are built, as is NN one-boson-exchange binding of the
deuteron (F206/F240). Scale-setting is advanced: $\alpha_s$ by dimensional transmutation with
$g_s=\tfrac12$ derived (F144), reproducing $\alpha_s(M_Z)$ to +1.3%, and the background-field
$b_0=\tfrac{11}{3}C_A$ gate passes **exactly** (F162).

**The defining open problem:** three ledger items — the overall mass scale $N$ (E3), the
scale-setting $\sqrt\sigma/f_\pi$ (Q1), and the $\alpha_s$ lattice→$\overline{\rm MS}$
conversion (Q2) — have been shown to **collapse into one undetermined constant, the one-loop
background-field $d_1$** ($\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$;
F233/F235). Computing it (the F162 programme) closes all three. Q3 (the NN isoscalar-vector
$\omega$ repulsion) is a bracketed coupling, quenched like the scalar channel.

**Exact:** $b_0=\tfrac{11}{3}C_A$ (F162), the chiral factor $\Lambda/f_\pi=7.04$.
**Quantitative:** $\alpha_s(M_Z)$ +1.3%, $N$ to a factor 1.9 zero-parameter (F233).

### 3.5 Gravity / cosmology

The most-revised sector, now settled. The 2026-06-29 decision (F178) adopts the induced
Einstein equation with the **full stress-energy source** as fundamental; the energy-only
$\nabla^2\ln K=-8\pi T^{00}$ (F106) is its static weak-field reduction, and the exact vacuum
solution is Schwarzschild (superseding the F114 horizon-free dielectric black hole). Newton's
$G$ is derived structurally, Sakharov-free (F79). The gravity dielectric (`ca_gravity.py`)
remains canonical in vacuum/weak-field; the interior/strong-field solver is full Einstein/TOV
(`ca_stellar.py`, `ca_interior_metric.py`, F181). GW speed equals $c_\text{lat}$, so GW170817
survives (F180); Schwarzschild/Kerr are exact (F183); neutron stars, shadows, QNM ringdown, and
inspiral phasing are built (F184–F189, `ca_qnm.py`, `ca_raytrace.py`, `ca_inspiral.py`). The
cosmological-constant problem is reduced from 121 orders to one O(1) factor: the bare CC is
exactly zero (F193) and the dilution exponent $p=2$ is derived (F196), landing 0.10 dex from
$\rho_\Lambda$.

**Open (G1):** why the residual lands at $\Omega_\Lambda\approx0.69$ rather than 0.1/0.9 — the
event-horizon route is circular; classified coincidental/anthropic (do **not** reopen $p=2$).

### 3.6 Fermion & lepton / Koide

Exactly three generations fall out of the BCC point group (F75), with the crystal-field
hierarchy and Koide signature (F76). The NJL gap and the Koide $\sqrt m$ Cooper-pair amplitude
(F77/F78) lead to the 45° EM-saturation charged-lepton Koide point (F80/F81/F82). The spectrum
is electron-calibrated / τ-anchored to ~0.1% (F120/F121), and the lepton shape-angle
$\delta^*=\tfrac29$ rad is derived as the $E_g$ representation weight (F174/F175). The full 3×3
Higgs-free see-saw / PMNS is built (F236, `ca_majorana.py`).

**Open:** the same weight→phase principle as E1; the charged-lepton spectrum is honestly a
one-angle fit given $\delta^*=\tfrac29$, $Q=\tfrac23$ (closed-negative CN3).

### 3.7 Neutrino / dark matter

The Higgs-free right-handed-neutrino Majorana see-saw (F47) and the sterile-neutrino
dark-matter relic (F200) are built; the keV sterile candidate is under quantified observational
pressure and demoted to sub-dominant (F205/F237 — an honest exclusion of keV sterile as 100% DM).
The surviving 100%-DM candidate is the **massive spin-2 "geon"**: no native massive spin-2
exists in vacuum (CN5, F216), so it must be a gauge-neutral bound state; it binds at
$\sqrt2\,M_\text{Pl}$ (F223) and is the stable one-cell Planck-mass black-hole remnant (F228).
The Bullet Cluster falsifies emergent-gravity-only DM (F191/F194), and the geon passes every
screen (cold, collisionless, above the fuzzy floor).

**Open (D3):** the relic abundance $\beta$ is a **free cosmological initial condition** — the
model has no inflaton/primordial-spectrum sector, so $\Omega_\text{DM}h^2=0.12$ is not a
derivable coupling (F238, sharpened to "provably free, stated cause").

### 3.8 Quantum-info & condensed-matter applications

A broad, largely exact applications layer demonstrating the substrate computes and condenses.
Electrical superconductivity is built on the lattice (`ca_superconductivity.py`, F210), with
$T_c$ / Eliashberg / first-principles $\alpha^2F$ and Padé gap ratios (F211/F215/F218), and the
Coulomb pseudopotential $\mu^*$ **derived** from the F64 dielectric via Thomas–Fermi screening
(F242 — the SC sector's last empirical input, closed positive). On the quantum-information side:
the substrate generates genuine $2^n$ entanglement (F212); the super-exchange $J$ emerges from
`ca_dirac` hopping and second quantization (F214/F217); CZ/CNOT/CCZ compile **exactly** from the
lattice exchange interaction, running Grover / Deutsch–Jozsa / QFT / GHZ live (F218/F220/F222);
stabilizer error correction holds a logical qubit (F221); the register saturates Tsirelson
$S=2\sqrt2$ (F226, Bell-indistinguishable from QM); and there is no observable
intrinsic-decoherence floor (F227). The Casimir effect is reproduced (F207/F209).

**Status:** mature; remaining items are applied refinements, not foundational gaps.

---

## 4. Code & infrastructure

The kernels (`ca-simulation/ca_*.py`, 90 modules) are the single source of truth, grouped
roughly as: lattice/foundational (~6), EM/photon (~7, with `ca_maxwell*` historical),
electroweak (~7), strong/QCD (~31 — the largest sector), gravity/cosmology (~15), fermion &
lepton/atomic (~5), neutrino/dark (~2), and quantum-info/condensed-matter (~11), plus engine and
coarse-graining utilities. Six `derive_*.py` modules hold the closed-form algebra (velocity
addition, $\beta_\text{LV}$, colour condensate, curl subleading, dielectric no-confine, F26
dispersion). The `forks/` directory (46 files) holds competing candidate fixes run head-to-head
via harnesses — chiefly the gravity/GR-3 family, plus curl-geometry, dark-sector, and
electroweak variants.

The **CASIM package** (`src/casim/`, 39 files) is a refactor-not-rewrite layer over the flat
kernels: an `engine/` with a `Channel` registry (~29 registered channels across photon, weak,
Z, gluon, gravity, coupled, spectral-matter, tier-3, many-body, and typed-particle families) and
a separate observer registry; `fields/`, `lattice/`, `particles/`, `gravity/`, `suite/`,
`analysis/`, `io/`, `viz/`, and a `gui/`, driven by `cli.py` (`casim` console script) and
`verify.py`. There are 46 scenario YAMLs (`scenarios/`, with a RUN-GUIDE).

Six machine indexes keep session context small — `INDEX.md` (hand-maintained map),
`findings-index.md`, `project-status-index.md`, `tests-index.md`, `code-index.md`,
`docs-index.md` — regenerated by `python3 tools/regen_indexes.py` after any session that adds
findings, tests, modules, or docs. The append-only `docs/status/changelog.md` (newest-first) and
`docs/status/exactness-inventory.md` are the running record.

---

## 5. Tests & exactness

Roughly 320 test files under `tests/`: `tests/findings/` (~255, one `test_F*.py` per finding),
`tests/runners/` (~42 standalone drivers/scans), `tests/priority/` (~16 GR/QM/QFT/SR battery),
`tests/casim/` (~6, the **default `pytest` target** per CLAUDE.md), and `tests/falsification/`
(~31 markdown spec briefs — future confrontations, no `.py` yet). The pass picture is clean:
findings that carry an explicit tag report full `X/X PASS` (e.g. 30/30, 20/20, 11/11) with **no
failing tests** in the index. The few non-clean rows are open *research* items, not test
failures — e.g. `test_F192_vacuum_energy` (CC under the full tensor, open), the F239 scheme
factor (one leg open), and one retired 2026-05-26 tunneling test. Falsification attempts that
"fail to falsify" (F243 low-density lensing) are positive results despite the wording.

Exactness is tracked in `docs/status/exactness-inventory.md` across three tiers — **exact
algebraic**, **machine precision**, and **quantitative** — plus a "currently not-yet-met" table.
The house rule is to prefer the higher tiers and never inflate a quantitative match to "exact";
this guide follows the same discipline (see the per-sector "exact vs quantitative" notes above).

---

## 6. Open frontier

Mirrors the authoritative ledger `docs/status/open-derivations.md` (last ledger audit
2026-07-02, with S1/F1/F2 updated 2026-07-03). Of 17 nominal rows, **~5 genuinely-open targets**
remain:

| ID | Sector | Open target | Note |
|----|--------|-------------|------|
| ~~L1~~ | Lattice | curl subleading coefficient | **CLOSED F245 (2026-07-15)** |
| ~~L2~~ | Lattice | F26 subleading / dispersion | **CLOSED F246 (2026-07-15)** |
| E1 | EW/lepton | weight→phase principle | number $\tfrac29$ derived (F174/F175); principle open |
| Q1 = Q2 = E3 | QCD | the one-loop constant $d_1$ | **the deepest open number**; F162 programme |
| Q3 | QCD | NN $\omega$ repulsion | bracketed coupling |
| G1 | Gravity | $\Omega_\Lambda\approx0.69$ O(1) factor | likely anthropic; do not reopen $p=2$ |
| D3 | Dark | relic abundance $\beta$ | provably free initial condition (F238) |

**Deepest single open number:** the strong-sector one-loop background-field constant $d_1$
($\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}\approx1.78$). E3, Q1, and Q2 all reduce to it
(F233/F235); the $b_0=\tfrac{11}{3}C_A$ leg is already exact (F162). Computing $d_1$ closes
three ledger items at once.

**Closed-negative results** (deliverables, not gaps — do not re-attack): Bell-indistinguishable
from QM (CN1/F226), no intrinsic-decoherence floor (CN2/F227), $\lambda_6$ not reducible / lepton
spectrum a one-angle fit (CN3/F179), democratic class excluded (CN4/F108), no native massive
spin-2 (CN5/F216), $\nu_R\nu_R$ tensor channel no-go (CN6/F223).

> The ledger note "highest F245" and its 2026-07-02 audit date **lag** the current
> frontier (F245/F246 landed 2026-07-15, closing L1 and L2). Rerun the Master Audit Prompt
> (`docs/roadmaps/open-derivations-prompts*.md`) to refresh the ledger, then rerun `/project-audit`.

---

## 7. Papers

Active series of 12 (`papers/`, reading order in `papers/README.md`); Paper VIII (Dielectric
Black Hole) was deprecated after the F178 gravity decision and IX–XIII renumbered VIII–XII:

I Base Structure · II Photon · III Higgs-Free Mass · IV Electromagnetism · V Strong Force ·
VI Weak Force · VII Gravity · VIII Fermion Sector · IX Lepton Sector · X Baryon Sector ·
XI Unification (Rotation Currency) · XII Koide Angle.

Plus `Claims-and-Falsifiers-Summary.md`, an applied note (EHD ionocraft efficiency), and
outreach drafts. PDFs are regenerated via pandoc/xelatex in `papers/pdf/`.

---

## 8. How to rerun this audit

Run `/project-audit` (`.claude/commands/project-audit.md`) — it regenerates the indexes, reads
the live ledgers, fans out module/test sub-agents, overwrites this guide, verifies against the
sources, and records a changelog entry. The methodology and a copy-pasteable prompt (for
sessions without the slash command) live in `docs/audits/project-audit-prompt.md`. Keep the
section headings above stable across reruns so each refresh is a meaningful `git diff`.
