---
id: CL168
title: 'The model-native emergent-gravity (\"dark matter without dark matter\") route, falsified by the Bullet-Cluster lensing/gas offset'
slug: 'the-model-native-emergent-gravity-dark-matter-without'
tier: supporting
kind: no_go
status: live
domain: [cosmology]
exactness: machine
findings: [F194, F358]
tests: []
modules: []
constants: []
supersessions: [S23-F194-bullet-cluster-clump-shape-claim]
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-04'
last_verified: '2026-09-03'
provenance: extracted
review_state: unreviewed-seed
confidence: medium
---

# CL168 — The model-native emergent-gravity ("dark matter without dark matter") route, falsified by the Bullet-Cluster lensing/gas offset

## Statement

The model-native emergent-gravity ("dark matter without dark matter") route, falsified by the Bullet-Cluster lensing/gas offset

## What it extends

*Not yet established by a reviewer.* This card was extracted mechanically from `findings/F194-emergent-gravity-bullet-falsification.md`; its `domain`, `kind` and `exactness` were inferred from the finding's own title and `**Status:**` line and **have not been confirmed**. The bar in `docs/claims/README.md` — that a card names the specific established result in QM / SM / GR / SR / QFT it derives, extends or contradicts — is **not yet met by this card**. Meeting it is what promotion to `review_state: authored` consists of.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F194-emergent-gravity-bullet-falsification.md` | The finding, in full | machine |
| `findings/F358-bullet-cluster-reexamination.md` | 2026-09 re-examination: the observational offset anchor is reconfirmed/sharpened by JWST (Rihtaršič et al. 2026); F194's own "regardless of clump shape" over-claim is withdrawn (ledger S23); the bottom-line verdict (dark source required) is independently reinforced by the MOND community's own 2026 internal Hernandez/Famaey dispute | machine (literature synthesis, no new computation) |

**This card's only evidence for the F194 half is the prose of its own finding.** That is what `review_state: unreviewed-seed` means, and it is why the card may not be cited as independent support for that half. F358 is an independent, outside-literature cross-check on the discriminator itself, not a re-derivation of F194's toy model. Promoting the card to `authored` still means naming the test-registry records and result artifacts that carry it, and confirming the classification above by hand.

## Falsifier

**Stated (added 2026-09-03, per F358).** This exclusion would be undercut by either:

1. an independently reproduced QUMOND/MOND-class calculation, using only directly observed baryonic mass (no extrapolated, non-standard stellar-remnant IMF), that matches the **full** Bullet-Cluster convergence ($\kappa$) profile — not just the offset centroid; or
2. independent verification, in external cluster ellipticals, of the top-heavy IGIMF stellar-remnant budget Zhang et al. (2026, arXiv:2606.19454) use to close the residual.

As of 2026-09, neither has happened: Hernandez's 2026 attempt at (1) (arXiv:2604.10811) was shown quantitatively insufficient by Famaey (arXiv:2605.10022, same year), and (2) is disputed by independent commentators (R. Massey, K. Romer, quoted in *Physics World*, 2026) as an unverified extrapolation. See `findings/F358-bullet-cluster-reexamination.md` for the full account.

## Status & history

`live`, inferred from the finding's own status line, quoted here verbatim so the inference is checkable:

> Confirmed — 5/5 checks PASS. The acceleration-scale derivation (E1) and the QUMOND solver self-consistency (E3) are quantitative/machine-level; the Bullet-Cluster falsifier (E4) is a 3D toy whose **conclusion is a robust topological discriminator**, not a parameter fit. This builds the one gravity-*side* dark-matter candidate that the catalog (§4) and [[F191-dark-matter-rotation-curves-bullet]] left open, and shows it fails the same test that breaks MOND at cluster scales.

**Date:** 2026-06-30 - 15:10

Seeded 2026-08-04 as part of standing up the claims layer (D12). No physics was read, changed or judged in creating this card.

**2026-09-03 update (F358, ledger S23):** re-examined per the E13 reopening-condition protocol. The word "topological" in F194's own status line above, and the stronger "regardless of... clump shapes" claim it rests on, are **withdrawn** — a live 2026 MOND/QUMOND-literature mechanism (Hernandez, arXiv:2604.10811) is a genuine counterexample to the strict form of that claim. The card's `status` stays `live` and `kind` stays `no_go` because the underlying verdict is unaffected: the best current, independently adjudicated (Famaey, arXiv:2605.10022) quantitative treatment of that same mechanism against the sharpest available (JWST) data still requires additional collisionless mass. No physics in this model changed; this update reflects an external-literature re-check only.

## Sources

- `findings/F194-emergent-gravity-bullet-falsification.md`
- `findings/F358-bullet-cluster-reexamination.md`
- `docs/theory/supersessions.yaml` — record S23-F194-bullet-cluster-clump-shape-claim
- `docs/claims/README.md` — the `unreviewed-seed` contract
