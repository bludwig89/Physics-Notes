# F342 — F75's own criterion doesn't select $T_{1u}$: condition (i) is vacuous under the model's site-diagonal gauge coupling

**Date:** 2026-08-31 - 16:35
**Status:** Candidate finding — 11/11 checks PASS (all exact, Fraction arithmetic; two declared controls each red only where declared). **This is a narrowing, not a promotion, of rubric row C1.** F75's group theory and F292's independent multiplicity check are untouched; what changes is *why* the physical identification stays a hypothesis.
**Module:** `casim.engine.particles.derive_generation_identification_gap` (new)
**Test record:** `F342-generation-identification-gap` (tier gate, entry `check_generation_identification_gap`), driver `tests/findings/test_F342_generation_identification_gap.py` → `test-results/F342_generation_identification_gap.json`
**Claim:** CL004 (`docs/claims/CL004-exactly-three-fermion-generations.md`) — narrows why it stays `contingent`; does not change its status.
**Checked:** 2026-08-31 - 17:05 — inline cold-subagent review (no independent claim-card-only "blind" pass; the reviewer knew the mechanism before verifying it), 6 PASS / 1 WEAKENS / 0 FAIL / 6 NOT RUN — **CONFIRMED**. See `docs/reviews/F342-review-2026-08-31.md`.
**Cross-references:** [[F75-three-generations-from-bcc-irrep-selection]] (Sec.1's operational definition and Sec.7's stated hypothesis — this finding's subject), [[F292-no-higher-multiple-of-three]] (§6 — the independent multiplicity check and the declined inference this finding explains), [[F324-ncolour-bracket-closed]] (premise (i) — untouched by this finding, see §6), [[F27-complex-mass-chiral-su2]] (the chiral mass step F75 §3 selects on), [[F38-fg1-anomaly-cancellation]] (the "identical gauge quantum numbers" content of F75's condition (i)).

---

## 1. The question this session was asked

Rubric row **C1** (`docs/status/completeness-2026-08-20.md` line 244) reads: *exactly three generations, PARTIAL — physical identification is a stated hypothesis.* F75 is closed as **group theory**: $\sum d^2=48$ forces the maximal single-valued $O_h$ irrep to dimension 3, and the BCC nearest-neighbour shell's odd-parity content realises exactly one such triplet, $T_{1u}$. What F75 §7 calls out, in its own words, is that *"generation index = orbital irrep of the nearest-neighbour shell"* is *"a model... not derived from the QCA update rule"* — a **stated hypothesis**, not a theorem. F324 (rubric B10) has since made even the **parity** of this count load-bearing for a second rubric row, which is why this session was asked to either close the hypothesis with a genuinely dynamical (not merely group-theoretic) argument, or show that it is not forced.

**Not re-attacked:** $\sum d^2=48$, or that $T_{1u}$ is the unique maximal single-valued irrep — both closed by F75 T1. **Not re-attacked:** F292's independent finding that the model's *other* instance of a "3" (the $d=3n$ reducible-dimension multiplicity) is a **frozen**, non-propagating degeneracy with no dynamics to carry a generation label — closed, and F292 explicitly, correctly, declined to read it as generations.

## 2. Why F292 declined, read against F75

F292 §6 is explicit about *why* its own "n copies of $\mathbb R^3$" multiplicity is not generations: *"the frozen directions have no dynamics to carry a generation label."* That objection **does not transfer to F75's mechanism** — the $T_{1u}$ shell states are the 8 real BCC nearest-neighbour lattice sites of the *same* $d=3$ vacuum, carrying the model's actual dispersion (F26/F30), not extra frozen spatial dimensions. F292's own falsifier 5 says as much: *"Derive the generations–frozen-copies identification of §6. That would promote an observation this finding deliberately refuses, and would bear on C1 and possibly B10."* F292 is not attacking F75's route at all; it is declining a *different, weaker* candidate identification and flagging, correctly, that doing so does not resolve F75's.

So the frozen-mode objection is not what keeps F75 §7 open. This finding identifies what actually is: F75's own *operational definition* of a generation multiplet (§1) has three conditions —

