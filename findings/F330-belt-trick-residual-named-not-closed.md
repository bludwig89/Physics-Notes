# F330 — The belt-trick residual, precisely named: Anastopoulos's "Postulate 1" replaces "the belt trick, imported"; the model's own rotor confirms its spin-½ consequence, and a lattice-native derivation is attempted and abandoned with a stated reason

**Date:** 2026-08-27 - 16:03
**Numbering:** **F330**, taken as `NEXT FREE NUMBER` (no gaps — max+1). Session `quiet-lucid-finkelstein`, sector `interactions`.
**Status:** Confirmed (narrowing, not closing) — **4/4 PASS**, two declared controls each verified red and red only where expected.
**Checked:** 2026-08-27 — 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED**
**Verdict:** Completeness row **A9** stays `PARTIAL`. **Read §1 before the results** — this does not derive the belt trick, and does not claim to. What moves: the residual is no longer a vague "the belt trick, imported" — it is now a single, precisely stated, peer-reviewed postulate, its spin-½ consequence is machine-verified on the model's own rotor rather than asserted, a lattice-native derivation attempt is made and its failure is diagnosed rather than left unexamined, and a scoped (non-numeric) argument narrows the postulate's status specifically in this model.
**Modules:** `src/casim/engine/interactions/qi_belt_trick.py`
**Test / results:** record `F330-belt-trick-reduction` (tier gate, entry `check_belt_trick_reduction`), driver `tests/findings/test_F330_belt_trick_reduction.py` → `test-results/F330_belt_trick_reduction.json`
**Cross-references:** [[F289-spin-statistics-connection]] (the rotor, $R(2\pi)=-\mathbb 1$, $\mathrm{SWAP}^2=\mathbb 1$ — this finding's starting point and the number reused throughout), [[F291-why-three-plus-one-dimensions]] / [[F292-no-higher-multiple-of-three]] ($d=3$ derived), [[F26-speed-of-light-as-rotation-rate]] (the rotor's origin, decision 2), [[F253-weight-as-phase-scale-nogo]] (the closest precedent for "compute the lattice's own holonomy and see whether it can carry the needed content" — there it was the $E_g$ plane's $2\pi/3$; here the outcome is negative for a different, structural reason, §3). External: Finkelstein & Rubinstein, *J. Math. Phys.* **9** (1968) 1762; **Anastopoulos**, "Spin-statistics theorem and geometric quantisation," quant-ph/0110169 (the formalisation this finding leans on throughout); Berry & Robbins, *Proc. R. Soc. A* **453** (1997) 1771 (the geometric-phase route this finding's B1/B2 is the $n=2$, spin-½ special case of).

---

## 1. What is claimed, stated before the results

F289 closed row A9's algebraic content: the spin-statistics theorem needs two premises — the spatial dimension ($\pi_1$ of the $n$-particle configuration space is $S_n$ only for $d\ge3$) and the $2\pi$ rotation phase of the exchanged object — and this model *derives* both rather than importing them ($d=3$ from F291/F292; $R(2\pi)=-\mathbb 1$ from the model's own SU(2) rotor since F26). F289's own "what remains" list named the gap this finding was chartered to attack:

> *"The homotopy between exchange and $2\pi$ rotation (the belt trick) is likewise the external Finkelstein–Rubinstein construction... A lattice-native version — an explicit path of BCC hops realising the exchange and its $2\pi$ counterpart, with the phase read off the walk — is the natural next step and is **not** done here."*

**This finding does not do that either.** §3 explains why the attempt was made and abandoned, and the reason is structural, not a failure of effort: the belt trick's content is a fact about the topology of *continuous* $\mathbb R^3$ (specifically, that $\mathbb R^3\setminus\{0\}$ retracts to the simply-connected $S^2$, and that the frame bundle $\mathrm{SO}(3)\to S^2$ over it is non-trivial), and the model's own topological content — the finite point group $O_h$ acting on the BCC lattice — is a different, unrelated kind of structure that does not supply a substitute.

What this finding does instead:

