---
id: CL273
title: The model's UV sensitivity reduces to exactly two operator coefficients with no free parameter, and both are Sakharov sectors
slug: uv-sensitivity-ledger-two-unabsorbable-coefficients
tier: headline
kind: reinterpretation
status: live
domain: [QFT, GR]
exactness: exact
findings: [F319, F264, F164, F59, F79, F116, F284]
tests: [F319-uv-completion]
modules: [casim.engine.interactions.qed_uv_completion]
constants: [c_lat, a_over_ellP, ell_P_m]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-16
last_verified: 2026-08-16
provenance: authored
review_state: authored
confidence: high
---

# CL273 — The UV-sensitivity ledger: exactly two unabsorbable coefficients

## Statement

On a lattice with a physical Brillouin-zone cutoff there are no divergences, so the four QED
counterterms $\{Z_1,Z_2,Z_3,\delta m\}$ are **finite reparametrisations** from bare lattice
parameters to measured ones, not subtractions of infinities. Enumerating every operator with
superficial degree $D\ge0$ in the full theory including gravity, and asking of each whether the
model has a free parameter to absorb its cutoff-dependence, leaves **exactly two coefficients
that it does not**: the cosmological constant ($D=4$) and the Einstein–Hilbert term
($D=2$, $1/16\pi G$). These are precisely the two Sakharov sectors F59 separated by their
$\Lambda$-scaling. The model predicts one correctly ($G$, structural via F79 at the F107 cell)
and overshoots the other by $10^{120.76}$ ($\rho_\text{vac}$, F164). The photon mass is a third
$D\ge0$ operator with no free parameter, but it is **forbidden** by exact transversality
($q_\mu\Pi^{\mu\nu}=0$, F251/Pi1) rather than unabsorbable, and is not counted.

## What it extends

Reinterprets the Dyson–Ward renormalisation programme of QED, and Sakharov's induced gravity,
as one finite ledger. Standard QFT treats renormalisability as the absorbability of divergences
into finitely many counterterms; on a physical cutoff the same power-counting theorem
($D=4-\tfrac32E_f-E_\gamma$ with $\partial_VD=\partial_LD=0$, F264 R1) becomes the strictly
stronger and entirely finite statement that finitely many operator coefficients carry the
cutoff. Same numbers; different ontology — hence `kind: reinterpretation`.

The ledger is not merely a restatement: it converts the cosmological-constant problem from
"the model inherits it" (F164) into a *counted* residual — the model's UV freedom is 4 absorbable
plus 2 unabsorbable coefficients, and A11's open item is one named number.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §7 | the ledger; exactly two unabsorbable | exact |
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §3 (U1–U4) | scheme differences are IR-independent, which is what licenses the counterterms | machine ($2.0\times10^{-12}$) |
| `findings/F264-qed-allorders-renormalizability-anomaly.md` R1–R3 | the power counting and the four-element counterterm closure | exact |
| `findings/F59-induced-eh-prefactor-and-f10-selection.md` Part A | the $\Lambda^2$ / $\Lambda^4$ sector split | derived |
| `findings/F164-cosmological-constant-120-orders-and-candidate-cancellations.md` Part B | $\rho_\text{vac}/\rho_\Lambda=5.8\times10^{120}$ | computed |
| record `F319-uv-completion`, legs `U9-D-order-independent`, `U9-exactly-two-unabsorbable` | 21/21 PASS | exact |

## Falsifier

1. Exhibiting a third $D\ge0$ operator, gauge- and Lorentz-invariant, with no free parameter to
   absorb it and not forbidden by an exact identity. The enumeration is finite and explicit in
   `UV_LEDGER`, so this is checkable row by row.
2. Showing that one of the four QED coefficients is *not* free in the model — which would
   **strengthen** the ledger rather than break it (fewer free parameters), and is expected as
   F115/F116/F251 land; the card would then be narrowed, not withdrawn.
3. A measured infrared dependence of the lattice-vs-continuum scheme constant, which would
   remove the licence for treating F264's counterterms as absorbing the lattice's cutoff
   dependence.

## Status & history

Issued 2026-08-16 against completeness row A11, which had read `PARTIAL` and "unmoved for three
reports" with the diagnosis that the physical-cutoff picture (F116/F164/F284) and the
counterterm picture (F264) were "both individually sound, nowhere reconciled". The reconciliation
is Wilsonian and was absent from the tree — `wilson` in this repo returned only the Wilson gauge
action and the Wilson $\Lambda_{\overline{\rm MS}}$ constant, never Wilson's renormalisation
group. This card is the reconciliation's standing form.

The `free parameter?` column is a judgement about the model's structure stated operator by
operator so it can be disagreed with row by row; F319 §9 flags it as such.

## Sources

- `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md`
- `src/casim/engine/interactions/qed_uv_completion.py` (`UV_LEDGER`, `superficial_degree`)
- `docs/status/completeness-2026-08-07.md` row A11
