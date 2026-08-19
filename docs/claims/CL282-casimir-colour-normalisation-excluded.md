---
id: CL282
title: 'The Casimir normalisation of the model''s bare colour coupling is excluded: g_s = sqrt3/4 with alpha_s(M_Z) = 0.0397 is a tested no-go, and g_s = 1/2 with alpha_s(mu_0) = 1/(16 pi) is the adopted reading'
slug: casimir-colour-normalisation-excluded
tier: headline
kind: no_go
status: live
domain: [QCD, SM]
exactness: exact
findings: [F325, F298, F299, F303, F294, F280, F144, F111b, F110, F101]
tests: [F325-x1-branch, F298-casimir-ladder, F303-coupling-normalisation]
modules: [casim.engine.gauge.derive_x1_branch, casim.engine.gauge.casimir_ladder, casim.engine.gauge.derive_coupling_normalisation]
constants: []
supersessions: [S22-F298-mixed-matching-C_F-and-the-X1-branch]
reviews: []
rolls_up_to: CL022
falsifier: stated
first_issued: '2026-08-18'
last_verified: '2026-08-18'
provenance: authored
review_state: authored
confidence: high
---

# CL282 — The Casimir normalisation of the bare colour coupling is excluded

## Statement

The model's bare colour coupling at the lattice scale is $g_s=\tfrac12$, i.e. $\chi=1$ and
$\alpha_s(\mu_0)=g_s^2/4\pi=1/(16\pi)$, and the $SU(N_c)$ $\beta$-function is the correct one to run it
with. The alternative reading — that the F110 C7 matching carries a fundamental Casimir, giving
$\chi=1/C_F=3/4$, $g_s=\sqrt3/4$ and $\alpha_s(M_Z)=0.0397$ ($-66.4\%$) — is **excluded**, on two
independent grounds:

1. **Structural.** The $C_F$ exists only in a *mixed* evaluation of C7, with the abelian rotor's
   $\mathbb Z_N$ symmetric residue $s(k)^2$ in the numerator against the $SU(N)$ gauge theory's
   $C_2(R_k)$ in the denominator. Under either self-consistent evaluation — both sides abelian, or
   both sides $SU(N)$ — $\chi=1/(4g^2)$ **identically, for every $N$ and every irrep**, exact over
   $\mathbb Q$. The mixed evaluation is not a rival convention: off the k-string tower it is
   level-dependent at $N=3$ as well, giving $\chi\in\{3/4,\,3/10,\,3/16\}$ plus **undefined** for the
   adjoint, decuplet and 27, where $s^2=0$ against $C_2\neq0$ — it assigns zero electric cost to a
   triality-0 link.
2. **Quantitative.** The Casimir reading requires
   $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=3.4\times10^{6}$, which is **5.63 decades** above
   the top of the model's own committed bracket $[1,\,7.980]$ (CL252), and requires the rule's
   loops-only one-loop constant to be $7.24\times$ Wilson's for an action measured at $5.3$–$5.7\times$
   **smaller** discretisation error than Wilson's.

Neither ground needs the $d_1$ computation that the X1 ledger row named as the decider.

## What it extends

