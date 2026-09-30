# Audit — why photon↔fermion momentum conservation is not operating, and whether a different derivation path exists

*2026-09-16 - 11:10 · sector `gauge`/`core` · scope: the F384→F390 chain · **not a finding** — no finding number spent, no test record, no gate run (the sandbox shell on the work machine was unavailable this session, so `make gate` and `casim test` could not be executed). Every number below is reproduced by `tools/verify_photon_momentum_diagnosis.py`, which re-implements the relevant casim functions from their own source and needs no casim import.*

**Status:** investigation complete on the diagnosis; **partial** on the replacement derivation (§7 states exactly what was and was not demonstrated).

---

## 0. The short answer

Ben's read is correct, and the reason is more elementary — and more fixable — than F389 §4's structural argument suggests.

F389 §4 concluded that exact momentum conservation fails because the two channels are "two separately-derived, separately-audited numerical prescriptions, bridged together, not two halves of one single gauge-invariant lattice action." That conclusion is right, and §6 below sharpens it. But it is not the *leading* cause of what F390 measured. Two more elementary defects sit underneath it, and both are proven here to machine precision:

1. **The beam in F390's scenario carries exactly zero field momentum.** `photon.build_beam_packet` places `E` and `B` in the *same* Cartesian component, so `E ∥ B` pointwise and `E×B ≡ 0` — measured `0.000e+00`, identically, not a small number. F390's momentum-conservation test was run against a field that had no momentum to give. **The engine already knew this**: `core.observers.Momentum`'s own docstring says so in as many words and names the fix. The warning was written in Stage 0 and not carried into Stage 5.

2. **`charge_coupling.bcc_curl_symbol` is not the symbol of a curl.** It fails the defining identity `curl(grad φ) = 0` maximally (`|C×G|/(|C||G|)`: max `1.000000`, mean `0.742`; a true curl gives exactly `0`). Its `k→0` limit is `C ∝ R k` with `R = diag(1,−1,1)` — a parity reflection inherited from the fermion walk's spin-quantisation axis. On the coordinate axes the reflection is exact at *every* grid mode: `Ĉ = +k̂` on x and z, `Ĉ = −k̂` on y. F390 §3 named its axis breakdown's mechanism "likely, not proven here"; the reflection itself is now proven exactly, and it predicts the specific three-way asymmetry F390 measured (§3.4). The end-to-end causal chain from the reflection to F390's cosines is a strong inference, not a re-run of the coupled scenario — that re-run is step 2 of §8.

Neither defect requires the deeper action-principle reconstruction to fix. Fixing them is a prerequisite to *asking* the momentum question meaningfully — until then, F390's cosines are measurements of an artifact.

A third conclusion, conceptual rather than numerical, follows in §6: **the roadmap's claim 1 as written is not achievable by any scheme.** A lattice has only discrete translation symmetry, so there is no exactly conserved continuum-style momentum to find. What *can* be made exact is stated in §6.2, and it is a better target.

---

## 1. What F389 and F390 actually measured

| Finding | Reported | What it was measuring |
|---|---|---|
| F388 §2 | `‖J_T‖/‖J‖ = 2.1×10⁻¹⁶` to `2.4×10⁻¹⁶`, five configurations | F384's current is longitudinal **by construction**, so the loop cannot radiate |
| F389 §3 | `‖ΔP_field‖ = 2.25×10⁻⁴` (was `5.1×10⁻³⁶`) | the added transverse current does source *something* |
| F389 §4 | `ΔP_matter ~ O(g)`, `ΔP_field ~ O(g²)`; doubling ratios `1.99–2.00` and `3.99–4.01` | an order mismatch between the two channels |
| F390 §2 | `cos(ΔP_matter, ΔP_field) = −0.989`; residual `0.174` | on-axis, with a **zero-momentum beam** (§2) |
| F390 §3 | same cosine `= +0.99995` for `axis=1` | the y-axis reflection (§3) |
| F390 §3 | direction correlation reverses at `m_index=4` | not explained by either defect; still open (§8) |

F390's own §3 already retracted the generality of its positive results after review. This audit explains *why* they were never general, and the explanation is not the one F390 offered as "likely."

---

## 2. Defect 1 — the beam has no momentum to give

`gauge/photon.py:342`, `build_beam_packet`, builds the Riemann–Silberstein analytic field `F = E + iB` from a **scalar** envelope times a **single real** polarization vector:

