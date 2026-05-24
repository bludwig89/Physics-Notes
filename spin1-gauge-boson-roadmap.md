# Roadmap — Elementary Spin-1 U(1) Gauge-Boson Photon (Standard-Model route)

*Drafted 2026-05-23 - 18:15.*

*Decision premise (set with the user 2026-05-23): build the Standard-Model elementary spin-1 photon as a **parallel fork**, not a replacement — the verified composite-photon results (F17, F20, F25, F26; Exactness Inventory Tier 1 #7–9, #22–30) stay intact and become the head-to-head baseline. Scope runs through **U(1) minimal coupling to the Dirac current** (closing the source-coupling gap, Mohr §C6 / Test V4), stopping before a full self-consistent QED loop except as a stretch phase.*

*Sources grounding this plan: `ca-simulation/ca_maxwell.py` (composite sector), `ca-simulation/ca_dirac.py` Phase E1 (existing external U(1) coupling, lines 377–418, 1028+), `reference-research/qca-papers-1-4-overview.md` (Test V4, the "external classical A_μ" gap), `reference-research/mohr-2010-maxwell-photon-wf-summary.md` §C2/§C6, `mohr-c5-c6-build-plan.md` (C6 source-coupling primitives already specced), `reference-research/ca-electroweak-design.md` Path C, `exactness-inventory.md` tiers.*

---

## 1. The two photons, side by side

The question is what the photon **is**. The model currently answers with the de Broglie composite; the Standard Model answers with an elementary gauge connection. Everything downstream follows from that one choice.

| Aspect | Current — composite (de Broglie) | Proposed fork — elementary spin-1 (SM) |
|---|---|---|
| Ontology | Bilinear of two Weyl spin-½ fields, $G^i=\varphi^T\sigma^i\psi$ | Fundamental vector field $A_\mu(x)$ / link variables $U_\mu(x)$ |
| Where spin-1 comes from | *Emerges* from product of two spin-½ | *Postulated* as the field's representation |
| Primitive object | $\mathbf E_G,\mathbf B_G$ (fields are derived) | $A_\mu$ (potential is primitive; $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$) |
| Gauge invariance | Absent / not fundamental | **Fundamental and exact** — defines the theory |
| Substrate | Rides the existing BCC Weyl QCA | A **second** field type with its own lattice DOF |
| Masslessness | Structural (no Yukawa term) | Protected by symmetry (Ward identity forbids $m^2A_\mu A^\mu$) |
| Statistics | Bose only *approximately* (Paper 4 smearing $f_\mathbf{k}$) | Manifestly, exactly bosonic |
| Coupling to matter | None — photon is source-free; U(1) is an **external classical phase** (Phase E1) | Minimal coupling $D_\mu=\partial_\mu-iqA_\mu$; sourced by $J^\mu=\bar\psi\gamma^\mu\psi$ |
| Transversality | Automatic ($2\tilde{\mathbf n}\cdot\mathbf E_G=0$, Tier 1 #8) | Must be **imposed** — Gauss-law constraint + gauge fixing |
| Light speed | $c_\text{lat}=1/\sqrt d$ forced by BCC uniqueness (Tier 1 #9) | Set by the gauge action normalisation (a free choice; pick to match for comparison) |
| Geometric reading | $c$ = real $(\mathbf E,\mathbf B)$ rotation rate; $i$ = linearisation artifact (F25/F26) | Standard phase-velocity picture; no rotation reinterpretation for free |

### What stays identical either way
The Dirac/Weyl matter sector (`ca_dirac.py`, `ca_bcc.py`), the BCC lattice itself, the split-step unitary methodology, and the exactness-tier discipline are all unchanged. The fork touches only the electromagnetic sector and the one coupling term that joins it to matter.

---

## 2. What you gain, what you pay

This is the crux — worth stating plainly before any code.

**Gains.** (1) Exact, fundamental U(1) gauge invariance, and with it a Ward identity and exact charge conservation from a symmetry rather than by hand. (2) A *principled* coupling to the Dirac current — this is the whole reason to do it; it directly closes the largest open gap in the model (the photon is currently source-free; `qca-papers-1-4-overview.md` calls the missing Maxwell-matter coupling "the single largest architectural gap," and Mohr §C6 lists source coupling as unbuilt). (3) Real electromagnetism becomes accessible: the static Coulomb force between two charges, and radiation from an accelerated charge — neither of which the composite photon can currently produce. (4) Manifestly exact Bose statistics, removing Paper 4's approximate-smearing caveat (`ca-electroweak-design.md` honest-caveat 3). (5) The longitudinal/Coulomb sector is native to $A_\mu$, rather than bolted on (the composite needed Mohr §C2's `longitudinal_mode` added separately). (6) Immediate contact with the entire validated corpus of lattice gauge theory (Wilson 1974; Kogut–Susskind 1975) for cross-checks.

**Costs.** (1) **Ontological economy is the real price.** The composite photon keeps the model close to its founding thesis — *one* Weyl substrate, everything else emergent. Introducing a fundamental $A_\mu$ is a second, independent field type, a genuine step away from "the universe is one automaton rule." This is the strategic cost, and it is larger than any of the engineering ones. (2) You forfeit the F25/F26 interpretation for free — $c$-as-rotation-rate and "$i$ is a linearised real rotation" are properties of the bilinear, not of $A_\mu$. (3) The composite sector's machine-precision results (transversality, dispersion, Poynting conservation, boost covariance) don't transfer; the elementary field needs its *own* exactness ledger re-derived from scratch. (4) New machinery the composite never required: gauge fixing, a Gauss-law constraint that must be preserved every step, link variables, a plaquette action. (5) Keeping the project's machine-precision-**unitarity** standard is harder — a naïve Yee/leapfrog Maxwell stepper is not QCA-unitary; you need a Hamiltonian (Kogut–Susskind) formulation or a bespoke unitary split-step.

The honest framing: the composite route is the more *original and economical* physics; the elementary route is the more *complete and conventional* physics. The fork lets you measure exactly what the extra field buys before committing the ontology.

---

## 3. Architecture of the fork

Following the project's fork convention (`<topic>_fork_<variant>.py` + a `<topic>_fork_harness.py` in `ca-simulation/forks/`, as with the `curl_fork_*` and `gr3_fork_*` families):

- **`ca-simulation/ca_gauge_u1.py`** — the elementary photon sector. Gauge field as **link variables** $U_\mu(x)=\exp(iqa\,A_\mu(x))$ on BCC links, field strength from plaquettes, a unitary Maxwell stepper, gauge fixing, and the Gauss-law constraint machinery. This is the structural sibling of `ca_maxwell.py`.
- **`ca-simulation/forks/gauge_fork_harness.py`** — runs `ca_maxwell` (composite) and `ca_gauge_u1` (elementary) through *identical* diagnostics (dispersion, transversality/Gauss, energy conservation, real-space group velocity) and tabulates them head-to-head.
- **`ca_dirac.py` (extend in place)** — finish the Peierls-phase covariant hopping that Phase E1 already stubs out (lines ~384, ~408: "proper Peierls phases … would require Peierls phases on the QCA hopping links"). The minimal-coupling scaffold (`∂_μ → ∂_μ − iqA_μ`, static-$A_0$ half-step phase) is already present; G2 completes it for a *dynamical, link-valued* $A$.
- **`model-tests/run_gauge_fork.py`** — driver that emits a Claude-readable result JSON/markdown (per CLAUDE.md, since coupled runs may exceed the 90 s sandbox budget).

Why link variables rather than a bare $A_\mu$ field: link variables make gauge covariance exact and bit-for-bit, preserve the project's unitarity standard, reuse the *same* half-step-phase pattern Phase E1 already validated for Aharonov–Bohm (Tier 1 #14), and are the standard lattice-gauge object with known continuum limits to validate against.

---

## 4. Phased plan

Phases are labelled **G-G\*** (Gauge) to sit alongside the existing V-gates and F-findings. Each lists a build, gate tests, and an exactness target stated in the inventory's tier language (Tier 1 = exact algebraic; Tier 2 = machine precision; Tier 3 = quantitative).

### G0 — Ontology decision doc *(this file)*
Lay out the head-to-head and the success criteria below. No code. **Exit:** user agrees the fork is worth building and on the $c_\text{lat}$-matching convention (§5).

### G1 — Free elementary photon on the BCC lattice
**Build.** $A_i$ link variables with conjugate electric field $E_i$ (Kogut–Susskind Hamiltonian form, which gives a clean unitary stepper and a natural Gauss law); $F_{\mu\nu}$ from plaquettes; free Maxwell EOM $\partial_\mu F^{\mu\nu}=0$; Coulomb-gauge fixing (or gauge-invariant $\mathbf E,\mathbf B$ observables only).

**Gate tests.**

- **G1-disp** — dispersion $\omega(\mathbf k)=c\,|\mathbf k|$ with exactly **2** transverse physical polarisations. *Target: machine precision (Tier 2);* compare to composite $|\mathbf k|/\sqrt3$ (#9).
- **G1-gauss** — Gauss-law constraint $\nabla\!\cdot\!\mathbf E=0$ preserved under evolution. *Target: machine precision.* This is the elementary analog of composite transversality (#8) — but here it is a *constraint to maintain*, not an identity that holds for free.
- **G1-gaugeinv** — physical observables invariant under $A_\mu\to A_\mu+\partial_\mu\lambda$. *Target: Tier 1 exact algebraic* (bit-for-bit with link variables). **No composite analog exists** — this is a genuinely new exactness result the gauge route makes available.
- **G1-energy** — $\tfrac12(\|\mathbf E\|^2+\|\mathbf B\|^2)$ conserved. *Target: machine precision;* the analog of F17 (composite Poynting conservation, $4.8\times10^{-14}$/200 steps).
- **G1-prop** — real-space wavepacket group velocity $=c_\text{lat}$. *Target: quantitative (Tier 3);* the analog of F20.

**Exit:** a free elementary photon that propagates, stays transverse, conserves energy, and is provably gauge-invariant.

### G2 — Minimal coupling to the Dirac field *(scope endpoint)*
**Build.** Covariant hopping $\psi(x)\to U_\mu(x)\,\psi(x+\hat\mu)$ — completes the Phase E1 Peierls-phase TODO. Dirac current $J^\mu=\bar\psi\gamma^\mu\psi$ as the source. Gauss law with charge: $\nabla\!\cdot\!\mathbf E=\rho=q\psi^\dagger\psi$.

**Gate tests.**

- **G2-cov** — gauge covariance of the *coupled* Dirac–gauge step: a simultaneous gauge transform of $\psi$ and $U_\mu$ leaves all observables fixed. *Target: Tier 1 exact algebraic.*
- **G2-AB** — Aharonov–Bohm phase pickup with a **dynamical link-valued** $A$ reproduces the existing static-$A_0$ result $\exp(i\oint A)$. *Target: machine precision;* **regression against Tier 1 #14** ($4.4\times10^{-16}$).
- **G2-ward** — current conservation $\partial_\mu J^\mu=0$ on Dirac eigenstates. *Target: machine precision* (FFT floor after the bilinear). This is exactly the `test_current_conservation` primitive already specced in `mohr-c5-c6-build-plan.md` §C6 — reuse it.
- **G2-gauss-src** — sourced Gauss law $\nabla\!\cdot\!\mathbf E=q\psi^\dagger\psi$ holds each step. *Target: machine precision.*

**Exit:** the photon is no longer source-free. This is the deliverable that closes Mohr §C6 / Test V4 — the gap the composite sector cannot close on its own.

### G3 — First genuinely-electromagnetic observables *(stretch)*
**Build/measure.** (a) Static two-charge **Coulomb potential** $V(r)$ from the field of two fixed charges — the lattice-gauge classic; compare to $1/r$ (or the lattice Green function). (b) **Radiation** from an oscillating Dirac current — the practical application Mohr §C6 and the Mohr build plan park under "future Phase G."

**Why it matters.** These are things the composite photon **cannot currently do at all**. G3 is where the elementary field earns its ontological cost — or fails to.

### G4 — Head-to-head & ontology verdict
Run `gauge_fork_harness.py`; tabulate composite vs elementary on every shared diagnostic. Then decide among: (i) elementary becomes canonical; (ii) composite stays canonical, elementary is the "interaction sector"; (iii) **synthesis** — composite as the free-radiation ontology, elementary link variables as the coupling layer, with the hard requirement that they **agree in their overlap** (free transverse propagation) to machine precision or one of them is wrong. The synthesis is the most likely landing given the project's thesis, and it is also the strongest possible self-consistency test.

---

## 5. The one convention to settle first: $c_\text{lat}$ matching

The composite photon has $c_\text{lat}=1/\sqrt3$ *forced* by BCC uniqueness (Tier 1 #9). The elementary gauge field's lattice light-speed is set by the action/Hamiltonian normalisation and is **a free parameter**. For the G1/G4 comparisons to be apples-to-apples, normalise the gauge action so the elementary photon also has $c_\text{lat}=1/\sqrt3$. (Alternative: run both at $c=1$ in their own natural units and compare dimensionless dispersion shape.) This must be agreed at G0 or the dispersion comparison is meaningless.

---

## 6. Exactness ledger — composite result → elementary analog

| Composite (exists) | Elementary analog (to build) | Tier target |
|---|---|---|
| Transversality $2\tilde{\mathbf n}\cdot\mathbf E_G=0$ — Tier 1 #8 | Gauss law $\nabla\!\cdot\!\mathbf E=0$ preserved — **G1-gauss** | Machine precision |
| $c_\text{lat}=1/\sqrt d$ — Tier 1 #9 | Gauge-field dispersion $\omega=c|\mathbf k|$ — **G1-disp** | Machine precision |
| Poynting conservation — F17 / Tier 2 #7,#10 | Field-energy conservation — **G1-energy** | Machine precision |
| U(1) Aharonov–Bohm — Tier 1 #14 | Dynamical-$A$ AB regression — **G2-AB** | Machine precision |
| *(none)* | **Gauge invariance** $A\to A+\partial\lambda$ — **G1-gaugeinv** | **Tier 1 exact** (new) |
| *(none — source-free)* | Current conservation $\partial_\mu J^\mu=0$ — **G2-ward** | Machine precision |
| Boost covariance of $E_G,B_G$ — Tier 1 #25–27 | Boost covariance of $F_{\mu\nu}$ | Machine precision |

The two "none" rows are the point of the exercise: gauge invariance and a conserved matter current are results the composite route structurally cannot produce, and the elementary route gets for (almost) free.

---

## 7. Risks, ranked

1. **Ontological (strategic, not technical).** A fundamental $A_\mu$ dilutes the single-substrate thesis. Mitigation: keep it a fork; let G4 decide; favour the synthesis reading.
2. **Unitarity of the gauge stepper.** Yee/leapfrog is not QCA-unitary. Mitigation: Kogut–Susskind Hamiltonian form or a bespoke unitary split-step; gate on norm conservation before trusting any G1 number.
3. **Gauss-law drift.** The constraint can leak over long runs. Mitigation: constrained (link-variable) formulation makes it exact by construction; monitor as a gate every phase.
4. **Loss of F25/F26.** The rotation interpretation doesn't transfer. Mitigation: none needed if the composite sector is retained (it is) — but note it explicitly so the geometric result isn't quietly orphaned.
5. **$c_\text{lat}$ mismatch** making comparisons meaningless — settled at G0 (§5).
6. **Vector-field lattice artifacts** (photon-doubling analog) on BCC. Mitigation: standard improved-action remedies; flag if G1-disp shows spurious modes.

---

## 8. Bottom line

Adopting the Standard-Model spin-1 gauge boson is not a tweak to the photon — it swaps the photon's *ontology* from "emergent bilinear of the one substrate" to "second fundamental field," and in exchange hands you exact gauge invariance and the principled matter coupling the model currently lacks. The fork costs roughly **G1 (free field) + G2 (coupling)** of build effort to reach a photon that can do what the composite cannot — be sourced by, and act on, charge — while the composite sector keeps every machine-precision result it already owns. The decision the fork is designed to inform is whether closing the source-coupling gap is worth admitting a second field into a theory whose whole appeal is having only one.

---

## Cross-references
- Composite sector & baseline: `ca-simulation/ca_maxwell.py`; Findings F17, F20, F25, F26; Exactness Inventory Tier 1 #7–9, #22–30.
- Existing U(1) coupling scaffold: `ca-simulation/ca_dirac.py` Phase E1 (lines 377–418, 1028+); Tier 1 #14.
- Source-coupling primitives already specced: `mohr-c5-c6-build-plan.md` §C6; `reference-research/mohr-2010-maxwell-photon-wf-summary.md` §C2/§C6.
- The gap this closes: `reference-research/qca-papers-1-4-overview.md` Test V4 ("external classical $A_\mu$" → composite); `reference-research/ca-electroweak-design.md` Path C.
- Fork convention: `ca-simulation/forks/` (`curl_fork_*`, `gr3_fork_*`).