> (i) carry **identical gauge quantum numbers**, (ii) are related by an **exact symmetry of the vacuum**, (iii) are **mutually independent**.

(ii)+(iii) is exactly "single irrep," and that half is the closed group theory. **Condition (i) is the half that was never independently checked against anything dynamical** — F75 cites F38 as *"the quantum numbers that generations must share"* but never verifies that the *specific* three $T_{1u}$ partners in fact carry a common charge, as opposed to it being assumed. That is the gap this finding closes — not by deriving the identification, but by showing exactly how much condition (i) can and cannot do.

## 3. The new result: condition (i) is forced to be vacuous, by one fact about the shell

**Claim.** Under the charge structure this project's own gauge modules implement — a scalar coupling constant, diagonal in the lattice-site basis, with no site, shell, or irrep index anywhere (verified: `grep -rn "T_1u\|T1u" src/casim/engine/` outside `forks/` returns **zero** hits; `charge_coupling.py` and `minimal_coupling.py` carry a single scalar charge parameter `q`, never indexed by site) — **condition (i) is satisfied identically by every 3-dimensional subspace of the shell, $T_{1u}$ and $T_{2g}$ alike, with the same charge value.** It supplies zero bits of selecting power beyond F75's own group theory.

**Why it is forced, not observed.** The model's founding posit (F326/P1) is a single, local, *homogeneous* update rule — no site is dynamically distinguished from another by construction. A charge operator that is (a) diagonal in the site basis (the minimal-coupling ansatz actually used) and (b) invariant under the vacuum's full $O_h$ symmetry (required, since the gauge coupling is part of what condition (ii) calls "the vacuum") **must be a multiple of the identity**, *whenever the group acts transitively on the site set it is diagonal over*. Check `G2` verifies the 8 BCC shell vertices form a **single orbit** under $O_h$; check `H1` verifies that a diagonal invariant operator is forced constant exactly when this holds. Given both, condition (i) can no more prefer $T_{1u}$ over $T_{2g}$ (the triplet F75 Step 3 excludes only by the *unrelated* chiral-mass-parity argument) than over any other 3-dimensional subspace of the shell, including a non-irrep-adapted one.

**Control (falsifiability, `H1`).** Replace $O_h$ with the non-transitive subgroup generated by the single $C_{4z}$ rotation (two 4-vertex orbits instead of one). The diagonal-forced-constant claim goes red immediately (`casim test --control` confirms: reddens exactly `H1_diagonal_forced_constant`, nothing else). This is the check-worthy content of "the vacuum's *full* symmetry is what does the work" — a smaller residual symmetry would not force homogeneity, and this is exactly the state of affairs *after* F76's crystal-field mass splitting (which needs $O_h\to D_{2h}$): the argument here is a **statement about the unbroken point**, and is silent about the broken one, which is where real masses live.

## 4. An independent cross-check of F75 T2

The projectors used above are built by a method F75's own test does not use, so this doubles as an independent re-derivation of F75 T2's decomposition. Instead of character-table projection, embed the shell equivariantly into $\mathbb R^3$ twice: once by each vertex's own coordinates $M_i=(s_x,s_y,s_z)_i$ (the **vector**, i.e. $T_{1u}$, embedding) and once by the pairwise products $N_i=(s_ys_z,\,s_zs_x,\,s_xs_y)_i$ (the $T_{2g}$ embedding). Both give, **exactly over $\mathbb Q$**:

$$M^\top M = N^\top N = 8\,\mathbb 1_3,\qquad M^\top N = 0,$$

so $\Pi_{T_{1u}}=\tfrac18 MM^\top$ and $\Pi_{T_{2g}}=\tfrac18 NN^\top$ are exact rank-3 projectors (`H2a–H2d`), mutually orthogonal and idempotent together with the singlets $\Pi_{A_{1g}}=\tfrac18 J$ and $\Pi_{A_{2u}}=\mathbb 1_8-\Pi_{A_{1g}}-\Pi_{T_{1u}}-\Pi_{T_{2g}}$ (`H2e–H2f`, ranks exactly $[1,1,3,3]$), and each commutes exactly with all 48 elements of $O_h$ (`H2g`). This reproduces F75 T2's $A_{1g}\oplus A_{2u}\oplus T_{1u}\oplus T_{2g}$ by a genuinely different construction — two independently-typed routes agreeing is itself evidence neither is circular (the same style of cross-check F292 §3 used for $d=2$).