1. **Names the residual exactly**, via Anastopoulos's peer-reviewed formalisation, rather than leaving it as an unspecified "belt trick, imported" (§2).
2. **Machine-verifies, on the model's own rotor**, the two representation-theoretic facts that make the named postulate's spin-½ consequence concrete rather than hand-waved (§5) — closing a real gap in F289 itself, which asserted "premise I2 then picks the one for spin-½: $-1$" without showing the mechanism connecting a *single*-particle rotation fact to *which* eigenvalue of the *two*-particle exchange operator is selected.
3. **States a scoped, non-numeric narrowing argument** for why the residual, while not eliminated, is less arbitrary in this model than in generic non-relativistic QM (§4) — explicitly labelled as a narrowing, not a derivation, matching CLAUDE.md's "moving toward a documented POSIT rather than an open residual."

---

## 2. The residual, named exactly: Anastopoulos's "Postulate 1"

Charis Anastopoulos ("Spin-statistics theorem and geometric quantisation," quant-ph/0110169) gives a geometric-quantisation derivation of the spin-statistics connection that isolates its one non-topological ingredient as a single, explicit postulate. Paraphrased to the two-particle, spin-$s$ case this model needs:

> **Postulate 1.** Exchanging two identical particles must be realisable as a smooth path along the orbit of the (diagonal) rotation group $\mathrm{SO}(3)$ acting on the pair, avoiding all coincident configurations, such that performing the exchange **twice** composes to **exactly one $2\pi$ rotation**.

Given Postulate 1 plus the already-standard facts — $R(2\pi)=(-1)^{2s}\mathbb 1$ on the spin-$s$ representation, and $\pi_1(S^2)=0$ so that *every* collision-avoiding exchange path is homotopic to the same representative (the "rotate the connecting rod by $\pi$" path, which manifestly satisfies Postulate 1) — the exchange sign follows: $(-1)^{2s}$, i.e. Fermi for half-integer spin, Bose for integer spin. This is precisely Finkelstein–Rubinstein's belt trick, restated with its non-topological content isolated into one named sentence.

**Why $\pi_1(S^2)=0$ does the topological half of the work, exactly, with no lattice content needed.** The relative-position space of two non-coincident points in $\mathbb R^3$ is $\mathbb R^3\setminus\{0\}$, which deformation-retracts onto $S^2$ (radial projection). $S^2$ is simply connected. So *any* two collision-avoiding paths from a separation $\mathbf r_0$ to $-\mathbf r_0$ are homotopic **rel endpoints**, and parallel transport (or any connection-respecting quantity) along homotopic paths with fixed endpoints agrees — a completely general fact about connections, not special to this model. This is genuinely elementary: it needs no lattice structure, and the ambient space is $\mathbb R^3$ whether or not the dynamics on it happen to be a BCC cellular automaton. **So the "uniqueness of the exchange path up to homotopy" half of the belt trick transfers to this model for free, unchanged, and needs no re-derivation.**

**What Postulate 1 supplies beyond that** is the claim that the *specific* representative path (rigid rotation by $\pi$) is the physically correct one to use — i.e. that the internal (spin) degrees of freedom are transported along the chosen exchange path via the *same* rotation that realises the positional exchange, rather than via some other, uncorrelated unitary. Anastopoulos states this cannot be derived from geometry alone; it is an assumption about *how physical transport works*, imposed by hand. **This is the actual content of "the belt trick, imported."**

---

## 3. The lattice-native attempt, and why it was abandoned

The natural question, and the one this session's brief asked: does the BCC lattice's own structure — the finite point group $O_h$ (order 48), the rotor's $\Omega(\mathbf k)=2\omega(\mathbf k/2)$ construction (decision 2), or F253's precedent of computing an explicit lattice holonomy (the $E_g$-plane $2\pi/3$) — supply Postulate 1, or a discrete substitute for it, rather than leaving it as an import?

