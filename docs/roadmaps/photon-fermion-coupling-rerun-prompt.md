# Prompt — fix the beam polarization and the curl symbol, then re-run photon↔fermion Stages 0–5

*Paste the block below into a fresh Claude Code session at the repo root. It is written to be standalone.*

---

## READ FIRST, IN THIS ORDER

1. `CLAUDE.md` — especially §Claims (D12), §Building or changing a module, §Concurrency, §Finding coverage.
2. `docs/audits/2026-09-16-photon-fermion-momentum-investigation.md` — **this is the brief.** Everything below implements its §8 program. Read §2, §3, §6.2 and §9 carefully; §9's caveats are load-bearing.
3. `references/lattice-conservation-laws-research-review.md` — §8 (Riemann–Silberstein null condition) justifies Part A; §2 (discrete exterior calculus) justifies Part C.
4. `tools/verify_photon_momentum_diagnosis.py` and `tools/verify_single_action_prototype.py`, plus their saved output in `test-results/`. **Run the first one now** and confirm you reproduce its numbers before changing anything.
5. `docs/roadmaps/photon-fermion-coupling.md` §2 Stages 0–5.
6. `findings/F384`…`F390` (seven files). Do not skip F388 §2, F389 §4, or F390 §3.

**Critical framing.** The audit was written in a session that could not run `make gate` — its verification scripts re-implement casim functions from source rather than importing them. **Your first job is to re-run every one of its checks against the real modules.** If any number disagrees, stop and report; do not build on top of a discrepancy.

## BOOKKEEPING — do this before any research

- Open a claim in `docs/design/session-claims.yaml` (`status: open`, sector `gauge`, one-line topic). No numbers yet.
- `make gate` must be green **before** you start. If it is not, stop and report.
- Take finding numbers one at a time, at write time, from `casim index`'s **NEXT FREE NUMBER** line — never max+1.
- Every finding you write gets the `review-finding` attack-and-fix pass (`.claude/commands/review-finding.md`) before the session ends. No exceptions.
- **Findings are past tense and are never rewritten.** F384–F390 stay as they are. Corrections land as *new* findings plus entries in `docs/theory/supersessions.yaml`. The thing that moves is `docs/claims/CL307`.

---

## PART A — the beam polarization fix

**The defect.** `gauge/photon.py`, `build_beam_packet` (~line 342), sets `E[pol_axis] = F.real` and `B[pol_axis] = F.imag` — both in the *same* Cartesian component. So `E ∥ B` pointwise and `E×B ≡ 0` identically. Confirmed measured `0.000e+00`, every axis, every carrier mode. F390's entire momentum-conservation test ran against a field carrying exactly zero momentum.

`core/observers.py`, `Momentum`'s docstring already states this and names the fix. Read it.

**The derivation.** The model's photon *is* the Riemann–Silberstein analytic field (decision 5, F67–F69). A genuine radiation field is **null**: `F·F = E² − B² + 2i E·B = 0`, i.e. `|E| = |B|` and `E ⊥ B`. `build_beam_packet` builds `F = (scalar envelope)·ê` with `ê` **real**, so `F·F = (scalar)² ≠ 0`. It is not a null field. The null condition is the model's own consistency condition, not an import.

**The fix.** Complex circular polarization. With `a1 = (axis+1)%3`, `a2 = (axis+2)%3`:

```
ê = (ê_a1 + i·ê_a2)/√2 ;   F_vec = ê · f ,  f = envelope · exp(i·k0·d_axis)
E = Re(F_vec) ,  B = Im(F_vec)
```

**Implementation requirements:**

- Add a `polarization=` parameter, `"linear"` (default, **bit-identical** to today) and `"circular"`. Backward compatibility is mandatory — F386/F387/F388 all have green gate records built on the current behaviour and none of them may move. Verify that with `make gate`, not by inspection.
- Do the same for `build_pair_mode` only if it needs it. It almost certainly does not: it already sets `E ∥ e1`, `B ∥ e2 = k̂×e1`, which is correct. Confirm, don't assume.
- Switch Stage 5's scenario (`scenarios/photon_fermion_push.yaml`) and any momentum-sensitive test to `"circular"`.