```python
E[pol_axis] = F.real
B[pol_axis] = F.imag
```

Both `E` and `B` live in the one component `pol_axis`. So `E ∥ B` at every site, and the Poynting momentum density `E×B` vanishes pointwise.

Measured (`L=16`, `σ=3.0`, the finding's own defaults), for every axis and both `m_index` values F390 used:

| axis | pol | m | max\|E×B\| pointwise | \|Σ E×B\| | field energy |
|---|---|---|---|---|---|
| 0 | 1 | 2 | `0.000e+00` | `0.000e+00` | `12.2577` |
| 0 | 1 | 4 | `0.000e+00` | `0.000e+00` | `12.2577` |
| 1 | 2 | 2 | `0.000e+00` | `0.000e+00` | `12.2577` |
| 2 | 0 | 2 | `0.000e+00` | `0.000e+00` | `12.2577` |

Exactly zero — not a noise floor. After the `Ĉ(k)`-transverse projection F388/F390 apply before injection, the beam's momentum is still only machine noise (`7×10⁻¹⁷` to `1.8×10⁻¹⁵`, with `cos(P, k̂)` between `−0.019` and `+0.007`, i.e. no direction at all).

**Consequence for F390.** `‖ΔP_field‖ = 0.037` in F390's run cannot be beam depletion, because the beam's momentum is zero at every tick. It is entirely the *new* field that F389's radiative current sources from the fermion. So the scenario has a matter packet gaining momentum and a field gaining momentum, with nothing losing any. `ΔP_matter + ΔP_field` was never going to approach zero; the residual `0.174` is not a near-miss, and the local minimum at `g_lat ≈ 0.6` that F390 §4 correctly identified as structurally guaranteed is a crossing of two independently-growing curves, exactly as that section says.

**This was already documented.** `core/observers.py`, `Momentum`'s docstring, Stage 0:

> The single-component `build_beam_packet` construction (E and B sharing one Cartesian axis, the RS-analytic-signal `F=E+iB` embedding) has `E∥B` pointwise and so carries **zero** field momentum by construction — a real limitation of that helper for this purpose, not of this formula; use `build_pair_mode` (or any genuinely transverse two-axis construction) when a nonzero `P_field` baseline is wanted.

F390 used `build_beam_packet`. The caveat existed one module away and did not travel.

### 2.1 The fix, derived and verified

In Riemann–Silberstein language — which is the model's own chosen language (decision 5, the De Broglie composite photon) — a genuine *radiation* field is a **null** RS field: `F·F = E² − B² + 2i E·B = 0`, i.e. `|E| = |B|` **and** `E ⊥ B`. `build_beam_packet` produces `F = (scalar) · ê` with `ê` a real unit vector, so `F·F = (scalar)² ≠ 0`. It is not a null field, which is the precise statement of the defect.

The fix is one line: make the polarization the **complex circular** vector `ê = (ê₁ + i ê₂)/√2`, so that `E = Re F` and `B = Im F` are automatically orthogonal and equal in magnitude. Measured:

| axis | m | \|Σ E×B\| | cos(P, k̂) | E·B/(\|E\|\|B\|) | \|E_L\|/\|E\| |
|---|---|---|---|---|---|
| 0 | 2 | `75.1260` | `+1.000000` | `+1.8×10⁻¹⁷` | `0.2741` |
| 0 | 4 | `75.1260` | `+1.000000` | `+2.6×10⁻³³` | `0.1395` |
| 1 | 2 | `75.1260` | `+1.000000` | `−2.7×10⁻¹⁸` | `0.2741` |
| 2 | 4 | `75.1260` | `+1.000000` | `+2.1×10⁻³⁵` | `0.1395` |

The momentum is now `O(1)`, points **exactly** along the beam axis (`cos = +1.000000`) for every axis and both carrier modes, and is conserved by casim's **own** free propagator `photon_step_spectral` to `4.4×10⁻¹⁵` relative over 40 ticks. `build_pair_mode`, which already does this correctly, conserves to `9.7×10⁻¹⁵`.

Note what this settles: **the photon sector's propagator and momentum observable are both sound.** `Σ_x E×B` is exactly conserved by `photon_step_spectral` — mode by mode, because that step rotates `(E_k[a], B_k[a])` by the same angle for each Cartesian component `a`, and `Re[E_k × B_k*]` is invariant under that rotation. The defect is confined to one test helper.

Note also what it does *not* fix: the `Ĉ(k)`-longitudinal leakage is essentially unchanged (`0.2755` for the current helper, `0.2741` for the fixed one, at `m=2`), because that comes from defect 2 and is independent of the polarization structure.

---

## 3. Defect 2 — the curl symbol is not a curl

`charge_coupling.bcc_curl_symbol` builds its vector from `_bcc_uvec(k/2)`'s `n⁺`, the **fermion walk's spin-quantisation axis**. `bcc_spin_axis`'s own docstring states the limit `n̂ → (k_x, −k_y, k_z)/|k|` and calls the y-sign flip "an intrinsic chirality convention of the Bisio BCC walk." F387 §1 established that `bcc_curl_symbol` inherits that sign, and measured the three resulting angles. This audit identifies what the inherited object actually is.

### 3.1 It is a reflection of k, not k

`C_odd(k) → R k/√3` as `k→0`, with `R = diag(1,−1,1)`. That single statement reproduces all three of F387's measured angles exactly:

| direction | angle(`R k`, `k`) | F387 measured |
|---|---|---|
| cubic axis `(1,0,0)` | `0.000000°` | `0.000000°` |
| face diagonal `(1,1,0)` | `90.000000°` | `90.000000°` |
| body diagonal `(1,1,1)` | `70.528779°` | `70.528779°` |

Away from `k→0` it is not globally a reflection either — `cos(C, k)` ranges over the full `[−1, +1]`, and `3864` of `4088` nonzero modes at `L=16` have `cos(C,k) < 0.99`.

### 3.2 It fails the defining identity of a curl

A curl operator must satisfy `∇×∇φ = 0` for every scalar `φ`. In symbols, with `G` the gradient symbol, that is `C × G = 0`, which requires `C ∥ G`. Since `G ∝ k` (spectral) or `G_j = e^{ik_j}−1` (forward difference), and `C ∝ R k`, it fails:

| gradient symbol | `\|C×G\|/(\|C\|\|G\|)` max | mean |
|---|---|---|
| spectral, `G = k` | `1.000000` | `0.741692` |
| forward difference, `G_j = e^{ik_j}−1` | `1.000000` | `0.707173` |
| **control — a true curl, `C = k`** | **`0.000e+00`** | — |

This is not a small discretisation error. On average the "curl of a gradient" is 74% of its maximum possible magnitude.

### 3.3 Why 300 findings did not catch it

Discrete exterior calculus gives two identities, both consequences of `d∘d = 0`:

- `div(curl A) = 0` — in symbol form `C·(C×A) = 0`. **This holds for any vector field `C` whatsoever.** It is a property of the cross product, not of `C`. `bcc_curl_symbol`'s own docstring cites it ("the identity `C_odd·(C_odd×x) ≡ 0` intact") as evidence of correctness. It carries no information.
- `curl(grad φ) = 0` — `C×G = 0`. **This is the one that constrains `C`.** It was never tested.

The model's no-monopole gate (`iĈ·B ≈ 0`, F387's `split_sourcing_preserves_no_monopole`, F388's `no_monopole_fix_holds_with_dynamical_current`, F389's `no_monopole_holds`) tests exactly the vacuous identity. That is why it has been green throughout, and why F387's split-sourcing fix genuinely works while resting on a defective yardstick.