## 5. What *would* supply selecting power — and that it does not exist here

Condition (i) becomes non-vacuous only for a charge operator that is $O_h$-invariant but **not diagonal in the site basis** — concretely, one with a distinct eigenvalue on each irrep block, $Q_\text{block}=a\,\Pi_{A_{1g}}+b\,\Pi_{A_{2u}}+c\,\Pi_{T_{1u}}+d\,\Pi_{T_{2g}}$. This is exhibited exactly (check `H3`, control `charge_locality=block`): with $c\ne d$, $T_{1u}$ and $T_{2g}$ now carry **different** charges, and condition (i) genuinely discriminates. That is precisely what an *orbital-shape-dependent* coupling would look like — a Yukawa-type term sensitive to *which* neighbour-shell orbital a fermion occupies, not merely to *which species* it is.

**No such coupling exists anywhere in the adopted engine.** `charge_coupling.py`'s `q` parameter and `minimal_coupling.py`'s `u1_wrap_*`/`su3_rotate_*` functions all take a single scalar charge, uniform across sites; `T_1u`/`T1u` appears **nowhere** under `src/casim/engine/{core,lattice,gauge,particles,interactions}/` — only in three **fork** files (`forks/gravity/gr_fork_F79_structural_G.py`, `forks/gravity/gr_fork_F201_kev_from_eg_texture.py`, `forks/particles/derive_weight_as_phase.py`), which the registry itself classifies as *"tested-and-rejected or live-exploratory,"* not the adopted spine. The live E$_g$ weight-as-phase mechanism (F175/F253/F255/F256, CLAUDE.md decision 7) that *does* successfully reproduce the charged-lepton mass ratios uses $\dim(T_{1u}\otimes T_{1u})=9$ only as a **dimension count** in a denominator — it never assigns or checks a per-component charge, so it does not touch condition (i) either.

## 6. Consequence for F324 / rubric B10

F324 §0 premise (i) is *"$n_\text{gen}$ is odd — only the parity, never the value"* (`derive_ncolour_bracket.py` line 152: *"The model's generation count (F75). Only its PARITY is ever used."*). This finding does not touch that: F324 never invokes condition (i) or the per-component identification, only the bare integer count and its parity. **B10's dependence on C1 is unchanged by this finding** — it was already, correctly, understood as resting on F75's *count*, not on the specific-partner identification this finding is about. Recorded here so a later session does not conflate the two residuals.

## 7. Verdict

**Rubric C1 stays PARTIAL — this finding does not promote it, and does not intend to.** What it adds: the identification is not merely *unproven*, it is **shown not to be forced** by anything currently in the model's dynamics, and that "not forced" is now a checked, falsifiable, exact statement rather than an impression. F292's caution about the frozen-copy analogue does not apply to F75's mechanism (§2) — a genuine positive distinction worth recording — but the reason F75 §7 remains open is different from and sharper than "the group theory doesn't fix the physical read": **the one condition in F75's own defining criterion that could in principle do that job is guaranteed, by the model's own homogeneity posit, to do no work at all**, for any grouping of shell states, T$_{1u}$ included. This is the valuable negative result the session's protocol asked for: a demonstration that the identification genuinely could be otherwise, because nothing currently checks that it is not.

**What would promote the grade**, stated constructively per §5: exhibit a physical mechanism in the *adopted* engine (not a fork) that couples fermions to the shell **non-diagonally** in the site basis — sensitive to which $T_{1u}$/$T_{2g}$ orbital a fermion occupies, not just which species — and show it is forced by the model's own postulates rather than posited. Absent that, F75 §7's identification remains, correctly, "Candidate."

## 8. External check: this is a known-hard problem, not an idiosyncratic gap

