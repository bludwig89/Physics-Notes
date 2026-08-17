---
id: CL271
title: Granted one internal index the rule does not read, the colour gauge group's unitarity, tracelessness, locality, connection, vector-like coupling and gluon count are all forced — so colour is one imposition, not six
slug: colour-structure-forced-by-one-index
tier: supporting
kind: derivation
status: live
domain: [QCD, QFT]
exactness: exact
findings: [F317, F91, F27, F68, F279, F293, F298, F289]
tests: [F317-su3-structure]
modules: [casim.engine.gauge.derive_su3_structure]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-16'
last_verified: '2026-08-16'
provenance: authored
review_state: authored
confidence: medium
---

# CL271 — Colour is one imposition, not six

## Statement

The completeness rubric's row **B1** records *"colour is still put in"*. That sentence bundles six
separate impositions. Granted **exactly one** of them — that the quark carries an internal index
which the model's own update rule does not read — the other five are **forced**:

1. **Unitary.** "Internal" means the rule acts on that factor as $R\otimes\mathbb 1_N$. The
   commutant of the model's own two steps (F27 mass step; BCC walk) on the full space is
   *computed* to be $M_N$, $\dim = N^2 = 9$, so the norm-preserving invariance group is exactly
   $U(N)$. The count is only meaningful because those steps generate the **full** $M_4$ on the
   Dirac factor ($\dim = 16$) and the re-typed walk is unitary ($2.2\times10^{-16}$).

2. **Special unitary.** The $U(1)$ subgroup of $U(N_c)$ carries a nonzero mixed anomaly on the
   model's own hypercharge nullspace:
   $A_{[SU(2)_L]^2U(1)_\text{trace}} = N_cb/2 \neq 0$, while the *same row* gives
   $A_{[SU(2)_L]^2U(1)_Y}=\tfrac12(N_cy_Q+y_L)\equiv0$ identically in $N_c$. **F27's chirality is
   what removes the $U(1)$ from $U(3)$**; a vector-like weak sector would leave $U(3)$ available.

3. **Local, hence a connection.** A cellular automaton has no global operations: its rule is one
   operator applied at every cell, so the on-site step commutes with a **site-dependent** $V(x)$
   ($7.0\times10^{-16}$) while the hop, which compares two cells, fails at $O(1)$ ($1.343$) and is
   repaired exactly ($6.0\times10^{-16}$) only by $U_\mu\to V(x)U_\mu V^\dagger(x{+}\hat\mu)$. The
   gluon field is the price of the rule being local — and the same statement, read on the on-site
   step, is *why* F27's $U(x)$ is pure gauge.

4. **Vector-like.** All 27 symmetric anomaly coefficients of $su(2)$ are **exactly** zero, while
   $su(3)$ carries $A^{888}=-1/\sqrt3$. Of $\{$vector-like, chiral, conjugate$\}$ exactly one
   colour assignment is anomaly-free. The model's chiral weak / vector-like strong split is
   therefore **one** fact, not two independent choices.

5. **Eight gluons.** $\dim su(3)=N^2-1=8$, and the connection of (3) is algebra-valued.

The sixth — the multiplicity $N=3$ — is **pinned but not free**: $\Lambda^3(\mathbb C^N)$ carries
an $SU(N)$ singlet at exactly one $N$, and it is 3. With Fermi statistics **derived** in-tree
(F289) rather than imported, that fixes $N_c=3$ **given one empirical input**: that baryons are
three-constituent states. It agrees with, and is logically independent of, F298's parameter-free
structural $N_c\le3$.

## What it extends

Standard-Model practice **posits** $SU(3)_c$ and reads its consequences off; the historical arguments
for colour (Greenberg 1964; Han–Nambu 1965) establish the multiplicity from hadron spectroscopy and
then adopt the group. The pieces used here — the $d^{abc}$ obstruction to a chiral triplet
(Georgi, *Lie Algebras in Particle Physics*; Weinberg II §22), the gauge principle, the
$[SU(2)_L]^2U(1)_B$ anomaly that is the standard reason baryon number is not gauged, and the
$\varepsilon$-tensor count — are all textbook, and **this card claims no new mathematics.**