### 3.4 This is the mechanism of F390's axis inversion

On the coordinate axes the reflection is exact at **every** grid mode, not just `k→0`:

| axis | m = 1, 2, 3, 4 | `Ĉ · k̂` | `Ĉ` |
|---|---|---|---|
| x | all | `+1.000000000` | `(1, 0, 0)` |
| y | all | `−1.000000000` | `(0, −1, 0)` |
| z | all | `+1.000000000` | `(0, 0, 1)` |

A y-propagating beam has its rotation generator **exactly reversed**. Everything the sourcing machinery derives from `Ĉ` — transversality, the Gauss solve, the published `A` — runs backwards for that beam. F390 measured `cos(ΔP_matter, ΔP_field)` flipping from `−0.989` (axis 0) to `+0.99995` (axis 1) — a sign reversal, on exactly the one axis where the generator is reversed. The reflection is proven here; that it is what produces that particular cosine flip is inference from the two facts sitting on the same axis, not a re-run of the coupled scenario.

It also explains why F390's three axes behaved as *three* different cases rather than two. `build_beam_packet`'s default `pol_axis = (axis+1) % 3` puts each beam in a different relation to the reflected (y) axis:

- `axis=0`: propagation on x, **polarization on y** — the flipped axis carries the field
- `axis=1`: **propagation on y** — the flipped axis carries the wavevector
- `axis=2`: propagation on z, polarization on x — neither is flipped

