---
id: CL253
title: The lattice's minimal coupling forces the einselected pointer basis to be site charge density, and its exact block-spin operator makes coherence irrelevant at b^-2 per dimension while populations stay marginal
slug: measurement-pointer-born-rg
tier: headline
kind: derivation
status: live
domain: [QM]
exactness: exact
findings: [F281]
tests: [F281-measurement-pointer-born-rg]
modules: [casim.engine.interactions.qi_measurement]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-05
last_verified: 2026-08-05
provenance: authored
review_state: authored
confidence: high
---

# CL253 — The pointer basis is forced by minimal coupling, and classicality is the block-spin attractor

## Statement

In this model the system–environment generator is fixed by the rule rather than chosen: every
interaction enters as minimal coupling, $\psi(x)\to e^{-iq\alpha(x)}\psi(x)$, whose generator
$H_\text{int}=\sum_x\hat\alpha(x)\otimes\hat n(x)$ is diagonal in site occupation. Therefore
$[H_\text{int},\hat n(y)]=0$ **exactly** (measured `0.0`, not $10^{-16}$) for every $y$, the
einselected pointer observable is the local charge density, and classicality is position
definiteness. Spin is **not** einselected (commutator $6.2219$), so a spin superposition survives
until amplified into a position difference.

Under the model's own exact block average $R_b$, a coherence whose branch-relative phase carries
wavevector $k$ acquires the RG eigenvalue $\lambda_\text{coh}(k,b)=\lvert D_b(k)\rvert^2 =
[\sin(kb/2)/(b\sin(k/2))]^2$ — **exactly 1 at $k=0$** (populations marginal; coarse total charge
matches the fine total charge with residual `0.0`) and with envelope $b^{-2}$ per dimension,
$b^{-6}$ in 3-D, for $k\ne0$. Coherence is therefore an *irrelevant* operator at the same leading
order as the F130 Lorentz-violating operators ($\lambda_n=b^{-n}$, leading $n=2$), so the IR fixed
point of the quantum lattice is a diagonal density matrix.

## What it extends

Decoherence theory (Zurek): einselection identifies the pointer basis as the one commuting with
$H_\text{int}$, but in standard quantum mechanics $H_\text{int}$ is a modelling input, so *which*
observable is classical is a choice made per problem. This claim removes the choice for this model:
the pointer observable is a consequence of the rule's minimal coupling, and key decision 3
(Higgs-free — no Yukawa scalar, no non-minimal coupling anywhere in the tree) is what closes the
alternatives. The classical limit is likewise upgraded from a limit taken by hand to an RG
eigenvalue of an operator the model already owned (F130/F133).

It does **not** extend or contradict unitarity: no collapse term is added, and F227's "unitary
theory with no objective collapse" is unchanged. The finite-environment recurrence
($\log_{10}(T_\text{rec}/\tau)\approx4.58\times10^{23}$ ticks for a mole of environment cells) is
a consequence of that unitarity, not a new mechanism.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md` §1 | $[H_\text{int},\hat n]=$ `0.0`; sieve minimises at the site basis with $S=6.1\times10^{-16}$; spin and hopping commutators non-zero | exact |
| `findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md` §3 | $\lambda_\text{coh}$ closed form vs the model's actual $R_b$ to $8.9\times10^{-16}$; $\lambda(k{=}0)=$ `1.0`; exponents `-2.0` / `-6.0` with residual 0 | exact |
| Record `F281-measurement-pointer-born-rg` (tier gate, entry `check_measurement`) | 17/17, with three declared controls verified red | exact |
| `test-results/F281_measurement_pointer_born_rg.json` | the result artifact | machine |

The Born-rule leg of F281 is deliberately **not** carried by this card — see
`## Status & history`.

## Falsifier

Three, each a declared parameter perturbation of the gate record, and each verified to fire:

