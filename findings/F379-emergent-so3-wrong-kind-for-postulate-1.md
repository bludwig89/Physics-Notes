# F379 — The model's emergent CONTINUOUS SO(3) genuinely extends F344 to the full rotation group (same rotor as F289/F330), but is the wrong KIND of object for Anastopoulos's Postulate 1: the residual is prequantisation-level (kinematic), not dynamical, at any size

**Date:** 2026-09-10 - 00:00
**Numbering:** **F379**, taken as `NEXT FREE NUMBER` (max F378, no gaps — max+1). Session `cowork-A9-emergent-so3-kinematic-2026-09-10`, sector `interactions`.
**Status:** Confirmed — **3/3 PASS**, one declared control verified red and red only where expected (`casim test --id F379-so3-kinematic-gap --control`).
**Checked:** 2026-09-10 - 11:30 — cold-subagent blind re-derivation + adversarial referee, 13-point attack pass: **CONFIRMED-NARROWER**. Central structural argument survived independently and was sharpened (a second, deeper layer added to §3); two citation errors and one code bug (untested branch '-' sign matrix) found and fixed. See "Reviewed & corrected" below.
**Verdict:** Completeness row **A9** stays `PARTIAL`, but the residual is hardened rather than merely re-asserted: the one route F330 left open (an emergent *continuous* SO(3), as opposed to the finite $O_h$) is tested directly, found real but insufficient, and the reason it is insufficient is shown to be general — it forecloses the entire "derive Postulate 1 from a bigger/better continuum limit" avenue, not just this model's specific attempt.
**Modules:** `src/casim/engine/interactions/qi_so3_kinematic_gap.py`
**Test / results:** record `F379-so3-kinematic-gap` (tier gate, entry `check_so3_kinematic_gap`), driver `tests/findings/test_F379_so3_kinematic_gap.py` → `test-results/F379_so3_kinematic_gap.json`
**Cross-references:** [[F330-belt-trick-residual-named-not-closed]] (the abandonment reason this finding generalises), [[F289-spin-statistics-connection]] (the rotor, $R(2\pi)=-\mathbb 1$), [[F344-bcc-walk-point-symmetry-d4h]] (the 48-element leading-order covariance this finding extends to the continuous group), F129/F130 (rubric A12, block-spin RG isotropy — the "emergent SO(3)" this finding tests and finds insufficient), [[F291-why-three-plus-one-dimensions]] (the "lattice's isotropy group is a premise" weak link). External: **Anastopoulos**, "Spin-statistics theorem and geometric quantisation," quant-ph/0110169v3 (published *Int. J. Mod. Phys. A* **19**, 655, 2004) — fetched and read directly this session (pages 1–16 plus Appendix A/B), Postulate 1 quoted verbatim in §2 below rather than paraphrased.

---

## 1. What is claimed, stated before the results

F330 abandoned a lattice-native belt-trick derivation with a stated structural reason (§3): the finite point group $O_h$ "carries no fundamental-group content of its own that could stand in for" $\pi_1(SO(3))$, and the rotor's $\Omega(\mathbf k)$ is a *dynamical* (temporal) rotation rate, not a *kinematic* (parallel-transport) one. F330's own text named the one route it left open, and this session's brief repeated it: does the model's own **continuum-limit machinery** — F129/F130's block-spin RG (rubric A12, `MACHINE`: the dispersion becomes an isotropic IR fixed point) or F344's exact leading-order covariance of the BCC Weyl walk under all 48 elements of $O_h$ — recover a genuinely **continuous** $SO(3)$ that the finite $O_h$ could not supply?

