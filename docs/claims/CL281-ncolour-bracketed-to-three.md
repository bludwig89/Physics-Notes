---
id: CL281
title: '$N_c=3$ is bracketed by two constraints that consume no measured number — F298''s C7 support $\{2,3\}$ and the $\mathbb Z_2$ doublet parity of the derived $SU(2)_L$ — at the cost of six named premises'
slug: ncolour-bracketed-to-three
tier: supporting
kind: derivation
status: narrowed
domain: [SM, QCD, QFT]
exactness: exact
findings: [F324, F317, F298, F318, F293, F279, F27, F75, F97, F99, F325]
tests: [F324-ncolour-bracket]
modules: [gauge.derive_ncolour_bracket]
constants: []
supersessions: [S22-F298-mixed-matching-C_F-and-the-X1-branch]
reviews: []
rolls_up_to: CL271
falsifier: stated
first_issued: 2026-08-17
last_verified: '2026-08-18'
provenance: authored
review_state: authored
confidence: low
---

# CL281 — $N_c=3$ from a parity and a ladder criterion

## Statement

Granted six premises — (i) an odd generation count, (ii) that the colour sector exists at all,
(iii) that the link rotor's modulus is the colour centre $\mathbb Z_{N_c}$, (iv) quarks in the
defining representation, (v) one colour-singlet lepton doublet per generation with right-handers
$SU(2)$ singlets, and (vi) no fermion doubling — the colour multiplicity is **odd and not 1** — $\{3,5,7,\dots\}$; the **upper** constraint that closed this on exactly 3 was withdrawn on 2026-08-18 (see *Status & history*), and no
leg of the argument consumes a measured **number**, the three-constituent baryon, or a branch of
the X1 colour-normalisation fork.

The **upper** constraint is F298's, imported and scanned one step lower: the C7 identity
$\chi_k=s(k)^2/(4g^2C_2(\text{antisym }k))$ is level-independent iff $N_c\in\{2,3\}$. The **lower**
constraint is the $\mathbb Z_2$ doublet parity: the model carries $n_\text{gen}(N_c+1)$ Weyl
isospin-$\tfrac12$ doublets — the $y_L=-N_c\,y_Q$ row of its own six-row hypercharge system — and
that count must be even, so $N_c$ is odd. The intersection over $N=1\ldots12$ is $\{3\}$.
Consequently the minimal totally antisymmetric all-quark singlet has three constituents — a
**corollary**, since given (iv) the constituent count *is* $N_c$.

**Three things this card does not claim.** The parity argument is **prior art** — Bär & Wiese 2001
state *"the number of colors must be odd in the standard model"* and obtain it unconditionally,
per generation, which is stronger than the total-count form used by default here. The incremental
content over F298 is **one bit**, selecting between two members of a set F298 already supplied, one
of which ($N=2$) passes F298's criterion **vacuously**. And $N_c$ is **not** derived from nothing:
premise (ii) is F318's untouched residual, and the $N=1$ edge is that premise restated in the
ladder's vocabulary rather than an independent exclusion.

## What it extends

The Standard Model takes $N_c=3$ as an input, and where it is argued rather than assumed the
arguments are measurements — $\pi^0\to\gamma\gamma$, $R$, the $\Delta^{++}$. What this card asserts
is a route with **no measured number** in it, and one that is independent of which branch of the
model's own centre-vs-Casimir dispute (X1) is correct.

**"No measured number" is not "no measurement."** Four of the six premises are empirically sourced
integers or booleans. The card states the narrow form and F324 §6 is written to stop the two being
used interchangeably.