**Acceptance — reproduce these exactly** (`L=16`, `σ=3.0`, unit amplitude, `center = [L/4 if a==axis else L/2]`):

| quantity | required |
|---|---|
| `\|Σ E×B\|` | `75.126` for `m ∈ {2,4}` on all three axes |
| `cos(P, k̂)` | `+1.000000` |
| `E·B/(\|E\|\|B\|)` | `≤ 1e-16` |
| drift under `photon_step_spectral`, 40 ticks | `≤ 5e-15` relative |
| linear mode vs today | bit-identical |

**New gate legs** (this is the durable part): a beam used in any momentum test must satisfy the null condition. Assert `|E·B|/(‖E‖‖B‖) < 1e-12`, `| ‖E‖−‖B‖ |/‖E‖ < 1e-12`, and `|Σ E×B| > 0` with `cos(P,k̂) > 0.99`. Add a declared control that turns them red.

**Do not** expect this to change the `Ĉ(k)`-longitudinal leakage. It does not (`0.2755 → 0.2741` at `m=2`); that is Part C's problem.

---

## PART B — make the curl defect visible (do this before Part C)

**The defect.** `charge_coupling.bcc_curl_symbol` is not the symbol of a curl. It builds its vector from `_bcc_uvec(k/2)`'s `n⁺` — the **fermion walk's spin-quantisation axis** — whose own docstring records the limit `n̂ → (k_x, −k_y, k_z)/|k|` and calls the y-sign flip "an intrinsic chirality convention of the Bisio BCC walk". Reusing it as a Maxwell curl generator inherits that reflection.

**Why nobody caught it.** Discrete exterior calculus gives two identities from `d∘d = 0`:

- `div(curl A) = 0` → `C·(C×A) = 0`. **Vacuous** — true for *any* vector field under a cross product. The module docstring cites it as evidence of correctness. It carries no information. The model's no-monopole gate (`iĈ·B ≈ 0`, in F387/F388/F389) tests exactly this one.
- `curl(grad φ) = 0` → `C×G = 0`, which requires `C ∥ G`. **This is the one that constrains C, and it has never been tested.**

**Your job in Part B is only to add the missing test.** Do not change `bcc_curl_symbol` yet.

Add a gate-tier leg measuring `‖C×G‖/(‖C‖‖G‖)` against both gradient symbols, with `C = k` as the control:

| symbol | expected |
|---|---|
| `C_odd` (current), spectral `G = k` | max `1.000000`, mean `0.741692` |
| `C_odd`, forward-difference `G_j = e^{ik_j}−1` | max `1.000000`, mean `0.707173` |
| control, true curl `C = k` | `0.000e+00` |

Also gate the on-axis reflection facts, which are exact at **every** grid mode and are the mechanism behind F390's axis breakdown: `Ĉ·k̂ = +1` on x and z, `−1` on y, for `m = 1,2,3,4`.

Register this as a **known-failing diagnostic**, honestly. A red-but-monitored leg is strictly better than an untested assumption. Use whatever the repo's convention is for that (check `tests/registry/` and `docs/design/finding-claim-test-guide.md`); if there is none, record the measured value as the expectation and add a caveat saying the expectation encodes a known defect, not a target.

This part is small, safe, and unblocks everything. **Write it as its own finding.**

---

## PART C — the curl symbol itself (decision point: do not rush this)

**Read this whole section before writing code.**

`bcc_curl_symbol` is load-bearing for `solve_A_coulomb_3d`, `magnetostatic_B`, `maxwell_curl_step`, `em_current.conserved_current`, `em_photon_sourcing.split_transverse_longitudinal` and `iC_dot_B_norm` — i.e. for F87, F384, F386, F387, F388, F389 and F390. F387 §1's argument that every consumer measures against `Ĉ` *consistently* is correct as far as it goes. The place it breaks is the boundary: the momentum observable `Σ E×B` and the Poynting geometry are Euclidean, not `Ĉ`-based, and the two conventions meet unreconciled exactly at the momentum question.