Three distinct geometries, three distinct results. F390 reported `cos(ΔP_matter, k̂_beam) = +0.995` (axis 0), `−0.0019` (axis 1) and `−0.0093` (axis 2) — an asymmetry that no account treating the three axes as equivalent can explain, and that this one predicts.

### 3.5 What is *not* explained

The `m_index=4` sign reversal on the x-axis (F390 §3, `cos = −0.988`) is **not** explained by either defect. `Ĉ = +k̂` exactly at `m=4` on x, and the RS-corrected beam gives `cos(P, k̂) = +1.000000` at `m=4` on every axis. So the `m`-dependence is not a photon-sector property at all: it lives in the matter-side coupling (the per-link step, or the `A` published from `B`). Left open; see §8.

---

## 4. Which of F384–F390 this touches

| Finding | Effect |
|---|---|
| **F384** | Unaffected as an algebraic construction — it solves continuity against `Ĉ` correctly. But "the transverse part is free, unconstrained gauge freedom" is a consequence of *defining the current by solving continuity*; §6 shows that framing is itself the avoidable step. |
| **F385** | Unaffected. The per-link Peierls step is the one piece of the chain that is already action-shaped (§6.3). |
| **F386** | The published `A` inherits defect 2 through `solve_A_coulomb_3d`. |
| **F387** | Its measurements are all correct and independently reproduced here. Its §1 identified the anisotropy and asked whether it needed a code fix, answering "no" on the grounds that every consumer measures against `Ĉ` consistently. That reasoning is sound *internally* and breaks at the boundary: the momentum observable `Σ E×B` and the Poynting geometry are Euclidean, not `Ĉ`-based. The two conventions meet, unreconciled, exactly at the momentum question. |
| **F388** | §2 is correct and is the most valuable single paragraph in the chain. |
| **F389** | The construction is correct. §4's diagnosis is correct and is sharpened, not contradicted, by §6 below. |
| **F390** | Claims 1 and 2 rest on a zero-momentum beam. The measurements are real; their interpretation as momentum exchange is not supported. The finding's own §3 and §4 already stop short of claiming exchange, which is why this audit narrows rather than overturns it. |

Nothing here disturbs the photon propagator (decision 5), `Ω_pair`, the `c_lat` results, or any magnitude-only check — F387 §1 already established that squaring removes the sign, so every `|C|`-based result is untouched.

---

## 5. External research review

Full review with sources: `references/lattice-conservation-laws-research-review.md`. The four results that bear directly:

1. **Exact lattice gauge invariance gives exact current conservation.** In Wilson-type lattice gauge theory the gauge field is a set of compact link variables and the action is invariant under local phase rotations *at finite lattice spacing* — not only in the continuum limit. The resulting lattice Ward–Takahashi identity **is** the discrete continuity equation. The current is never constructed to satisfy continuity; it is `∂S/∂A_link`, and continuity is a theorem. This removes F384's free-transverse-sector problem at the root rather than patching it.

2. **Discrete exterior calculus gives both `d∘d = 0` identities by construction.** Fields become cochains: `φ` on sites (0-form), `A`, `E` on bonds (1-forms), `B` on plaquettes (2-form). `B = dA` is literally the oriented sum of `A` around a plaquette — which is exactly the Peierls holonomy F385 already computes. Both `curl∘grad = 0` and `div∘curl = 0` then hold identically, with no borrowed spin axis and no reflection. **The repo already does this correctly in 2D**: `charge_coupling.discrete_curl_z` and `discrete_div`, whose docstring says "chosen as the adjoint partner of `discrete_curl_z` so that `div∘curl ≡ 0`." The 3D BCC path abandoned that construction for the spectral `bcc_curl_symbol`. The fix is to extend existing, correct code — not to invent anything.