The same gap — a group-theoretic or algebraic multiplicity of 3 with no dynamical closure to physical generations — recurs across the literature that attempts this kind of derivation, and no external template exists for closing it. Furey's complex-sedenion construction (Furey & Hughes, [arXiv:1904.03186](https://arxiv.org/html/1904.03186)) gets a factor of $S_3$ (order 3, structurally analogous to this project's $T_{1u}$ multiplicity) from $\mathrm{Aut}(\mathbb S)=\mathrm{Aut}(\mathbb O)\times S_3$, and states plainly that the correspondence to physical generations is *"currently being investigated"* and that *"it is not clear yet what this corresponds to physically"* — the identical gap, unclosed, in a different algebraic framework. Other approaches to "why three" (e.g. anthropic/leptogenesis arguments, [arXiv:1602.03003](https://arxiv.org/abs/1602.03003)) close the *count* by phenomenological selection rather than a first-principles dynamical mechanism, which is a different kind of argument than either F75 or this finding attempts. This project's residual is therefore generic to the shape of the problem, not a defect specific to this model — consistent with F324 §8's and F338's finding of the same pattern for B10's own residual.

## 9. Test summary (`test_F342_generation_identification_gap.py`, 2026-08-31)

| Check | Statement | Result |
|---|---|---|
| G1 | $\lvert O\rvert=24,\ \lvert O_h\rvert=48$ (cross-check of F75 G1) | PASS |
| G2 | 8-vertex shell orbit structure under the requested symmetry group | PASS (1 orbit, full $O_h$) |
| **H1** | **diagonal $O_h$-invariant charge forced constant** | **PASS** |
| H2a–c | $M^\top M=N^\top N=8\mathbb 1_3$, $M^\top N=0$ (exact) | PASS |
| H2d | independent re-derivation of F75 T2: ranks $[1,1,3,3]$ | PASS |
| H2e–f | partition of unity, idempotent, mutually orthogonal | PASS |
| H2g | $T_{1u}$, $T_{2g}$ projectors commute with the full group | PASS |
| **H3** | **condition (i) has zero selecting power (site-diagonal charge)** | **PASS** |

**Overall: 11/11 PASS.** Two declared controls, each red only where declared (verified via `casim test --control`): `symmetry_group=C4z_only` → reddens `H1` only; `charge_locality=block` → reddens `H3` only.

## 10. Falsifiers

1. **Exhibit a non-diagonal (orbital-shape-dependent), $O_h$-invariant gauge coupling in the adopted (non-fork) engine.** §5 dies immediately, and condition (i) regains real content — this is the concrete, constructive path to closing F75 §7.
2. *(Already checked, not a live falsifier — kept for completeness.)* The premises of §3 (the 8-site shell is a single $O_h$ orbit; the model's actual charge assignment is diagonal in the site basis) are checked facts about this project's own code and geometry, confirmed here and independently re-confirmed in review (`docs/reviews/F342-review-2026-08-31.md`), not open assumptions — so this is a verification already performed, not a future test that could still go either way.
3. **Derive, from the QCA update rule itself, why only $T_{1u}$ (not $T_{2g}$, not a non-irrep-adapted subspace) is dynamically populated with independent propagating fermionic content.** That would be the actual closure of F75 §7 and is explicitly not attempted here.

## 11. Provenance

- Session claim: `docs/design/session-claims.yaml`, session `steady-cubic-schur`, opened 2026-08-31 - 16:20.
- Module: `casim.engine.particles.derive_generation_identification_gap` (new; `_SPINE`, `findings=("F342","F75","F292","F324","F27","F38")`).
- Test record: `F342-generation-identification-gap`, `kind: assertion`, `tier: gate`, entry `check_generation_identification_gap`, 11/11 PASS, two controls verified red-only-where-declared via `casim test --control --id F342-generation-identification-gap`.
- Verification method: exact `Fraction` arithmetic throughout — no floating point, no `casim.numerics` dependency (this module does no array/FFT work and imports neither numpy nor the façade).
- Reads: F75 (the hypothesis and its operational definition), F292 (the declined analogue and its falsifier 5, which this finding answers in the negative for F75's own mechanism), F324 (the downstream B10 dependency, confirmed unaffected), F27/F38 (the chiral mass step and the anomaly content condition (i) invokes).