**The obvious one-line fix does not work. Verify this yourself first.** Undoing the reflection, `C_fixed = R·C_odd` with `R = diag(1,−1,1)`, improves matters a lot but does **not** produce a curl:

| candidate | `cos(C,k)` min | `‖C×G‖/(‖C‖‖G‖)` max | mean |
|---|---|---|---|
| `C_odd` (current) | `−1.000000` | `1.000000` | `0.741692` |
| `R·C_odd` (reflection undone) | `+0.088045` | `0.996116` | `0.175821` |
| `k` (true spectral curl) | `+1.000000` | `0.000000` | `0.000000` |

The reflection is exact only in the `k→0` limit and on the coordinate axes. At finite `k` off-axis, `C_odd` is parallel to neither `k` nor `Rk`. **Reproduce this table before proceeding** — if a one-line fix worked, the rest of this part would be unnecessary.

**The real fix is a discrete exterior calculus complex on the BCC lattice.** Assign fields by degree — scalars to sites (0-forms), `A` and `E` to bonds (1-forms), `B` to plaquettes (2-forms), charge to cells — and define the curl as the exterior derivative `d`, concretely the **oriented sum around a plaquette**. Then both identities hold by construction, because the boundary of a boundary is empty. Note that `B = dA` is then literally the Peierls holonomy, which is already what F385's per-link step computes.

**The repo already does this correctly in 2D.** `charge_coupling.discrete_curl_z` and `discrete_div` are exactly a DEC adjoint pair — the second's docstring says it was "chosen as the adjoint partner of `discrete_curl_z` so that `div∘curl ≡ 0`", and `solve_A_coulomb_2d` imposes the Coulomb gauge in that convention. The 3D BCC path did not extend it. **Extend existing correct code; do not invent a new symbol.** `references/lattice-conservation-laws-research-review.md` §2 names the nearest published precedent for a non-cubic DEC Maxwell complex.

**Constraints on how you land it:**

- **Do not replace `bcc_curl_symbol` in place.** Build the corrected curl as a new object alongside it, under the project's fork convention (`forks/gauge/`) or as a clearly named sibling. The falsification record matters and every magnitude-only result (`|C|/|k| → 1/√3`, F87's MX1, F26's `c_lat`) is untouched by the defect — F387 §1 already established that squaring removes the sign.
- Gate both `d∘d = 0` identities on the new complex to machine precision. The 2+1D prototype reaches `8.9×10⁻¹⁶`; match that in 3D.
- Then, and only then, measure the blast radius: run the existing consumers against both symbols and report what moves. **Report before switching anything.**

**If the BCC DEC complex turns out to be more than this session can carry, stop after Part B and say so.** A correctly-scoped negative result here is worth more than a rushed replacement, and the audit's §9 explicitly says deciding what to do about this symbol is a research session of its own. Parts A, B and D are independently valuable without it.

---

## PART D — re-run Stages 0–5

Only after Part A lands (Part C optional — if it does not land, say so explicitly in every finding and note that the re-run still carries the curl defect).

Work through `docs/roadmaps/photon-fermion-coupling.md` §2 in order. For each stage: re-run it against the fixed beam, record what changed, and write the result as a **new** finding.

- **Stage 0** — re-run the momentum baseline with the fixed beam. Note that `core/observers.py`'s `Momentum` is **verified sound** (`Σ E×B` is exactly conserved by `photon_step_spectral`, mode by mode) — do not "fix" the observer. The roadmap's own Stage 0 text says field momentum should be "derived on the model's own `C(k)` curl symbol"; that instruction is what Part C calls into question, and the observer's actual `Σ_k E_k × conj(B_k)` construction is the correct one. Record that.
- **Stage 1** — F384's current is unchanged as algebra. But read audit §6.1: its "transverse part is free gauge freedom" is a consequence of *defining the current by solving continuity*, and the alternative (current `= ∂S/∂A`, continuity as a theorem) removes the problem class rather than patching it. Do not rebuild that here; record it as the named successor route.
- **Stage 2** — F385 is unaffected. Confirm, don't redo.
- **Stage 3** — `solve_A_coulomb_3d` inherits the curl defect. If Part C landed, re-measure; if not, caveat it.
- **Stage 4** — re-run `F388-fermion-photon-coupled-channels` with the fixed beam. F388 §2's core finding (the current cannot radiate) is unchanged and remains correct.
- **Stage 5** — **this is the point of the exercise.** Re-run `scenarios/photon_fermion_push.yaml` with the circular beam and re-measure all four of F390's claims from scratch. Expect the cosines to change; how much is not knowable in advance, so measure, do not predict.