**No, and the reason is a category mismatch, not insufficient searching.** $O_h$ is a **finite** subgroup of $\mathrm{SO}(3)$: it classifies which *discrete* rotations map the BCC lattice to itself. Postulate 1 is a statement about *continuous* paths in the full $\mathrm{SO}(3)$ (or its double cover $\mathrm{SU}(2)$) connecting two positional configurations — the belt trick is precisely the fact that $\mathrm{SO}(3)$, as a continuous manifold, is not simply connected ($\pi_1(\mathrm{SO}(3))=\mathbb Z_2$), and that a $2\pi$ rotation traces the non-trivial loop. $O_h$, being finite and discrete, carries **no fundamental-group content of its own that could stand in for this** — a finite group's classifying space has a different (and here, irrelevant) homotopy type from $\mathrm{SO}(3)$'s. F253's holonomy computation ($2\pi/3$ on the $E_g$ plane under the $C_3$ point-group element) is a genuine discrete holonomy, but it answers a different question — a symmetry-breaking angle in an internal order-parameter space — and has no bearing on the *continuous* rotation-group topology the belt trick needs. **Searching for a discrete analogue of $\pi_1(\mathrm{SO}(3))$ in $O_h$ is not a hard problem this finding failed to solve; it is not the right kind of object to look in.**

The rotor's $\Omega(\mathbf k)$ construction (decision 2) is likewise the wrong tool for a different reason: it is a **dynamical** rotation rate (radians accumulated per CA tick, as a function of momentum), whereas Postulate 1 needs a **kinematic** (parallel-transport / holonomy) rotation — how an object's orientation frame responds to being *moved along a path in space*, with no reference to time evolution or dispersion at all. The two are conceptually different constructions that happen to share the word "rotation." Nothing forces them to coincide, and the model does not supply a bridge between them.

**What survives, and is worth recording precisely so a later session does not re-attempt the same dead end:** the model's spin *does* live in a genuine $\mathrm{SU}(2)$ representation (the rotor), and $R(2\pi)=-\mathbb 1$ on it *is* exactly the double-cover fact the belt trick needs downstream of Postulate 1. What the model does not supply is the *kinematic transport law* — the connection on the position-times-spin bundle that would make Postulate 1 a theorem about paths rather than an assumption about how spin moves. Building such a connection from the CA's own update rule (rather than positing it) is a well-defined, harder question this finding does not attempt, flagged in §7.

---

## 4. A narrower argument: Postulate 1 has no rival in this model (stated as a POSIT-narrowing, not a derivation)

In generic non-relativistic quantum mechanics, "spin" is an abstract internal Hilbert space attached to a particle, with an $\mathrm{SO}(3)$ action imposed by hand as an extra postulate (the particle "has spin $s$" means its internal states carry the spin-$s$ representation, full stop — nothing about how that representation must respond to a particle being *moved* is forced by anything else in the theory). Postulate 1 is exactly the further, independent choice of *how* that internal representation transports along a physical path, and generic QM has no resource to argue it could not have been otherwise: a theory could in principle attach spin to particles via some other, uncorrelated transport rule, and nothing internal to non-relativistic QM forbids it. That is the sense in which Anastopoulos calls it *ad hoc*.

**This model does not have that freedom to exercise.** There is no separate "spin Hilbert space" in the tree at all — the two-component object at every site *is* the $\mathrm{SU}(2)$ rotor built in F26/decision 2, and every place spin appears (F289's rotor, this finding's $R(\theta,\hat n)\otimes R(\theta,\hat n)$) is that same object. The model has never constructed, and has no place to construct, a second, independent transport rule that spin could instead obey. So while this finding cannot show that Postulate 1's specific content (spin transports via the *same* rotation that carries the position) is **forced** — no argument here derives it from anything more basic — it can say something narrower and true: **there is no alternative available within the model's own structure for Postulate 1 to be chosen over.** That is a real, stated narrowing of "arbitrary physical assumption" toward "the only mathematically expressible option," in the same spirit as F255's upgrade of a posit via Schur-isotropy — but weaker, because F255 proved uniqueness from a representation-theoretic theorem, and this argument only observes the absence of a constructed rival. **It is reported here as a POSIT-narrowing claim and nothing stronger, and it is not represented by any numeric check in `qi_belt_trick.py`** — there is no way to machine-verify the non-existence of a construction nobody has proposed.

---

## 5. What is machine-verified — the spin-½ consequence, on the model's own rotor