The novelty relative to the literature is narrow and is stated as such: the group ($SU(2)_L$, via
F27's β-gauging) and the content (the F279/F293 nullspace) are **derived in this tree** rather than
assumed, and the parity is deployed as the lower edge of an **interval** rather than as a
consistency check on a known $N_c$.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F324-ncolour-bracket-closed.md` §2 (G0, W1, W2, W2b) | the mod-2 rule cross-checked against the Dynkin-index form ($T=1,4,10,20,35$); content $=N_c+1$ doublets/generation from the imported nullspace; parity $0,1,0,1,\ldots$ | exact (ℤ, ℚ) |
| `findings/F324-ncolour-bracket-closed.md` §2.1 (W3, W3b) | colour's **own** $\mathbb Z_2$ anomaly at $N_c=2$ is satisfied (4/generation), so the exclusion runs through $SU(2)_L$ — **and** the bracket is a function of the quark colour rep: fundamental $\{3\}$, adjoint $\{2\}$, two-index-antisym $\{2,3\}$, symmetric $\{2\}$ | exact |
| `findings/F324-ncolour-bracket-closed.md` §2.2 (Y1) | the same constraint arrives **locally** under a $U(2)$ embedding, via $q\equiv2j\ (\mathrm{mod}\ 2)$ on the model's own $y_L=-N_c$ | exact |
| `findings/F324-ncolour-bracket-closed.md` §2.1 (W4) | F293's six anomaly-**cancellation** rows contain neither reading: nullspace dim 1 at every $N_c$, grav and cubic identically zero in $N_c$ | exact (symbolic over ℚ) |
| `findings/F324-ncolour-bracket-closed.md` §3 (U1, U1b, U1c) | support $\{2,3\}$; **and both edges labelled** — $N=1$ fails by convention, $N=2$ passes vacuously; **and** the sextet gives $\chi=3/10$ against the tower's $3/4$ | exact (`Fraction`) |
| `findings/F324-ncolour-bracket-closed.md` §4 (B1, B1c) | the intersection is $\{3\}$; and the bracket is **empty** at a true $N_c\ge4$, so the argument can fail | exact |
| `findings/F324-ncolour-bracket-closed.md` §5 (P1, P2) | the constituent count $=N_c$ (corollary); agreement with F317 §6's float route, explicitly not confirmation | exact (over ℚ) |
| record `F324-ncolour-bracket` | 15/15 in-tree, **eight** declared controls, six distinct measured red sets | exact |

## Falsifier

1. **Fermion doubling** (premise (vi)) — the most likely way this dies. An even continuum species
   multiplicity makes the parity vacuous, and a naively doubled spectrum is **vector-like**, so by
   Nielsen–Ninomiya there is no chiral gauge theory left to constrain. The constraint survives only
   in a doubler-free (Ginsparg–Wilson) formulation, where Bär & Campos (hep-lat/0001025) exhibit
   the lattice analogue of Witten's obstruction. **CL020** is `narrowed`. Control:
   `doubler_multiplicity=2`.
2. **The k-string truncation failing at $N=3$** — the exposure F298 did not name and F324 U1c
   measures. The sextet $(2,0)$ gives $\chi=3/10$ against the tower's $3/4$, so if the full link
   Hilbert space is followed and level-independence does not survive at $N=3$, the upper constraint
   has **no support at all** and the bracket has nothing to intersect.
3. **Content** (premises (iv), (v)). A different quark colour rep, a fourth doublet species, or a
   right-handed doublet changes or vacates the parity. The conclusion does not weaken — it
   **inverts** to $N_c=2$. Controls: `quark_colour_rep=adjoint`, `include_lepton_doublet=false`,
   `vector_like_su2=true`.
4. **An even generation count** (premise (i)) — unless the Bär–Wiese per-generation form is granted,
   which retires this falsifier and replaces it with *"each generation must be independently
   consistent"*.
5. **The continuum-limit status of the obstruction.** $\pi_4$ is a fact about the Lie group; the
   model's $SU(2)_L$ is a lattice gauge symmetry, and a lattice-native form is not attempted. The
   local $U(2)$ reading (Y1) is partial insurance: under that embedding the constraint is
   perturbative and this falsifier does not apply.
6. **Premise (iii)** — the one premise with **no control**. If the rotor modulus is not the colour
   centre, the upper constraint is not a function of $N_c$ and the pairing dissolves.

## Status & history

**2026-08-18 — NARROWED from $\{3\}$ to odd $N_c\neq1$: the UPPER constraint is withdrawn
(F325, S22-F298-mixed-matching-C_F-and-the-X1-branch).** This card's upper leg is F298's C7 support $\{2,3\}$, imported verbatim. F325 shows that
support is a property of the **mixed** matching — the C7 identity evaluated with the abelian rotor's $s(k)^2$
against the SU(N) gauge theory's $C_2(R_k)$. Under either self-consistent evaluation $\chi=1/(4g^2)$ for
**every** $N$ and every irrep (exact over $\mathbb Q$; leg **L6** of `F298-casimir-ladder`, with the declared
control `numerator=casimir` reddening exactly L2 and L3), so there is no upper bound to intersect with.
**F324 anticipated this itself.** Its §3 U1c measured the sextet off the k-string tower — $\chi_6=3/10$ against
the tower's $3/4$ — and booked it as *"falsifier 5b … the most serious structural exposure on the upper side"*,
concluding *"the support $\{2,3\}$ is a property of the **truncation**, not yet of the model."* F325 completes
that table: at $N=3$ the mixed matching gives $\chi\in\{3/4,3/10,3/16\}$ plus **undefined** for the adjoint,
decuplet and 27, where the $\mathbb Z_3$ rotor's $s^2=0$ against $C_2\neq0$ — it assigns zero electric cost to a
triality-0 link. Falsifier 5b is therefore not merely exposed; it is realised.
**What survives, and it is the whole of the lower leg:** the $\mathbb Z_2$ doublet parity of the model's own
derived $SU(2)_L$ (Witten's global anomaly; prior art, Bär & Wiese 2001), which consumes no C7 input and no X1
branch, and gives $N_c$ **odd**. With premise (ii) removing $N=1$ the bracket is $\{3,5,7,\dots\}$.
F324 §8 priced its own incremental content over F298 at *"one bit"*; this spends exactly that bit, and the card
returns to where F324 found it minus the parity. `status` live → narrowed, `confidence` → low.
**The corollary goes with it:** the three-constituent baryon followed from $N_c=3$ given premise (iv), so it is
again $N_c$-conditional rather than discharged.

`contingent`, with all six contingencies in the Statement rather than a footnote.

**What this changes for B10.** Before F324 the row read: *the route space is mapped, the one
surviving route requires a normalisation the model's own machinery does not use, and no argument
for it exists* — F293 §4.2's $\Lambda$-scale selector, contradicted by F299 (the **X1** fork). That
selector is no longer needed, and **B10 stops being an X1 dependent**. X1 remains load-bearing for
B8, D16, G5, E3, Q1, Q2, and $d_1$ is still its deciding computation.

**A transfer of debt, recorded as one.** B10's conditionality has moved, not vanished: from a
hadron-spectroscopy fact inside the colour sector (F317 §6's three-constituent baryon) to F75's
generation parity (rubric row **C1**) plus premises (iii)–(vi). The **premise count went up.** What
improved is *proximity*: the old input was logically equivalent to the answer, and the new ones are
not. F324's grade recommendation is `PARTIAL` → `PARTIAL` with the row rewritten — **not** a
promotion.

**Adversarial pass, before first issue.** Two independent referees attacked this — one on the group
theory against the literature, one on circularity and overclaim — and both returned hits. All of
them are folded into F324 and this card rather than parked in a review file: the Bär–Wiese
attribution, the local-$U(2)$ correction to an "invisible to local anomalies" claim that was false
as first written, the colour-input correction (premise (iv)), the $N=1$ convention, the
mixed-symmetry exposure, the demotion of the constituent count to a corollary, the removal of an
unfailable flag from the pass count, and the replacement of "improvement in kind" with "improvement
in proximity". The first draft claimed more than this card does.

**Not yet armed.** The authoring session could not run `make gate`, `casim test`, `casim index` or
`make claims` — the device workspace was unavailable throughout. `confidence: medium` and
`last_verified` reflect the harness run described in F324 §11, not a gate run. Raise to
`confidence: high` only after the barrier is green and `make control` reproduces the eight declared
red sets.

## Sources

- `findings/F324-ncolour-bracket-closed.md`
- `findings/F317-su3-structure-derived.md` §6, §10 item 2 (the close this executes)
- `findings/F318-cell-carries-the-internal-index.md` §D (premise (ii); the double-count dissolved)
- `findings/F298-casimir-ladder-c7-rerun.md` §2 (the upper constraint, and its k-string restriction)
- `findings/F293-why-three-colours.md` §1, §4.2 (R1; the selector retired)
- `docs/claims/CL020-no-doublers-has-a-domain.md` (falsifier 1)
- `docs/claims/CL271-colour-structure-forced-by-one-index.md` (parent)
- Witten, *An SU(2) anomaly*, Phys. Lett. B **117** (1982) 324
- Bär & Wiese, *Can one see the number of colors?*, Nucl. Phys. B **609** (2001) 225 — **the prior art for the parity conclusion**
- Bär & Campos, *Global anomalies in chiral lattice gauge theory*, hep-lat/0001025 — the doubler-free lattice form
- Davighi, Gripaios & Lohitsiri, *Global anomalies in the Standard Model(s) and Beyond*, JHEP **07** (2020) 232 — the local↔global interplay under the $\mathbb Z_n$ quotients
- Wang, Wen & Witten, *A New SU(2) Anomaly*, 1810.00844 — the isospin-$\tfrac32$ caveat on non-spin manifolds