What is extended is the *accounting*. In the SM the six impositions listed above are independent
postulates, because there is no rule beneath them to test them against. Here there is: the model has
a specific local update, a derived chiral $SU(2)_L$ (F27), a derived hypercharge nullspace
(F279/F293) and derived Fermi statistics (F289), and every leg above is evaluated **on those**. That
turns four postulates into consequences and reduces a fifth to one empirical input. The QCA
literature (D'Ariano–Perinotti and successors) derives free field dynamics from a homogeneous
update but takes internal gauge structure as given; no derivation of the colour group's *shape* from
a QCA rule was found.

## Evidence

Record `F317-su3-structure` (tier gate, entry `check_su3_structure`), **21/21 PASS**, 1.2 s.

| leg | statement | residual |
|---|---|---|
| S0 | $\operatorname{Tr}T^aT^b=\tfrac12\delta^{ab}$ — the basis is checked, not trusted | `0.0` |
| S1a | all 27 $su(2)$ symmetric anomaly coefficients, exact over $\mathbb Q[i]$ | exactly `0` |
| S1b | $A^{888}=-1/\sqrt3$, exact | $-\sqrt3/3$ |
| S1c | exactly one of three colour assignments is anomaly-free | 0.0 / 0.5774 / 1.1547 |
| S2a | branch-space coupling is a scalar | `0.0` |
| S2b | the split a chiral colour would have cost | $5.137\times10^{-3}$ |
| S3a | on-site step commutes with **site-dependent** $V(x)$ | $7.0\times10^{-16}$ |
| S3b | bare hop — covariance fails | $1.343$ |
| S3c | with the compensator — exact | $6.0\times10^{-16}$ |
| S3d | same three legs on the tree's own `strong.py` | $1.391$ / $4.3\times10^{-16}$ |
| S4a | the rule generates the full $M_4$; the re-typed walk is unitary | 16; $2.2\times10^{-16}$ |
| S4b | commutant $=M_3$ | $\dim = 9$ |
| S4c | prediction: every level exactly 3-fold degenerate | $9.0\times10^{-16}$ |
| S5a | $[SU(2)_L]^2U(1)_Y\equiv0$ in $N_c$ | exactly `0` |
| S5b | $[SU(2)_L]^2U(1)_\text{trace}=N_cb/2$ | symbolic, $\neq0$ |
| S5c | nullspace dimension | 1 |
| S5d | cubic $SU(N)^3$ cancels $2-2$, with $A(\mathbf3)\neq0$ | `0.0`; 0.5774 |
| S5e | $2y_Q-(y_u+y_d)\equiv0$ in $N_c$ | exactly `0` |
| S6a | $\Lambda^3(\mathbb C^N)$ singlet count, $N=2..6$ | 0,**1**,0,0,0 |
| S6b | the singlet at $N=3$ | $\dim=1$ |
| S7 | $\dim su(3)=8$; the algebra closes | $5.6\times10^{-17}$ |

**Six declared controls, each verified red and red only where declared:**
`use_compensator=false` → S3c+S3d; `chiral_colour=true` → S2a; `rule_reads_colour=true` → S4b
(commutant $9\to3$); `drop_d_R=true` → S5d+S5e; `n_colour=4` → S6b; `n_colour=2` → S1c+S5d+S6b.

## What this does NOT claim

$SU(3)_c$ is **not derived from nothing.** The existence of the internal index is an input and
nothing in F317 produces it. The claim is the reduction: six impositions to one.

It also claims **no new mathematics.** Three of the legs are textbook (the $d^{abc}$ obstruction,
the gauge principle, the $[SU(2)_L]^2U(1)_B$ anomaly, the $\varepsilon$/Fermi-statistics count for
colour). What is new is that they are evaluated *on this model's own content and rule*, where they
close a gap the tree had recorded as open.

## What it changes elsewhere

**CL086 / F91's one unforced assignment is closed.** F91 recorded colour's vector-like coupling as
`by construction` and the BCC gluon's even propagation law as **unforced**, selected by *"the
elegant-design philosophy"*. Leg 4 supplies the missing premise, so F91 G1's chain
(vector-like $\Rightarrow$ branch-scalar coupling $\Rightarrow$ F68's even law) runs with no free
step. The even law is now **forced**.

It does **not** touch the X1 colour-normalisation fork (centre vs Casimir), and does not re-open
any of B10's three closed routes (anomaly, spatial-3, $\mathbb Z_3$) — no centre appears anywhere
in it.

## Falsifier

1. **Any step of the rule found to read the colour index** (a genuine colour dependence in the walk
   or the mass step, not a background gluon). The commutant then stops being $M_N$, the group is
   smaller than $U(N)$, and legs 1–2 collapse. Made to fire as a declared control:
   `--param rule_reads_colour=true` collapses the commutant $9\to3$.
2. **A colour representation other than a single fundamental per chirality.** A reducible or higher
   assignment can be anomaly-free while chiral, and leg 4 goes with it.
3. **A right-handed $SU(2)_L$ doublet entering the content.** $[SU(2)_L]^2U(1)_\text{trace}$ then
   vanishes, $U(3)$ becomes available, and leg 2 is unexplained again.
4. **A stable colour-singlet bound state with a number of constituents other than three**, produced
   by the tree's own binding sector. The $\Lambda^3$ count then selects a different $N$.

## Status & history

**2026-08-16 — first issued** with F317 (drafted at F316, renumbered after a 70-second collision with
a concurrent session; recorded in the finding header and on the claim board).

`status: live`. `confidence: medium` rather than high for one reason, stated rather than implied:
the whole card is **conditional on the internal index existing**, and that condition is not derived
anywhere in the tree. If a future finding shows the index cannot be added to the model's cell
without breaking F291's spatial bound or F313's time count, this card's premise fails and every leg
goes with it. That is a live question — the coloured quark field is $s=36$ where both of those
results live on the minimal $s=2$ cell — and it has never been asked.

Row **B1** is expected to move from *"colour is still put in"* to `PARTIAL` with a single named
input at the next completeness run; **this card does not itself move a rubric grade** (that is a
completeness-run decision).

## Sources

- `findings/F317-su3-structure-derived.md` — the finding, with §8 stating prior art leg by leg
- `src/casim/engine/gauge/derive_su3_structure.py` — the module
- `tests/findings/test_F317_su3_structure.py`, record `F317-su3-structure` → `test-results/F317_su3_structure.json`
- [[F91-pairing-classification-theorem]] / **CL086** — the assignment this closes, amended not retracted
- [[F27-complex-mass-chiral-su2]], [[F68-minimal-coupling-forces-even-photon]], [[F279-hypercharge-constraint-attribution]], [[F293-why-three-colours]], [[F298-casimir-ladder-c7-rerun]], [[F289-spin-statistics-connection]], [[F43-fg7-dynamical-gluons]]
- `docs/status/completeness-2026-08-07.md` row B1 — the row this answers
- External: Greenberg, *Phys. Rev. Lett.* **13** (1964) 598; Han & Nambu, *Phys. Rev.* **139** (1965) B1006; Georgi, *Lie Algebras in Particle Physics* (2nd ed.) ch. 25; Weinberg, *The Quantum Theory of Fields* **II** §22