1. `casim test --id F281-measurement-pointer-born-rg --param coupling=nonminimal` — replace the
   model's minimal coupling with any coupling that is not a function of the local charge density.
   M1a/M1b go red: the commutator becomes $6.2219$ and the predictability sieve's minimiser moves
   from $\theta=0$ to $\theta=\pi/4$. **If a non-minimal coupling is ever found to be required
   anywhere in the model — a Yukawa scalar, a derivative coupling, any term not built from
   $\hat n(x)$ — this claim fails**, because the uniqueness argument is exactly the absence of
   such a term.
2. `--param block_b=1` — M3c goes red. Included because it is the trivial way the RG statement
   could be vacuous, and the ratchet should say so.
3. A measured $\lambda_\text{coh}$ departing from $\lvert D_b(k)\rvert^2$ by more than $10^{-12}$
   at any $(k,b)$ would falsify the closed form directly; nine points are checked.

The claim is **not** falsifiable by experiment: both the recurrence exponent and the $10^{-143}$
macroscopic coherence suppression are unobservable by construction. That limit is stated in F281
§"Not claimed" and is why `tier: headline` rests on the structural results rather than on a
prediction.

## Status & history

Issued 2026-08-05 from F281, which was written to close completeness row **A8** (measurement
problem / classical emergence), recorded `ABSENT` with *zero hits repo-wide* in
`docs/status/completeness-2026-08-04.md`.

**Deliberately narrower than F281.** F281 also derives the Born rule on two legs — a dynamical
leg (only $\ell^2$ is conserved by a real BCC Weyl tick; change `0.0`, every other $p$ moving by
3–32%) and an envariance leg (fine-graining gives $p_k=\lvert c_k\rvert^2$, exact over $\mathbb Q$).
That result is **not** claimed on this card, because the envariance leg inherits the standing
Schlosshauer–Fine objection (it assumes outcome weights depend only on the reduced state) and the
dynamical leg assumes weights are a function of the amplitudes at all. Neither assumption is
derived in F281, and F281 says so in §2.6. A Born-rule card should be written when one of those
two hypotheses is closed, or written now as `status: contingent` with the hypothesis named — that
is a judgement for the next session and is recorded here so that "no card" is a decision rather
than an omission.

**Condition met, 2026-08-06.** `CL264` is that card. It closes leg 1's hypothesis rather than
leg 2's: Gleason derives both that outcome weights are a function of the state and that the
function is quadratic, once the model supplies the two premises — $\dim\ge3$, because a
measurement here needs a record and a record needs cells (and the rule's own 2-dim momentum
blocks are invariant but *unreadable*), and non-contextuality, because the record channel is
$H_\text{int}$ itself and carries no reference to the measured basis. Leg 2 is not repaired but
made **unnecessary**: that route never uses envariance, so the Schlosshauer–Fine objection has
nothing to attach to. **This card is otherwise unchanged** — its subject is the pointer basis and
the RG, and F304 moves neither.

**Scope limit carried from F281 §"Remains".** The diagonality argument is proved explicitly for
the $U(1)$ wrap generator. The $SU(2)_L$ and $SU(3)_c$ couplings are site-local rotations and are
diagonal in position by construction, but the explicit non-Abelian commutator has not been
written out. This card's statement is therefore correct as written — the pointer observable is
site charge density — but the *uniqueness* half of the argument is currently $U(1)$-explicit and
non-Abelian-by-inspection. Widening it is named as the next step in F281.

## Sources

- `findings/F281-measurement-pointer-basis-born-rule-rg-classicality.md`
- `findings/F227-decoherence-unitarity-floor.md` — the causal cone, and "unitary, no objective collapse"
- `findings/F130-blockspin-rg-gauge-gravity.md` — the exact `R_b` and the LIV irrelevance exponent this matches
- `src/casim/engine/gauge/minimal_coupling.py` — the generator whose diagonality is the whole argument
- `src/casim/engine/core/blockspin.py` — `block_average_field`, the `R_b` measured against
- `docs/status/completeness-2026-08-04.md` — row A8, ABSENT, the gap this closes
- Zurek, *Rev. Mod. Phys.* **75** (2003) 715 — einselection, predictability sieve, envariance
- Schlosshauer & Fine, *Found. Phys.* **35** (2005) 197 — the standing objection to the envariance leg
