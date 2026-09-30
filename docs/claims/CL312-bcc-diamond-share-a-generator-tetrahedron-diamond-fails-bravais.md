---
id: CL312
title: 'BCC and diamond-cubic share a generator tetrahedron; diamond-cubic fails the Bravais premise the model''s dimension selector already assumes'
slug: 'bcc-diamond-share-a-generator-tetrahedron-diamond-fails-bravais'
tier: supporting
kind: no_go
status: live
domain: [SM]
exactness: exact
findings: [F400, F291, F292]
tests: [F400-coordination-selector]
modules: [casim.engine.lattice.coordination_selector]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL246
falsifier: stated
first_issued: '2026-09-23'
last_verified: '2026-09-23'
provenance: authored
review_state: authored
confidence: high
---

# CL312 — BCC and diamond-cubic share a generator tetrahedron; diamond-cubic fails the Bravais premise the model's dimension selector already assumes

## Statement

The model's own BCC quantum-walk generator set — one regular tetrahedron of BCC's 8-vector nearest-neighbor coordination shell (Paper 2's Gram-matrix re-derivation, `references/qca-papers-1-4-overview.md` Eq. 20) — is vertex-for-vertex identical, as a set of integer vectors, to the standard diamond-cubic lattice's own coordination-4 nearest-neighbor bond tetrahedron. Despite that shared local geometry, diamond-cubic is not a Bravais (single-orbit) lattice: its two sublattices are related by the vector $(1/4,1/4,1/4)$ of the conventional cubic cell, which is not an integer combination of the FCC primitive lattice vectors (checked exactly in rational arithmetic), so no pure translation connects them. BDPT's uniqueness theorem for the model's $s=2$ Weyl walk is stated for a single abelian group $G\cong\mathbb Z^3$ acting on one orbit of sites — exactly the property diamond-cubic lacks. Consequently, the model's own dimension-selector machinery (F291/F292's S1/S2/S3, which take only a dimension $d$ and never a lattice type or coordination number — confirmed by direct inspection of their function signatures) cannot be "run against diamond-cubic instead of BCC" to produce a different verdict: diamond-cubic was never a competing $(s{=}2,\,G=\mathbb Z^3)$ candidate for those selectors to choose between in the first place. A genuine coordination-4 QCA would require either doubling the internal cell to $s=4$ (against BDPT's own minimality axiom, since $s=2$ already succeeds for BCC) or a non-abelian generator group extending $\mathbb Z^3$ — the "Non-Abelian extension" Paper 1 only sketches and never solves for $d=3$, here or in the cited literature.

## What it extends

BDPT's own axiomatic derivation of the Weyl QCA (Bisio–D'Ariano–Perinotti–Tosini 2015; Raynal 2017's Gram-matrix re-derivation) — specifically the scope of their stated uniqueness theorem, which this card shows is conditioned on the walk's group $G$ being abelian and single-orbit (Bravais), a premise ordinary crystallography's own coordination-4 example (diamond-cubic) fails independently of dimension. This sharpens, rather than contradicts, BDPT: their theorem was never claimed to rule out non-Bravais or non-abelian-$G$ constructions, and this card is the first place in this project's tree (or its six reference documents) that the diamond-cubic case is checked against that premise explicitly, rather than assumed settled by "BCC has the right point group" (D1, `docs/theory/key-decisions.md`).

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md` | The full derivation: BCC's $T_+$ tetrahedron = diamond's bond tetrahedron (exact integer Gram-matrix match); $(1/4,1/4,1/4)$ is not an FCC lattice vector (exact rational linear-algebra check, with a declared control verifying a genuine FCC vector *does* pass); `dimensionality.py`'s selector signatures carry no lattice/coordination-number parameter (inspected directly) | exact |
| `findings/F291-why-three-plus-one-dimensions.md`, `findings/F292-no-higher-multiple-of-three.md` | The S1/S2/S3 selector machinery this card shows cannot discriminate lattices, only dimensions | exact |
| `docs/theory/notebook-reconstruction-03-sigma-clifford-ca-lattice.md` (NB-044) | Diamond-cubic's coordination number measured directly at exactly 4, from real fractional-coordinate lattice geometry (not asserted by citation) | exact (direct geometric construction) |
| `references/qca-papers-1-4-overview.md` (Paper 1 Eq. 15/23, "Non-Abelian extension"; Paper 2 Eq. 18–20) | BDPT's own stated $G=\mathbb Z^3$ premise, the Dirac two-branch coupling this card's $s=4$ alternative is modeled on, and the never-solved non-abelian sketch | cited, not re-derived |

## Falsifier

1. **Exhibit a homogeneous $s=2$ QCA on diamond-cubic's full two-sublattice point set using pure $\mathbb Z^3$ (FCC) translations only, satisfying BDPT's five axioms.** This card's central claim (no pure translation connects the sublattices) would be directly contradicted — it is an exact rational-arithmetic computation and should not be findable, but is stated as a falsifier for completeness.
2. **Build the non-abelian-$G$ extension of Paper 1's sketch into a genuine $d=3$, coordination-4 walk reproducing this model's own required physics (F26/F27's speed of light, F69's photon).** This would not falsify anything this card asserts (it explicitly leaves route (b) unexplored) but would show the "why BCC not diamond" question has a live, uninvestigated alternative construction after all — narrowing this card's scope rather than overturning it.

## Status & history

First issued 2026-09-23, from `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md`, itself a direct response to `docs/theory/notebook-v2/01-thread-map.md` row T01/T10 and `docs/theory/notebook-v2/index.md` §5 Prompt D. Rolls up to `CL246` (F291's own "why $d=3$" card) as the specific coordination-number/lattice-type half of that broader dimension-selection claim; `status: live` and independent of CL246's own review state. No prior status to narrate.

## Sources

- `findings/F400-bcc-vs-diamond-cubic-coordination-selector.md`
- `findings/F291-why-three-plus-one-dimensions.md`
- `findings/F292-no-higher-multiple-of-three.md`
- `references/qca-papers-1-4-overview.md` — Paper 1 (BDPT 2015) Eq. 15/23 and the Non-Abelian extension sketch; Paper 2 (Raynal 2017) Eq. 18–20
- `docs/theory/notebook-reconstruction-01-scalar-qft-opening.md` (NB-005/006, tetrahedron isomer counting)
- `docs/theory/notebook-reconstruction-03-sigma-clifford-ca-lattice.md` (NB-044, diamond-cubic coordination measured)
- `docs/theory/notebook-v2/01-thread-map.md` row T01/T10; `docs/theory/notebook-v2/index.md` §5 Prompt D — the question this card answers