Given Postulate 1 (external, §2) and the uniqueness of the exchange path (elementary, §2), the representative exchange path is "rotate the pair rigidly by $\pi$." This finding verifies, using `qi_belt_trick.py` (which reuses `qi_spin_statistics._rotor_for_physical_angle`, F289's own function, rather than a second implementation):

| Check | What it shows | Residual |
|---|---|---:|
| **B1** — antisymmetric singlet, invariance sweep (12 axes × 12 angles, including non-multiples of $\pi$) | $R(\theta,\hat n)\otimes R(\theta,\hat n)$ never leaks the true singlet outside its own span, for **any** angle and axis, and the retained coefficient is exactly $1$ | leak $1.77\times10^{-16}$; phase deviation $3.33\times10^{-16}$ |
| **B2** — symmetric triplet, deviation from scalar at $\theta=\pi$ | the triplet is an invariant **subspace** but is **not** a scalar representation at the belt trick's own exchange angle — eigenvalues exactly $\{-1,+1,-1\}$ | deviation $1.632993=\sqrt{8/3}$ (exact) |
| **B2b** — triplet subspace leak at $\theta=\pi$ | confirms the triplet *is* invariant (does not mix with the singlet) — the needed contrast against B2 | $1.57\times10^{-16}$ |
| **B3** — two exchanges, composed | $(R(\pi)\otimes R(\pi))^2=\mathbb 1$ exactly, **via F289's own already-derived** $R(2\pi)=-\mathbb 1$ (imported and surfaced, not recomputed) — "exchange twice returns the identical state," recovered from the geometric route rather than reasserted | $3.46\times10^{-16}$; cross-checked against F289's own $R(2\pi)+\mathbb 1$ residual, $1.73\times10^{-16}$ |

**What this closes that F289 left open.** F289 established that $\mathrm{SWAP}$ has spectrum exactly $\{+1^{(3)},-1^{(1)}\}$ (an involution, from $d\ge3$) and separately that $R(2\pi)=-1$ (the rotor), then stated *"premise I2 then picks the one for spin-½: $-1$"* without exhibiting the mechanism. B1/B2 exhibit it: the belt-trick construction (Postulate 1's representative path) reduces to a genuine c-number phase **only on the antisymmetric channel** — the singlet is the unique one-dimensional invariant subspace on which "exchange = a scalar" is even a well-posed statement for *every* rotation angle, not merely $\theta=\pi$. On the symmetric (triplet) channel the same construction is **not** a scalar at $\theta=\pi$, so the naive identification does not directly apply there — which is exactly why extending this argument beyond a single antisymmetric pair (general $n$, or spin $>1/2$) is the substance of the still only partially resolved Berry–Robbins problem (Atiyah 2000–2001 gave a general construction using algebraic geometry; the case is not closed for all $n$ by elementary means), not a straightforward corollary.

**Why B1's exact result is not a tautology.** A one-dimensional subspace is trivially "scalar" under *any* operator that preserves it — the substantive claim is that the true singlet's span is *preserved at all* (does not leak into the triplet) for every rotation, which is a genuine, checkable fact about the antisymmetric combination specifically, verified by direct construction from Pauli kets (not imported "pre-labelled" as special). §6's control demonstrates this is not vacuous: the symmetric ($m=0$ triplet) state, given the identical treatment, fails.

---

## 6. Controls

| Perturbation | Goes red at | Meaning |
|---|---|---|
| `--param theta_exchange=6.283185307179586` (2π instead of π) | B2 | at the *wrong* angle the triplet becomes scalar again (integer-spin $2\pi$-periodicity: $D^{(1)}(2\pi)=\mathbb 1$) — confirming $\pi$, the belt trick's own exchange angle, is what makes the triplet non-scalar, not an arbitrary choice of angle |
| `--param wrong_singlet=true` | B1 | substituting the $m=0$ triplet member (identical normalisation, symmetric instead of antisymmetric) breaks the invariance under a generic axis — B1 is a real statement about the antisymmetric combination, not a tautology about any 1-dimensional subspace |

Both verified via `casim test --control --id F330-belt-trick-reduction`: each control reddens exactly the named leg and no other.

---

## 7. What this closes, what it narrows, and what remains

**Closes nothing new at the level of the spin-statistics theorem itself** — Postulate 1 is not derived, and this finding says so throughout, not only here.

**Narrows.**

1. The residual is now a single, precisely stated, citable postulate (Anastopoulos's Postulate 1) rather than an unspecified "belt trick, imported" — a genuine sharpening of what row A9's `PARTIAL` status means.
2. F289's unexhibited step — *why* spin-½ picks the $-1$ eigenvalue of $\mathrm{SWAP}$ rather than merely being told two eigenvalues exist — is now machine-verified on the model's own rotor (B1/B2/B3), closing a real gap in F289's own argument.
3. A lattice-native derivation was genuinely attempted, and its failure is diagnosed with a specific, stated structural reason (§3: $O_h$ is finite and cannot carry $\pi_1(\mathrm{SO}(3))$'s content; the rotor's $\Omega(\mathbf k)$ is dynamical, not kinematic/parallel-transport) rather than left as an unexamined possibility for a future session to re-attempt blindly.
4. A scoped, explicitly non-numeric argument (§4) narrows Postulate 1's status specifically in this model: the model has no independent spin Hilbert space and hence no constructed rival transport law for the postulate to be chosen over — weaker than a derivation, stronger than leaving the postulate unexamined.

**Remains, stated as precisely as this finding can make it.**

1. **Postulate 1 itself is not derived**, here or anywhere in the cited literature — it is imported, exactly as F289 already said, now with an exact citation and statement rather than a paraphrase.
2. **The kinematic transport law is not built.** §3's diagnosis names what a genuine internal derivation would require — a connection on the model's own position-times-spin structure, derived from the CA update rule rather than posited — and this finding does not attempt it. This is the concrete next step, if one is taken: not "search the lattice for a homotopy invariant" (§3 explains why that search is mis-targeted) but "construct, from the update rule, a parallel-transport law for the rotor along a spatial path, and check whether it *forces* Postulate 1's specific content or leaves it free."
3. **Only spin-½, $n=2$ is covered.** B1/B2's clean reduction is specific to a single antisymmetric pair; general $n$ or spin $>1/2$ is the (still only partially closed) Berry–Robbins problem, not addressed here.
4. **§4's narrowing argument is not a numeric result** and is not falsifiable by a `casim test` invocation in the way B1–B3 are — it is a structural observation, honestly labelled as weaker than a derivation.

---

## Reviewed & corrected

**2026-08-27 - 16:21** — attack pass: **CONFIRMED**. A cold adversarial subagent ran all 13 attacks
plus unprompted checks (module docstring vs. code, the session-claims `used:` entry, and the validity
of the "homotopic paths with fixed endpoints give equal parallel transport, for any connection" step
in §2). Found: nothing that breaks or narrows the finding's stated claim — 11/13 clean PASS, 2 minor
WEAKENS (both cosmetic/process, not physics): (a) the registry record's single blanket
`expect: {exactness: exact, tol: 1e-12}` doesn't literally govern B2's lower-bound-style pass condition
(`deviation_from_scalar > 0.5`) the way it governs the residual-to-zero legs — noted, but this exactly
matches the established house pattern already used in F289 itself (S3b/S5c mix residual and
inequality checks under one declared tolerance), so it is not a departure introduced here; (b) B1's
near-zero leak is, by a linear-algebra identity, forced for *any* $\det=1$ SU(2) rotor acting on the
antisymmetric tensor — the sweep is an implementation-correctness/control check rather than a probe
capable of discovering new physics, which the finding's own §5 already states ("not a tautology... the
substantive fact [is that it does not leak]") but did not spell out as explicitly as it could have.
Fixed: renamed the module docstring's stale `C1`–`C4` labels to match the actual `B1`/`B2`/`B2b`/`B3`
check names used throughout the code and registry record, and added one clause to B1's docstring entry
naming the linear-algebra-forced nature of the sweep directly. Rejected: none — no attack claim was
found to be wrong. Deferred: none. Two process-hygiene gaps the subagent caught (no changelog entry
yet at review time; `tests-index.md` stale after `gen_test_registry.py` ran post-indexing) are closed
in the same session, after this note, per Step 7/9 below.