This is a no-go on a *reading* of the model's own bare coupling, and what it protects is a claim about
established physics: the zero-parameter prediction of $\alpha_s(M_Z)$ by dimensional transmutation from
a Planck-scale boundary value (CL022, F144), which the excluded reading would have moved from a
$2.1\sigma$ tension to a $-66\%$ falsification. It also settles a question in lattice gauge theory's own
vocabulary: whether a compact-$U(1)/\mathbb Z_N$ rotor's integer flux ladder may be matched level-by-level
against an $SU(N)$ link's Casimir ladder. It may not — the two are different operators, and the constant
relating them is a spectral discrepancy rather than a stiffness.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F325-x1-resolved-branch-b-adopted.md` §2 | three evaluations of C7 over $\mathbb Q$; only the mixed one produces a $C_F$ or an $N$ restriction | exact |
| `findings/F325-x1-resolved-branch-b-adopted.md` §3 | branch A vs the CL252 bracket: 5.630 decades, $7.241\times$ Wilson's loops-only | quantitative |
| `findings/F325-x1-resolved-branch-b-adopted.md` §5 | the magnetic side of C7 audited: unit-entry adjacency in both theories, no factor | exact |
| record `F298-casimir-ladder` leg **L6** | $\chi=1$ for every $N$ and all 11 irreps at $N=3$ under the consistent matching; control `numerator=casimir` reddens exactly L2, L3 | exact |
| record `F303-coupling-normalisation` leg **N8** | the band rebuilt from its committed inputs; control `casimir_on=False` reddens exactly N8 | quantitative |
| record `F325-x1-branch` | 7/7, two controls verified `CONTROL` | exact / quantitative |
| `findings/F324-ncolour-bracket-closed.md` §3 U1c | the mixed matching already level-dependent at $N=3$ off the tower (the sextet leg), booked there as falsifier 5b | exact |

## Falsifier

Three, and the first is the one to attack.

1. **Show the integer flux spectrum is derived from the rule**, rather than the exactly-solvable
   modelling choice F101 §2, F110 and `link_hamiltonian.py` present it as. The rule's own $(\mathbf
   E,\mathbf B)$ are continuous real fields under an $SO(2)$ rotation and the model's links are
   $SU(3)$-valued matrices; if instead the rule forces an integer-spectrum $\hat E$ on a link, the mixed
   matching is physical, this no-go fails, and CN19 returns with it.
2. **A completed one-loop background-field computation of the model action's own $\Lambda$-ratio
   returning $\approx3.4\times10^{6}$** — six decades outside CL252's bracket — would reinstate the
   Casimir reading. Any value inside $[1,\,7.98]$ confirms this card.
3. **A measurement of $\alpha_s(M_Z)$ near $0.0397$** would do it observationally, which is to say the
   card is falsified by the world as well as by the tree.

## Status & history

Issued 2026-08-18 with F325, closing ledger row **X1** (`docs/status/open-derivations.md` Part D), which
had stood since 2026-08-06 as the project's only recorded contradiction — *"two adopted results that
disagree"* — and was load-bearing for rubric rows B8, B10, D16, G5, E3, Q1 and Q2 simultaneously.

The caveat behind it is older than the row: F101 §7 wrote the "A-vs-C / Casimir caveat" on **2026-06-05**,
F144 was built across it a week later, and F294/F298/F299 rediscovered it as "H1 vs H2" two months on.
The resolution has the same shape one level up — F294 §"Remains" item 1 asked for a genuine $SU(N)$ link
Hamiltonian to settle the reading, and one already existed (`su3_ladder.py`, **2026-06-07**, five days
before F144, finding F111b), uncited by any of the four findings that wanted it.

**What this card costs, recorded here because a no-go that hides its price is not a no-go.** F298's
structural $N_c\le3$ bound (**CN19**) falls with the mixed matching, and that bound is also **CL281's
upper constraint** — so the $N_c$ bracket reopens from $\{3\}$ to odd $N_c\neq1$, $\{3,5,7,\dots\}$, with
CL281 narrowed accordingly. **$d_1$ is not closed by this card**: its role changes from choosing a branch
to pinning $\alpha_s(M_Z)$ inside the adopted one.

**The residual, which is a different question from the one this card closes.** F325 §6 shows the
circularity lemma of F144 A1 step 2 fixes only the electric/magnetic stiffness *ratio*, so
$\chi=1/\Omega(k)$ and the value $\chi=1$ is F101 §7's normalisation rather than a derivation. That does
not revive the Casimir reading — $\chi=3/4$ is not derived either — but it means the adopted $g_s=\tfrac12$
rests on one unclosed $k$-selection, plausibly the same object as F155's matching scale $q_\ast$.

## Sources

- `findings/F325-x1-resolved-branch-b-adopted.md`
- `findings/F298-casimir-ladder-c7-rerun.md`, `findings/F299-casimir-scaling-discriminator-reinstated.md`, `findings/F303-no-centre-normalisation-argument.md` (all partially superseded, **S22**)
- `findings/F111b-tree-gauge-su3-ladder.md`, `findings/F280-d1-subtracted-against-wilson.md`, `findings/F324-ncolour-bracket-closed.md`
- `docs/theory/supersessions.yaml` record `S22-F298-mixed-matching-C_F-and-the-X1-branch`
- `docs/status/open-derivations.md` Part D (row X1, resolved)
- `docs/status/x1-colour-normalisation-fork-2026-08-18.md`, `docs/status/x1-section8-results-2026-08-18.md`
- Kawai, Nakayama & Seo, *Nucl. Phys.* **B189** (1981) 40
