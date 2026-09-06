---
id: CL259
title: 'BBN and the free-neutron lifetime bound m_n - m_p to +-0.0056 MeV; the model''s own derived +1.51 MeV differs from measurement by 0.217 MeV but is NOT excluded once its own literature-informed theory uncertainty (+-0.280 MeV, F372) is propagated'
slug: bbn-bounds-np-splitting
tier: supporting
kind: no_go
status: narrowed
domain: [QCD, cosmology, SM]
exactness: quantitative
findings: [F297, F122, F123, F40, F372]
tests: [F297-bbn-light-elements, F372-npsplit-theory-uncertainty]
modules: [src/casim/engine/interactions/cosmology_bbn.py, src/casim/engine/particles/baryon_dynamics.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-05'
last_verified: '2026-09-05'
provenance: authored
review_state: authored
confidence: high
---

# CL259 — BBN measures $m_n-m_p$, and the model's value is excluded

## Statement

Primordial helium at fixed $\eta_b$ pins the neutron–proton mass splitting to
$m_n-m_p=1.293\pm0.0056$ MeV ($1\sigma$; $\partial Y_p/\partial\Delta m=-0.607\ \text{MeV}^{-1}$).
The model's derived value, $+1.51$ MeV (F122/F123), gives $Y_p=0.1210$ ($-36.6\sigma$),
$\mathrm{D/H}=1.85\times10^{-5}$ ($-22.6\sigma$), and a free-neutron lifetime of **330.8 s**
against the measured $878.4\pm0.4$ s.

**The sign is not in question and is not being retracted.** F122's actual claim — that the
down–up current-mass gap beats the proton's larger electromagnetic self-energy, so the neutron is
heavier — stands. What this card originally asserted is that the *value* is excluded and that
F122's acceptance criterion was three orders of magnitude too loose: check S8b tested "within 1
MeV"; BBN tests to $\pm0.0056$ MeV, a factor **179**.

**Narrowed by F372 (2026-09-05).** The 0.217 MeV gap and the 179x tightening both stand — BBN
really does pin $\Delta m$ that sharply. What does **not** stand is treating the model's *point*
$\Delta m=1.51$ MeV as if it carried zero theoretical uncertainty when judging whether it is
*excluded*. F372 checked both of F297 Sec.10's named fixes (the EM self-energy against the model's
own P2 wavefunction and two external determinations; the F40 strong gap against PDG 2024 and BMW
2015) and found neither term wrong by anywhere near the needed size — the model's decomposition
matches BMW 2015's ab initio lattice QCD+QED result to $\le1\%$ term-by-term, and BMW's own total
sits the *same* $\sim0.22$ MeV from the measured value that the model's does. Propagating BMW's own
combined uncertainty ($\pm0.280$ MeV) onto the model's $\Delta m$ drops the significance from
$36.6\sigma$ (this card's original number) to $\mathbf{0.77\sigma}$ — and every other defensible
theory-uncertainty composition F372's own review pass tried (Thomas-Wang-Young's EM-only figure
alone, or that figure combined with PDG 2024's quark-mass uncertainty) stays in the
$0.77$–$1.97\sigma$ range, under the $2\sigma$ threshold in every case. The measured neutron
lifetime (878.4 s) and $Y_p$ (0.2453) both fall inside the $\pm1\sigma$ band BMW's figure
propagates onto them. **Not excluded, at every composition tried — though the margin is
uncertain by roughly a factor of two depending on the composition, not a single comfortable
number.**

## What it extends

The Standard Model takes $m_n-m_p$ from experiment. This model derives it, from the F40 current-quark
gap ($+2.51$ MeV) minus a constituent-quark Coulomb self-energy difference ($-1.00$ MeV). Once the
model also owns the expansion rate, BBN becomes an internal consistency condition on that derivation
rather than an external datum — and the condition fails.

Exactly one statement follows: **one of the two terms is wrong by 0.217 MeV** — $8.6\%$ of the
strong term, or $21.7\%$ of the electromagnetic one. On size grounds the EM term is the likelier
culprit: $22\%$ is an ordinary error for a Coulomb self-energy estimated from a constituent-quark
charge distribution, whereas $8.6\%$ on the F40 gap would move $m_d/m_u$ outside its PDG range.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F297-bbn-light-element-abundances.md` §5 | the bound, the exclusion and the decomposition | quantitative |
| `tests/registry/interactions.yaml` → `F297-bbn-light-elements` | checks K2-8, K2-9; and the declared red control `--param delta_m_mev=1.51` | quantitative |
| `src/casim/engine/interactions/cosmology_bbn.py` → `neutron_lifetime` | the $\tau_n$ leg, which needs no network at all | quantitative |
| `test-results/F297_bbn_light_elements.json` | the numbers | quantitative |

The $\tau_n$ leg is the sharper of the two and is independent of every network assumption: the
free-decay phase-space integral $f(q)$ rises steeply in $q=\Delta m/m_e$, and the coupling $K$ is a
constant that does not depend on $\Delta m$, so re-using the value calibrated at the measured
splitting is legitimate. A cross-check on that coupling — computing $K$ instead from the model's own
$G_F$ and the registry $g_A$ (plus external $|V_{ud}|$) — gives $\tau_n=948$ s against 878.4
measured, $+7.9\%$, the expected size of the omitted Coulomb and radiative corrections. **The
coupling side is sound; the $\Delta m$ side is not.**

## Falsifier

This card is killed by any of:

1. A re-derivation of the F122 decomposition landing inside $1.293\pm0.0056$ MeV — which is the
   *intended* outcome and the point of stating the band. **Not achieved by F372**: F372 checked this
   directly (both named branches) and found no term-level correction of the needed size is
   supported by any independent method surveyed. The card is narrowed, not killed, by this route.
2. A demonstration that $\partial Y_p/\partial\Delta m$ is materially different from
   $-0.607\ \text{MeV}^{-1}$, which would loosen the band. The derivative is measured inside the
   same network by finite difference at $\pm0.02$ MeV. Unaffected by F372.
3. Any error in the free-decay phase-space integral large enough to move $\tau_n(1.51\ \text{MeV})$
   from 331 s to within the measured $878.4\pm0.4$ s — a factor 2.7, which no plausible correction
   supplies. **Superseded by F372's actual resolution**: no error in the phase-space integral was
   needed or found; propagating $\Delta m$'s own $\pm0.280$ MeV theory uncertainty (not a
   correction to the integral) already puts 878.4 s inside the resulting $[120.7,1225.1]$ s band.

## Status & history

`live` as of 2026-08-05, issued together with CL258 by F297. **Narrowed to `narrowed` on
2026-09-05 by F372**, which checked F297 Sec.10's own named fixes and found neither survives an
independent check (the model's EM term matches its own P2 wavefunction to 3.2% and two external
determinations to $\le4\%$; its strong term matches PDG 2024 to 0.8%), then corrected the
significance test itself: the model's $\Delta m$ estimate carries a real, literature-quantified
$\sim0.280$ MeV theory uncertainty (BMW 2015's own combined stat+sys), and against that the
$36.6\sigma$ exclusion becomes $0.77\sigma$ — not excluded. Nothing in
`findings/F297-bbn-light-element-abundances.md` or `findings/F122-p2-dynamical-baryon-three-body.md`
was edited: F372 is its own finding, per D12.

**Bearing on CL109.** `CL109` is the `unreviewed-seed` card carrying F122. Its `Statement` is the
finding's title and does not assert the splitting *value*, so it is not narrowed by this card — but
F122's own S8 check is, and a note recording that has been added to CL109's history so the two cards
cannot drift apart. Nothing in `findings/F122-p2-dynamical-baryon-three-body.md` was edited: a card may move without a finding
moving, which is the whole point of the layer (D12).

This is filed as `kind: no_go` because that is what it is — an option the model has closed, and its
own. `no_go` cards are the falsification record and are the last thing that should ever be archived.

## Sources

- `findings/F297-bbn-light-element-abundances.md`
- `findings/F122-p2-dynamical-baryon-three-body.md`, `findings/F123-p6-si-scale-matter-sector.md`
- `findings/F372-npsplit-theory-uncertainty.md`
- `docs/claims/CL258-bbn-light-elements.md`, `docs/claims/CL109-p2-the-dynamical-baryon-a-real-time-non.md`
- PDG 2024 ($\tau_n$, $m_n-m_p$, $m_d/m_u$); Aver et al. 2021; Cooke, Pettini & Steidel 2018
- Borsanyi et al. (BMW collaboration) 2015, *Science* 347, 1452 (arXiv:1406.4088)
- Thomas, Wang & Young 2015, *Phys. Rev. C* 91, 015209 (dispersive Cottingham sum rule)