3. **Variational / multisymplectic integrators preserve discrete momentum maps exactly.** A scheme derived as the discrete Euler–Lagrange equations of *one* discrete action preserves the momentum map of any symmetry of that action, exactly and for any timestep. An operator-splitting scheme that bridges two separately-derived prescriptions has no action, hence no functional whose symmetry could produce a conservation law. This is the precise technical content of F389 §4's diagnosis.

4. **On a lattice the conserved quantity is crystal momentum, not momentum.** Discrete translation symmetry is a discrete group; Noether's theorem needs a continuous one. What survives is quasi-momentum, conserved **modulo reciprocal lattice vectors** (Umklapp). §6.2 draws the consequence.

Two obstructions worth knowing before committing to the single-action route:

- **Nielsen–Ninomiya.** A single Weyl species cannot be put on a lattice with exact chiral gauge invariance, locality and no doublers. The chain is coupling U(1) to a single Weyl 2-spinor, so this is live, not academic. It is not a blocker for a *vector-like* (Dirac) U(1) — which is what electromagnetism is — but it means the clean route runs through the Dirac sector, and the Weyl-only scope that F384–F390 all declare is exactly the scope where the theorem bites.
- **Ginsparg–Wilson.** The standard resolution: exact (modified) chiral symmetry at finite lattice spacing, at the cost of a non-ultralocal operator. Worth knowing as the escape hatch; expensive.

---

## 6. The different path

### 6.1 One action, two variations

Replace the bridge with a single discrete action in `ψ` and compact link variables `U_{x,d} = e^{i q a A_d(x)}` on the BCC hop links:

$$S \;=\; \sum_t \Big( S_\text{matter}[\psi_t, \psi_{t+1}, U_t] \;+\; S_\text{gauge}[U_t, U_{t+1}] \Big)$$

with `S_matter` the model's own BCC walk kernel decorated with F385's Peierls phases, and `S_gauge` a Wilson-type plaquette action on the BCC's own plaquettes. Then:

- `δS/δψ̄` → the fermion step. This is F385 fork (a), essentially unchanged.
- `δS/δU_{x,d}` → the field equation, **with the current as its source, read off rather than chosen.**
- Local gauge invariance of `S` (`ψ_x → e^{iθ_x}ψ_x`, `U_{x,d} → e^{iθ_x}U_{x,d}e^{−iθ_{x+d}}`) → a lattice Ward identity that **is** discrete charge conservation.

What disappears: F384's minimal-solution construction, its undetermined transverse sector, F388 §2's inability to radiate, and F389's disclosed constitutive choice of *which* transverse field to add. None of them are fixed — they stop being questions.

### 6.2 Restate the target

**The roadmap's claim 1 (`ΔP_matter + ΔP_field ≈ 0`, with `P` the continuum-style functional `Σ_k k|ψ̃|²` + `Σ_x E×B`) cannot be made exact by any scheme on a lattice.** There is no continuous translation symmetry to generate it. This is not a defect of casim; it is what a lattice is.

Three targets that *are* exact, in descending order of how well the single-action route delivers them:

- **(A) Exact charge conservation** — a lattice Ward identity from exact gauge invariance. Delivered outright, verified below at `3.9×10⁻¹⁶`.
- **(B) Exact crystal-momentum conservation** — total quasi-momentum conserved mod reciprocal lattice vectors, which holds whenever the tick map commutes with lattice translation. Checkable as `Φ∘T = T∘Φ` to machine precision. Necessary but *not* discriminating: casim's bridged scheme is translation-covariant too, so this alone does not separate the schemes.
- **(C) Matched-order approach to the continuum** — `ΔP_total = O(a^n)` with **the same order in the coupling on both channels**. This is the real content of F389 §4: `O(g)` against `O(g²)` is a structural asymmetry, not a discretisation error, and it is what one action removes, because both channels are variations of one functional and cannot have mismatched leading orders.

This restatement is the single most useful output of this audit. Stage 5 has been chasing (C) while measuring it against a bar set by a quantity that does not exist.

### 6.3 What already exists to build on

| Piece needed | Already in the repo |
|---|---|
| Peierls link phases on BCC hops | `minimal_coupling.u1_link_weyl_step_3d_bcc` (F385) |
| DEC curl with both identities | `charge_coupling.discrete_curl_z` / `discrete_div` — **2D only**, needs the 3D BCC extension |
| Wilson plaquette action | `gauge.bcc_action`, `gauge.link_hamiltonian` |
| A correct `E⊥B` photon mode | `photon.build_pair_mode` |
| An exactly-conserving momentum observable | `core.observers.Momentum` (verified sound, §2.1) |