**This finding answers that question directly, and the answer is no — but not for the reason one might guess (that the emergent continuous group is somehow still too small or not exact enough).** §4–§6 machine-verify that the model's emergent $SO(3)$ is real, exact, and genuinely extends F344 from 48 discrete elements to the full continuous rotation group, using literally the same rotor object central to F289/F330. §3 then shows, grounded directly in Anastopoulos's own paper (fetched this session rather than relied on via F330's paraphrase), that Postulate 1 is stated at a level — the classical phase space and its group action, *before any Hamiltonian is introduced* — that no fact about the model's *dynamics*, however large or exactly-derived the symmetry it recovers, can reach. This generalises F330's diagnosis: it is not that $O_h$ happened to be the wrong *size*; it is that a dynamical symmetry fact of *any* size is the wrong *kind* of object.

---

## 2. Postulate 1, quoted exactly from the primary source (not paraphrased)

F330 paraphrased Anastopoulos's Postulate 1. This finding fetched the paper directly (quant-ph/0110169v3) to pin its exact wording and — more importantly — the architecture surrounding it, which turns out to be the load-bearing fact.

**Postulate 1** (Anastopoulos, §4.2, verbatim):

> "In combination of two identical systems, each characterised by a symmetry group $G$, it should be possible to obtain the permutation (3.3) by smooth transformations along the orbits of the diagonal action of $G$ on $\Gamma_S$."

made explicit by three conditions (paraphrased tightly, symbols as in the paper): the Lie group $G$ acts **transitively by symplectomorphisms on** $\Gamma$ — the **classical phase space** (for a single spin-$s$ system, $\Gamma=S^2$, §4.1) — and (i) there exist one-parameter subgroups realising the positional exchange $x_1\to x_2$, $x_2\to x_1$ as non-coincident paths; (ii)/(iii) the **lift** of that action to the prequantising $U(1)$ bundle composes correctly to the exchange phase $e^{i\theta}$.

**The architectural fact this finding turns into a closed argument.** Anastopoulos states explicitly, twice, that his entire construction lives at the level of *prequantisation* — strictly before any Hilbert space or Hamiltonian is introduced:

> "our study does not need to take into account the full quantisation algorithm: the spin-statistics connection can be phrased at the level of **prequantisation**, *i.e.* **before constructing the physical Hilbert space**." (§1)

and, discussing group actions on phase space generally (§3):

> "Symmetries are generated by a Hamiltonian flow, **but this is the case for dynamics only if time-translation is a symmetry**. This is not the case in, for instance, open systems."

— i.e. Anastopoulos deliberately does *not* frame $G$'s action as a fact about any particular Hamiltonian's symmetry group. $\Gamma=S^2$ with $SO(3)$ acting transitively (§4.1) is pure representation theory: the Hopf-bundle integrability condition $s=n/2$ is a fact about $SU(2)$ and the sphere, true for *any* spin-$s$ system whatsoever — model, Hamiltonian, and dynamics unspecified. The paper's own Introduction (§1) restates the residual in the same register, before any of the geometric construction is even built: the postulate "remains equally *ad hoc* **in virtue of standard quantum theory**" — i.e. the gap is not filled by choosing a *better* quantum theory, this model's or any other's.

---

## 3. Why this closes the "emergent continuous SO(3)" avenue — the argument, stated before the numbers

Postulate 1's content is a claim about the **classical phase space** $\Gamma$ of the internal (spin) degree of freedom and a **transitive symplectic** action of $G$ on it, entirely prior to and independent of any Hamiltonian. F129/F130 (rubric A12) and F344 are, without exception, claims of a *different* kind: that the model's own **time evolution** — the dispersion relation $\Omega(\mathbf k)$, or the leading-order Weyl Hamiltonian $H_W=\boldsymbol\sigma\cdot\mathbf k/\sqrt3$ — becomes covariant under a rotation group **in a limit** (IR fixed point for F129/F130; leading order in $|\mathbf k|$ for F344). This is a **dynamical** (Hamiltonian-symmetry) fact.

Since Postulate 1's own architecture places its content strictly *before* any Hamiltonian is chosen — the transitive $G$-action on $\Gamma=S^2$ needs nothing beyond the standard $SU(2)/U(1)$ structure the model's rotor already has (F289's $R(2\pi)=-\mathbb 1$, unconditionally, with no reference to $H_W$, $\Omega(\mathbf k)$, or any dynamics at all) — no dynamical fact can bear on it. Enlarging the model's *dynamical* symmetry from the discrete $O_h$ (F330's diagnosis) to a genuinely continuous, exactly-derived $SO(3)$ (this finding's §4–§6) answers a question one logical layer downstream of the one Postulate 1 asks. **This generalises F330 §3's diagnosis**, which was stated specifically about *this* model's rotor ("$\Omega(\mathbf k)$ is dynamical, not kinematic"): the generalisation is that *any* dynamical symmetry fact — discrete or continuous, fundamental or emergent, of any size — is categorically the wrong kind of object, because the target (Postulate 1) is not a dynamical-symmetry statement at all. This is not a claim invented for this model; it is what Anastopoulos's own prequantisation architecture and his own Introduction-stage remark ("ad hoc in virtue of standard quantum theory", §1) already say.

**A second, independent layer, found while stress-testing this argument.** It is worth asking whether the mismatch is *only* dynamical-vs-kinematic, or whether even a genuinely kinematic object of the right type would still fall short. Anastopoulos's own §4.1 worked example supplies the test case: the free spin-$s$ system already has an **exact, transitive, symplectic** $SO(3)$ action on $\Gamma=S^2$ — not an IR/leading-order approximation, an honest group action on the actual classical phase space, which is *strictly stronger* than anything a dynamical-covariance argument (this model's or any other's) could ever hand over. And the paper still needs Postulate 1 as a **further, explicitly ad hoc** ingredient on top of that — condition (iii), that the *lift* of the one-parameter-subgroup exchange path into the prequantising bundle produces the physically correct phase, rather than some other consistent lift. So the gap is two layers deep, not one: (1) dynamical vs. kinematic (this model's emergent $SO(3)$ is dynamical, hence irrelevant), and (2) even an *exact, kinematic, phase-space-level* $SO(3)$ action — stronger than layer (1) could ever supply — is *still* not enough, because the lift/holonomy datum of condition (iii) is a separate structure that mere existence of the group action does not fix. This means that even a future, more ambitious attempt to build a genuinely kinematic (rather than dynamical) $SO(3)$ action directly from the model's own lattice structure — the route F330 §7 and this finding's §8 leave open — would *still* need to separately supply condition (iii)'s lift, and would not get it for free from the group action alone.

**What survives, and why the numerical work below still matters.** The argument in this section, by itself, is a reading of the primary source — it does not depend on whether this model's continuum limit is impressive or not. What §4–§6 add is: (a) confirmation that the model's continuum limit is exactly what it claims to be (real, continuous, exact $SO(3)$ covariance, not merely an aspiration); (b) identification of the object realising that covariance as *literally* F289/F330's own rotor, closing any residual worry that "maybe the model's dynamical rotor is secretly the right kind of kinematic object after all" (it is the same function, evaluated the same way, and the argument above still applies); and (c) a concrete extension of F344's own result (48 elements → the full continuous group), which is worth recording for its own sake regardless of the Postulate-1 question, since it further narrows F291's flagged weak link ("the lattice's isotropy group... is a premise").

---

## 4. K1 — the idealised Weyl Hamiltonian is covariant under the FULL continuous SO(3), via F289/F330's own rotor

$H_W(\mathbf k)=\mathbf k\cdot\boldsymbol\sigma/\sqrt3$ (F26/F344's own leading-order limit) is checked against

$$U(R)\,(\mathbf k\cdot\boldsymbol\sigma)\,U(R)^\dagger \;\overset{?}{=}\; (R\mathbf k)\cdot\boldsymbol\sigma$$

for $R$ a **continuous** Rodrigues rotation (not restricted to $O_h$'s 48 elements) and $U(R)=$ `_rotor_for_physical_angle` — F289/F330's own function, unmodified. Swept over 8 Fibonacci-sphere axes × 7 angles deliberately offset from $O_h$'s characteristic values × 5 $k$-directions (280 checks):

| Quantity | Residual |
|---|---:|
| worst $\lVert U(R)(\mathbf k\cdot\boldsymbol\sigma)U(R)^\dagger - (R\mathbf k)\cdot\boldsymbol\sigma\rVert$, 280 swept (axis, angle, $\mathbf k$) | $2.47\times10^{-16}$ |

**What this is, honestly stated.** The identity $U(R)(\mathbf k\cdot\boldsymbol\sigma)U(R)^\dagger=(R\mathbf k)\cdot\boldsymbol\sigma$ is the standard $SU(2)$-adjoint identity — true for *any* rotation $R$ and *any* correctly-parametrised rotor, model-independent, and it would pass at the same floor for $n_\text{axes}=n_\text{angles}=n_k=2$ just as well as for 280 swept combinations. It is **not** a new fact about this model's dynamics, and this finding does not claim it is. What is a genuine, non-tautological check is the **identification**: that the object realising the continuum-limit covariance for THIS model is literally F289/F330's own `_rotor_for_physical_angle`, evaluated at a continuous (non-$O_h$) rotation — i.e. this extends F344's 48-element-only verification to the continuous group **using the model's actual code**, closing the residual worry that the extension might fail for some convention-bookkeeping reason specific to the continuous case. K3 (§6) confirms the check is at least non-vacuous in the sense that matters (same rotation vs. an uncorrelated one).

---

## 5. K2 — the ACTUAL shipped BCC walk obeys the same law, extending F344's leg C8 to a generic continuous rotation (both branches)

F344 §4 established, for the shipped `bcc._bcc_uvec`, that the leading-order spin vector obeys $\mathbf n(g\mathbf k)=(SgS^{-1})\mathbf n(\mathbf k)$ for $g\in O_h$, with $S=\operatorname{diag}(p)$, $p=(+1,-s,+1)$ ($s=+1$ on the '+' branch, giving $S=\operatorname{diag}(1,-1,1)$; $s=-1$ on the '-' branch, giving $S=\mathbb 1$) — and verified (leg C8) that the covariance defect for one specific element, the $120°$ rotation about the body diagonal, shrinks linearly in $|\mathbf k|$ relative to $|\mathbf n|$ (decade ratios converging to exactly 10). This finding sweeps the **same relation for a generic continuous rotation** $R\notin O_h$ (axis $(1,1,-2)/\sqrt6$, angle $1.1071487$ rad — not a multiple of $\pi/2$ or $2\pi/3$), using $R'=SRS^{-1}$ as F344's own frame-conjugation prescribes, on **both branches** (the registry check exercises both, after the review below caught a sign error that the original single-branch check had not):

| $|\mathbf k|$ | rel. defect, branch $+$ | decade ratio | rel. defect, branch $-$ | decade ratio |
|---:|---:|---:|---:|---:|
| $10^{-1}$ | $2.870\times10^{-2}$ | — | $7.712\times10^{-1}$ | — |
| $10^{-2}$ | $2.916\times10^{-3}$ | $9.844$ | $7.825\times10^{-2}$ | $9.856$ |
| $10^{-3}$ | $2.920\times10^{-4}$ | $9.984$ | $7.836\times10^{-3}$ | $9.986$ |
| $10^{-4}$ | $2.921\times10^{-5}$ | $9.998$ | $7.837\times10^{-4}$ | $9.999$ |

Both branches converge to a decade ratio of exactly $10$ — i.e. the defect is linear in $|\mathbf k|$, exactly as F344's closed-form mechanism ($O(k^2)$ absolute, hence $O(k)$ relative) predicts, confirmed here for a **generic** continuous rotation rather than only the one discrete element F344 checked, and on both branches rather than only the shipped default. **What this is, honestly stated:** given F344's own leading-order coefficients ($p$, $q$, and the frame-conjugation $R'=SRS^{-1}$) as correct, the linear-in-$|\mathbf k|$ convergence for a generic continuous $R$ follows automatically from Taylor consistency of the shipped `_bcc_uvec` — it is not an independent lattice-symmetry mechanism beyond what F344 already established. The genuinely non-trivial content added here is confirming that the specific $S$-matrix convention is right on **both** branches (see "Reviewed & corrected" below — this is exactly the check that caught a sign-matrix bug in the branch-'$-$' path during review), not the continuous-vs-discrete generalisation by itself.

---

## 6. K3 — control: an uncorrelated rotor fails, confirming the check is not vacuous

| Perturbation | Residual |
|---|---:|
| K1 with the correct rotor $U(R)$ | $4.39\times10^{-17}$ |
| K1 with an **uncorrelated** rotor $U(R')$, $R'\ne R$ | $0.590$ |

Postulate 1's own content (F330 §2's paraphrase) is "spin transports via the *same* rotation... rather than via some other, uncorrelated unitary." K3 confirms this is exactly what K1 tests: substituting an unrelated rotation for the spin transport (same $\mathbf k$-rotation $R$, wrong spin rotor) breaks the identity at $O(1)$, not merely by round-off. K1's floor-level pass is therefore a genuine "same-rotation" statement, not a tautology of SU(2) unitarity.

---

## 7. Controls

| Perturbation | Goes red at | Meaning |
|---|---|---|
| `--param use_uncorrelated_rotor=true` | K1 only | transporting spin via a rotation uncorrelated with the one applied to momentum breaks K1's identity at $O(1)$ ($0.590$) while K2 (a fact about the shipped dispersion alone) and K3 (which reports both residuals directly) are structurally unaffected — confirming K1 tests the "same rotation" content specifically. |

Verified via `casim test --id F379-so3-kinematic-gap --control`: the control reddens exactly K1 and no other leg.

---

## 8. What this closes, what it narrows, and what remains

**Closes.** The "maybe a bigger/better continuum limit would supply Postulate 1" avenue, for a stated, general reason rather than by re-running F330's specific lattice attempt: Postulate 1 is architecturally prequantisation-level (prior to any Hamiltonian), so no dynamical symmetry fact — this model's continuous $SO(3)$ included, however exactly it is derived — can supply it. A future session should not re-attempt "derive Postulate 1 from an even bigger emergent symmetry group" without first defeating this argument, which does not depend on the size or exactness of the group recovered.

**Narrows/extends.**

1. F344's exact leading-order covariance (previously verified for exactly the 48 elements of $O_h$) is extended to the full continuous $SO(3)$, both for the idealised Weyl Hamiltonian (K1, exact, $2.5\times10^{-16}$) and for the actual shipped dispersion (K2, the same $O(k)$-relative mechanism F344 found for one discrete element, now confirmed for a generic continuous rotation).
2. F291's flagged weak link ("the lattice's isotropy group... is a premise, not something proved here") is narrowed further: the model's leading-order dynamics is now shown covariant not merely under $O_h$ (F344) but under the full continuous rotation group, using literally the spin-statistics argument's own rotor.
3. F330's abandonment reason ("$O_h$ is finite... $\Omega(\mathbf k)$ is dynamical, not kinematic") is generalised from a fact about this model's specific construction to a general architectural fact about Postulate 1 itself (grounded in the primary source's own prequantisation framing, fetched directly rather than paraphrased) — a stronger and more defensible closure than "the specific object we tried was too small."

**Remains, stated as precisely as this finding can make it.**

1. **Postulate 1 is not derived**, here or anywhere in the cited literature. This finding does not weaken that fact; it explains, more precisely than F330 could, exactly why no amount of dynamical symmetry — in this model or in principle — can change it.
2. **The genuinely open route, if one exists, is not more dynamics but a different logical object entirely**: a *kinematic* construction — a fact about the classical phase space $\Gamma$ and its group action, built from the model's own structure without reference to $H_W$, $\Omega(\mathbf k)$, or any time-evolution operator at all. This finding does not attempt to build one, and F330 §3's original observation stands: the model's only genuinely kinematic geometric object at the lattice scale is the finite $O_h$ point group, which (unchanged by this finding) still cannot carry $\pi_1(SO(3))$'s content.
3. **Only the spin-½, $n=2$ case is touched**, matching F330's own scope limit; the Berry–Robbins problem for general $n$/spin is untouched.
4. **A second, deeper layer, named in §3, sharpens the target for any future attempt.** Even a genuinely *kinematic* $SO(3)$ action built from the model's own structure — the route item 2 leaves open — would still need to separately supply Postulate 1's condition (iii): the lift of the exchange path to the prequantising bundle, i.e. a specific transport/holonomy law, not merely the existence of a transitive group action on a phase space. Anastopoulos's own §4.1 worked example (an *exact* transitive symplectic $SO(3)$ on $S^2$) already has the group action and still needs condition (iii) as a separate, additional assumption. A future attempt that builds a kinematic $O_h$-or-better action and stops there will not have closed the row.
5. **No new empirical prediction.** Every number here is a structural/consistency residual, as in F330.

---

## Reviewed & corrected

**2026-09-10 - 11:30** — attack pass (cold subagents: a blind independent re-derivation with F330/F289/F344 as allowed prerequisites but F379 itself forbidden, then a full adversarial referee with access to everything, per `.claude/commands/review-finding.md`). **Verdict: CONFIRMED-NARROWER.**

The blind re-derivation reached the same conclusion independently — categorical (prequantisation-level) mismatch, not a matter of degree — via its own reading of the primary source, and added the "second layer" argument now incorporated into §3 (Anastopoulos's own §4.1 worked example has an *exact* transitive symplectic $SO(3)$ action, strictly stronger than any dynamical-covariance fact, and *still* needs condition (iii) separately). This is treated as genuine independent convergence on the finding's central structural argument, which this finding's numerics (K1–K3) do not themselves establish and were never claimed to establish.

The adversarial referee ran all 13 attacks, executed the code directly, and found: the central structural argument (§3) survives all attacks and is accurate to the primary source (verified by an independent PDF fetch and text extraction). Two citation/attribution errors were found and are now fixed in this file and the module docstring: (a) the journal was misstated as "*J. Phys. A* **37**, 2004"; the paper is *Int. J. Mod. Phys. A* **19**, 655 (2004) — confirmed against arXiv metadata; (b) the "ad hoc... in virtue of standard quantum theory" quote was misattributed to the paper's Conclusions (§5), which contains no such language; it is in the Introduction (§1), before any of the geometric construction is built — now corrected in §2/§3. One genuine code bug was caught: `shipped_walk_continuous_covariance_decades`'s branch-$'-'$ sign matrix used $S=\operatorname{diag}(-1,1,-1)$, which contradicts F344's own stated convention $p=(+1,-s,+1)$ (giving $S=\mathbb 1$ on the '$-$' branch); the shipped default only ever exercised branch '+', so the bug was never caught by the gate. Fixed in `qi_so3_kinematic_gap.py` (confirmed: branch '$-$' now converges to decade ratio $\approx10$, matching branch '+'), and `check_so3_kinematic_gap`'s K2 leg now exercises **both** branches so this class of error cannot recur silently. §4/§5 above are also rewritten to state plainly that K1 is a standard, model-independent $SU(2)$-adjoint identity and K2's continuous-vs-discrete extension is largely an automatic Taylor-consistency corollary of F344's already-established coefficients — the genuinely non-trivial content is confirming the specific numeric conventions are right (on both branches) using the model's actual rotor and dispersion code, not the abstract "continuous group" generalisation by itself. This narrowing does not change the finding's verdict or its closing argument, which never rested on K1/K2 being non-trivial physics.

Rejected: none of the referee's 13 attacks broke the central argument (11 PASS-equivalent, 2 attacks — #6 external-data-currency and #12 robustness — genuinely FAILED and are the fixes above; the rest were PASS or WEAKENS on framing only, now addressed). Deferred: none. The referee's recommendation to double-check F129/F130's full content beyond a targeted grep is noted but not acted on here — those findings are cited only for their already-established headline result (rubric A12, `MACHINE`), which this finding does not re-derive or depend on beyond that headline.
