---
id: CL290
title: 'Majorana is the required completion of this model''s own hypercharge derivation, conditional on no protecting symmetry existing and F165/F279 standing'
slug: majorana-neutrino-structurally-forced
tier: supporting
kind: reinterpretation
status: contingent
domain: [SM]
exactness: exact
findings: [F341, F47, F165, F202, F266, F279]
tests: [F341-majorana-forced-by-hypercharge-closure]
modules: [casim.constants.electroweak, casim.engine.gauge.hypercharge]
constants: [Y_NU_R, Y_LEPTON_L, Y_E_R]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-31'
last_verified: '2026-08-31'
provenance: authored
review_state: authored
confidence: medium
---

# CL290 — Majorana is the required completion of this model's hypercharge derivation

## Statement

Within this model's own structure, the right-handed neutrino $\nu_R$ is Majorana, not Dirac-only:
no gauge or global symmetry registered anywhere in the model forbids the F47 Higgs-free Majorana
bilinear $\nu_R^{\mathsf T}C\nu_R$ (its only gauge charge, $Y=0$, permits rather than forbids the
term), and removing that term would reopen the model's own gate-tier, machine-verified F165/F279
hypercharge-quantisation closure — a Dirac-only completion leaves the hypercharge normalisation
$y_\phi$ (and hence the derived quark-charge fractions $\tfrac23,-\tfrac13$) as a free, undetermined
second input rather than the single derived normalisation the project currently certifies.

## What it extends

Standard-Model neutrino phenomenology leaves Dirac vs Majorana genuinely undetermined by symmetry
alone — the Standard Model (with $\nu_R$ added as a singlet) has no analogous mechanism forcing
either option, and the physical question is resolved only empirically (neutrinoless double-beta
decay). This claim asserts that *this model's* additional structure (Higgs-free hypercharge
quantisation derived from anomaly cancellation plus one Majorana closure row, F165/F279) breaks
that degeneracy internally: consistency with an already-certified result of the same model requires
the Majorana option. It is a structural/consistency argument, not a new gauge-invariance no-go —
the SM itself is not extended by a new exclusion theorem, only this model's internal derivation is
shown to depend on the choice.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F47-majorana-seesaw-higgs-free.md` | Constructs the Higgs-free, R-unitary, gauge-invariant Majorana step; $Y_{\nu_R}=0$ structurally forced | exact / machine |
| `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md`, `findings/F279-hypercharge-constraint-attribution.md` | Establishes the gate-tier hypercharge closure this claim shows depends on the Majorana row | exact ($\mathbb{Q}$) |
| `findings/F202-leptogenesis-from-intrinsic-L-violation.md` | The model already treats $L$-violation as load-bearing (leptogenesis), evidence against an unstated protecting symmetry | structural |
| `findings/F341-majorana-forced-by-hypercharge-closure.md` | This claim's own finding: S1 (no protecting-symmetry generator registered) + S2 (dropping the Majorana row reopens F165/F279 to a 2-parameter family, with control) | exact ($\mathbb{Q}$), machine-verified |
| `tests/registry/particles.yaml` record `F341-majorana-forced-by-hypercharge-closure` | 5/5 checks PASS, `casim test` verified | exact |

## Falsifier

**Structural falsifier (would break this claim without needing new observation):** the discovery, anywhere in the model's own construction, of a global or gauged symmetry under which $\nu_R$ carries a nonzero charge independent of $Y$ (a genuine lepton-number or $B\!-\!L$ generator arising from the CA rule itself, not added by hand) would remove the "no protecting symmetry" leg (S1) and, if it also forbade the Majorana bilinear, would reopen row C4 to a Dirac-only possibility that does not sacrifice F165/F279 (if the same symmetry supplied an alternative closing constraint).

**Empirical falsifier, external to the model:** this claim does not predict a specific $0\nu\beta\beta$ half-life or effective Majorana mass — the model has not derived the absolute scale $M_R$ (ledger row D4, still OPEN) needed to compute one. The claim is falsified in the ordinary particle-physics sense only if neutrinos are shown empirically to be Dirac (e.g., via a lepton-number-conserving discriminator with no viable Majorana loophole), which is not the same question as, and does not bear directly on, this model's *internal* structural argument.

## Status & history

`status: contingent` because the claim rests explicitly on the model's already-certified F165/F279 hypercharge closure remaining correct — if a future finding overturns F165/F279 (e.g. finds an independent route to $y_\phi=3y_Q$ that does not need the Majorana row), the S2 leg of this claim's evidence dissolves and the claim would need to be reopened or withdrawn, even though S1 (no protecting symmetry) would be unaffected. First issued 2026-08-31 from F341; not narrowed or superseded.

## Sources

- `findings/F341-majorana-forced-by-hypercharge-closure.md`
- `findings/F47-majorana-seesaw-higgs-free.md`
- `findings/F165-hypercharge-quantisation-from-anomaly-and-mass.md`
- `findings/F202-leptogenesis-from-intrinsic-L-violation.md`
- `findings/F266-sterile-neutrino-dark-matter.md`
- `findings/F279-hypercharge-constraint-attribution.md`
- `docs/reviews/F341-review-2026-08-31.md` (cold-subagent adversarial review, CONFIRMED-NARROWER)
- `tests/registry/particles.yaml` record `F341-majorana-forced-by-hypercharge-closure`
- Schechter, J. & Valle, J. W. F. (1982), "Neutrinoless double-beta decay in SU(2) x U(1) theories", *Phys. Rev. D* 25, 2951 -- the "black-box theorem" external anchor named in F341
- KamLAND-Zen Collaboration (2024), arXiv:2406.11438 -- current experimental T_1/2 > 3.8e26 yr / m_bb < 28-122 meV bound, external empirical anchor named in F341