**Two specific things to settle in Stage 5:**

1. **The `m_index=4` anomaly.** F390 §3 measured the direction correlation reversing at `m_index=4` on the x-axis (`cos = −0.988`). The audit establishes this is explained by *neither* defect — `Ĉ = +k̂` exactly at `m=4` on x, and the fixed beam gives `cos(P,k̂) = +1.000000` at `m=4` on every axis. So it is not a photon-sector property; it lives in the matter-side coupling. Re-measure it with the fixed beam **before** theorising.
2. **Restate claim 1.** Audit §6.2: the roadmap's claim 1 (`ΔP_matter + ΔP_field ≈ 0`, with `P` a continuum-style functional) **is not achievable by any scheme on a lattice.** Discrete translation symmetry yields only crystal momentum, conserved modulo reciprocal lattice vectors. `Σ_k k|ψ̃(k)|²` is not even the right representative — it jumps by a reciprocal lattice vector on any Umklapp event. Replace the claim with:
   - **(A)** exact charge conservation (lattice Ward identity) — achievable, gate it;
   - **(B)** exact crystal-momentum conservation, checkable as `Φ∘T = T∘Φ` to machine precision. Necessary but **not discriminating** — the existing bridged scheme is translation-covariant too, so this alone does not separate schemes. Gate it anyway; it is the honest lattice statement of "momentum is conserved";
   - **(C)** matched-order approach to the continuum — `ΔP_total = O(aⁿ)` with **the same order in the coupling on both channels**. This is what F389 §4's `O(g)` vs `O(g²)` mismatch actually diagnoses.
   Update the roadmap text and `docs/claims/CL307` accordingly. Claim 1 as written should be **withdrawn as unachievable**, not left open.

---

## EXPLICIT DO-NOTS

- Do **not** edit `findings/F384`–`F390`. New findings + `supersessions.yaml` only.
- Do **not** change `bcc_curl_symbol` in place (Part C).
- Do **not** "fix" `core/observers.py`'s `Momentum` — it is verified sound.
- Do **not** change the default of `build_beam_packet` in a way that moves any existing green gate record.
- Do **not** report `make gate` green without running it; a bare `pytest` misses the three `kind: scenario` physics gates (CLAUDE.md, V-004).
- Do **not** quote the audit's §7 CONFIG A / CONFIG B numbers as results. That section explicitly marks the coupled-momentum comparison **not established** and CONFIG B **degenerate** (a real Gaussian ψ at rest with `A=0` has `J ≡ 0`, so nothing was sourced).

## FLAG FOR A LATER SESSION, NOT THIS ONE

`references/lattice-conservation-laws-research-review.md` §7.1: Nielsen–Ninomiya says a single Weyl species cannot carry exact chiral gauge symmetry on a lattice with locality and no doublers. F384–F390 all declare Weyl-2-spinor-only scope, which is exactly where the theorem bites. It is not an obstruction for a vector-like U(1) — ordinary QED — so the single-action route of audit §6.1 probably runs through the **Dirac** sector (`particles.dirac_bcc`), not the Weyl one. Cross-check against F328 and F378, which already bear on it. **Settle this before anyone builds the BCC DEC complex for the matter sector**, since it changes what `S_matter` is.

## DELIVERABLES

1. New findings for Part A, Part B, and each stage that materially changed, each with a test record, declared controls, and a `**Checked:**` line from the review pass.
2. `docs/status/changelog.md` entry (short, one paragraph).
3. `docs/status/exactness-inventory.md` updated for any new exactness claim.
4. `make indexes && make gate` green.
5. `docs/claims/CL307` updated; the roadmap's claim 1 restated per Part D.
6. A short closing report: what moved, what did not, and what you deliberately did not attempt.