The 3D BCC DEC complex is the one genuinely new object. Everything else is assembly.

---

## 7. Prototype — what was demonstrated and what was not

`tools/verify_single_action_prototype.py` builds a 2+1D lattice QED toy from a single Hamiltonian

$$H = -\kappa \sum_{x,i}\big[\psi^*(x{+}e_i)\,e^{iqA_i(x)}\psi(x) + \text{c.c.}\big] \;+\; \tfrac12\sum E^2 \;+\; \tfrac12\sum B^2,\qquad B = d_1 A$$

on a DEC complex, and compares it head-to-head with a "bridged" scheme of the same shape as F387/F388 (free-rotate, then source from the **transverse part only** of a separately-built current, then step matter on the published `A`). Both use the *same* exact free-field rotation, so the only differences are the two choices casim actually made.

**Established, to machine precision:**

| Check | Measured | casim comparison |
|---|---|---|
| `curl(grad φ) = 0` | `8.9×10⁻¹⁶` | `bcc_curl_symbol`: max `1.000000`, mean `0.742` |
| `div(curl* B) = 0` | `8.9×10⁻¹⁶` | holds (vacuously) |
| continuity as a **consequence** of `J = ∂H/∂A` | `3.9×10⁻¹⁶` | F384 imposes it by construction |
| transverse (radiative) fraction of the derived current | **`0.7367`** | F388: `2.1×10⁻¹⁶` to `2.4×10⁻¹⁶` |
| `Σ E×B` conserved by the free propagator | `1.8×10⁻¹⁴` over 400 ticks | (casim's is also exactly conserved, §2.1) |
| **Gauss-law drift, full derived current** | **`4.7×10⁻⁵`** | — |
| **Gauss-law drift, transverse-only source** | **`5.5×10⁻²`** | — |

The last two are a clean, physical discriminator and the prototype's strongest coupled result: sourcing only the transverse part of the current breaks the lattice Gauss law by a factor of **~1150**, because the longitudinal part of `J` is precisely what keeps `div E − qρ` static. F387's split recipe substitutes a separate algebraic Gauss solve for that mechanism; whether the substitution is equivalent has never been tested, and this says it is not obviously so.

The transverse-fraction row is the central result: **the same physical setup that gives casim a current incapable of radiating gives a derived current that is 74% radiative, with nothing added and nothing chosen.**

**Not established.** The prototype does **not** demonstrate exact coupled momentum conservation, and the seeded-beam configuration did not show a clean exchange (`cos(ΔP_m, ΔP_f)` ran `−0.06` to `+0.61` rather than approaching `−1`). Two reasons, both identified and both honest:

- The prototype's `H` omits the scalar-potential/Coulomb term, so the longitudinal sector of `E` carries energy and momentum that never couples back to matter. The system is therefore not closed, and no conservation argument applies to it. Fixing this means adding `A₀` and a constrained (Gauss-law-preserving) integrator — a bigger build than one session.
- Per §6.2, the quantity being measured has no exact conservation law on a lattice regardless. The prototype was aimed at the wrong target for the same reason Stage 5 was.

The self-sourced configuration was **degenerate and its numbers should be ignored**: a real Gaussian `ψ` at rest with `A = 0` has `J = 2κq·Im[ψ^*(x{+}e)e^{iqA}ψ(x)] ≡ 0` exactly, so nothing was sourced and both schemes returned `~10⁻¹⁶` noise. Re-running that comparison needs a complex (moving or chirped) initial packet.

---

## 8. Recommended program

In dependency order. Steps 1–2 are small and unblock the rest.

1. **Fix `build_beam_packet`** (§2.1) — complex circular polarization, or a `null=True` option to preserve the existing helper. One line plus a test. Add a gate leg asserting `|Σ E×B| > 0` and `cos(P, k̂) > 0.99` for any beam a momentum test uses. *This is the single highest-value change in the list.*
2. **Re-run F390's scenario against the fixed beam**, before doing anything structural. Every one of its four claims should be re-measured; the cosines will change, and it is not knowable in advance by how much. This may also resolve the `m_index=4` anomaly (§3.5), which is currently unexplained and should not be theorised about before the beam is fixed.
3. **Add the missing curl test to the gate.** `|C×G|/(|C||G|)` against both gradient symbols, with `C = k` as the control. It is three lines and it is the check whose absence let defect 2 persist. Do this even if `bcc_curl_symbol` is kept — a known-failing gated leg is infinitely better than an untested assumption.
4. **Build the 3D BCC DEC complex** — sites, bonds, plaquettes, cells with `d0`, `d1`, `d2` and their adjoints, extending `discrete_curl_z`/`discrete_div` from 2D. Gate both `d∘d = 0` identities. This is the one genuinely new object §6.3 identifies.
5. **Derive the current as `∂S/∂A`** on that complex and verify continuity as a consequence (the prototype's `3.9×10⁻¹⁶` result, transplanted to BCC). This supersedes F384's construction rather than amending it.
6. **Restate the roadmap's Stage 5 claim** per §6.2 — (A) exact, (B) exact and gated, (C) measured with matched orders. The current claim 1 should be withdrawn as unachievable rather than left open.
7. **Decide the Weyl-vs-Dirac question** (§5). The single-action route is clean for a vector-like U(1); the Weyl-only scope F384–F390 all declare is where Nielsen–Ninomiya bites. This should be settled before step 4, because it may change what `S_matter` is.

---

## 9. Caveats

- **No gate was run.** The sandbox shell on the work machine was unavailable this session, so nothing here has been through `make gate`, `casim test`, or the finding-review pass. Every number is reproducible from `tools/verify_photon_momentum_diagnosis.py`, which re-implements the relevant casim functions from their own source rather than importing them — so a transcription error in that re-implementation is a live risk, and the first thing a follow-up session should do is re-run the same checks against the real modules.
- **Defect 2 is diagnosed, not repaired.** This audit does not propose that `bcc_curl_symbol` be changed in place. It is load-bearing for a large amount of existing work, every magnitude-only result built on it is untouched, and F387 §1's argument that its consumers are internally consistent is correct as far as it goes. What is established is that it is not a curl and that the boundary where that matters is the momentum observable. Deciding what to do about it is a research session of its own.
- **§3.5's `m_index=4` anomaly is unexplained.** It is not defect 1, not defect 2, and not a photon-sector property. It should be re-measured after step 1, not theorised about now.
- **The prototype is 2+1D with a single-component matter field**, not a BCC Weyl spinor. Its structural results (the two `d∘d` identities, current-as-`∂H/∂A`, continuity as a consequence, the Gauss-law discriminator) are dimension-independent and transfer. Its *numbers* do not, and the coupled-momentum results are explicitly not established (§7).
- **§7's Gauss-drift factor of ~1150 compares the prototype's own two schemes**, not casim's actual recipe. F387's split recipe carries the longitudinal sector via a separate algebraic Gauss solve, which the prototype's bridged scheme does not implement. The comparison establishes that the transverse-only source term alone cannot maintain Gauss's law; it does not establish that F387's full recipe fails to. That is a distinct check and is worth running.
- **The external review (§5) leans on search results and standard textbook results**; per-paper verification was limited this session because the fetch tool hit a session cap. The four load-bearing statements are standard and long-established, but specific attributions in `references/lattice-conservation-laws-research-review.md` should be confirmed against the primary sources before anything cites them.
- Only the Weyl 2-spinor / U(1) sector is examined, matching F384–F390's own declared scope.

**Test record:** none — `analysis-only` plus two standalone verification scripts; no registry record is claimed and no gate leg is added by this document.
**Claim:** none — this is an audit of existing engine constructions and a proposed derivation route, not an assertion against established physics; no `docs/claims/` card is issued per D12's bar. It does bear on **CL307**, whose narrowed status rests on F390's cosines: §2 shows those were measured against a zero-momentum beam, so the card should be re-examined after step 2, not before.

**Cross-references:** [[F390-photon-fermion-push-scenario]], [[F389-radiative-transverse-em-current]], [[F388-fermion-photon-coupled-channels]], [[F387-curl-anisotropy-omega-pair-mismatch]], [[F386-a-field-convention]], [[F385-u1-link-covariant-step]], [[F384-conserved-bcc-em-current]], [[F344-bcc-walk-point-symmetry-d4h]], [[F87-charge-coupling-paired-photon]].
