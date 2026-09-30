---
id: CL316
title: 'Koide pseudo-masses cannot explain the quark hierarchy in this model: with lepton-like amplitudes they are incompatible with the CKM, and with a signed down sector they fit it for any E_g angle pair in a band, predicting nothing'
slug: 'koide-pseudomass-quark-route-nonpredictive'
tier: supporting
kind: no_go
status: open
domain: [SM]
exactness: quantitative
findings: [F404, F407]
tests: [F404-koide-pseudomass-fork, F407-koide-pseudomass-minimal]
modules: [casim.engine.forks.particles.koide_pseudomass_fork, casim.engine.forks.particles.koide_pseudomass_minimal]
constants: []
supersessions: []
reviews: [docs/reviews/F404-review-2026-09-24.md]
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-24'
last_verified: '2026-09-24'
provenance: authored
review_state: authored
confidence: medium
---

# CL316 — The Koide pseudo-mass route does not explain the quark hierarchy

## Statement

Give each quark sector a Hermitian amplitude matrix $S_f$ on the $T_{1u}$ triplet whose diagonal is exact Koide ($Q=2/3$) at an E_g angle $\delta_f$, with $T_{2g}$/$T_{1g}$ off-diagonals carrying the Q deviation and the CKM. Then (i) exactly, $Q_\text{phys}-Q_\text{pseudo}=\lVert S_\text{off}\rVert_F^2/(\operatorname{tr}S)^2$, so quarks need off-diagonal weight $0.427$ (up) and $0.254$–$0.394$ (down) of $\operatorname{tr}S$ while charged leptons need none; (ii) exactly, CP violation requires the $T_{1g}$ component; (iii) with all amplitudes positive, as for the leptons, exact Koide in both sectors and the measured CKM cannot hold together (smallest Koide violation among CKM-holding solutions $2.1\times10^{-2}$ of $\operatorname{tr}S$); (iv) with $-\sqrt{m_d}$, angle pairs in a band $-0.05\lesssim\delta_D-\delta_U\lesssim0.1$ (including universal δ\*) fit the CKM at the unitary floor ($\chi^2=0.119$ for $\lvert V_{us}\rvert,\lvert V_{cb}\rvert,\lvert V_{ub}\rvert,\lvert V_{td}\rvert,J$, a floor set by tension inside the mixed direct/global-fit input set), and off-band pairs fail. So the route predicts no CKM observable; its only output is a correlation between the two sector angles. (v) The same holds for the report's *minimal* ansatz (three real $T_{2g}$ amplitudes and one $T_{1g}$ amplitude, 9 parameters against 10 observables, Jacobian rank 9, F407). Fitting masses and CKM with errors, every candidate pair fits at $\Delta\chi^2\le1$ in both mass schemes, with $m_s$ unpulled and a signed down sector chosen by the fit, lightest or middle amplitude negative. With all-positive amplitudes the fit closes only at $m_s\approx27$ MeV (mixed) or $12.6$ MeV ($M_Z$), about a quarter of the PDG value, and GST $\lvert V_{us}\rvert\approx\sqrt{m_d/m_s}$ does not emerge when $\lvert V_{us}\rvert$ is held out.

## What it extends

The Koide relation's extension to quarks through weak-basis "pseudo-masses" (Gérard–Goffinet–Herquet, PLB 633 (2006) 563; Żenczykowski, arXiv:1301.4143), and the Standard Model's quark Yukawa sector, where masses and CKM are ten free inputs. The claim is that this route, built on the model's $O_h$ generation structure, does not reduce that count.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F404-koide-pseudomass-quark-fork.md` | The trace identity, Schur–Horn angle windows, the joint search in both mass schemes, the unitary-floor comparison | exact (P1, P6) + quantitative / numerical (P2–P5, P7) |
| `findings/F407-koide-pseudomass-minimal-quark-fit.md` | The minimal ansatz: parameter count and rank, candidate-pair fits in both schemes, all-positive $m_s$ profile, GST non-emergence, δ landscape | quantitative / numerical |
| record `F407-koide-pseudomass-minimal` → `test-results/F407_koide_pseudomass_minimal.json` | 7/7 legs (mixed; $M_Z$ by `--param`); controls `t1g=false` and `force_positive=true` (both: M2 × 3 red) | quantitative |
| record `F404-koide-pseudomass-fork` → `test-results/F404_koide_pseudomass_fork.json` | 8/8 legs; controls `down_signs=+++` (P3, P4b, P7 red), `ckm_weight=0` (P4a red) and `koide_weight=1e4` (P4a red) verified | quantitative |

## Falsifier

(iii) is a numerical search result: a single explicit pair $U_U$, $U_D$ with all-positive exact-Koide diagonals whose $U_U^\dagger U_D$ matches the CKM moduli and $J$ within 2σ would refute it. (i) and (ii) are identities and cannot be falsified by data; they fall only if the amplitude-matrix reading of F78 is abandoned. (iv) would be overturned by a lattice principle that fixes $\delta_U$, $\delta_D$ and the off-diagonal textures, reducing the parameter count below ten; that would be a new finding, not a correction to this one.

## Status & history

2026-09-24 - 17:05: extended by F407 (report derivation three). The minimal ansatz, a subset of F404's, passes the report's failure test ($m_s$ not pulled with signed amplitudes) and is still non-predictive: one degree of freedom, spent on nothing. Clause (v) added; the title's "negative lightest down amplitude" now reads more generally, since the middle-negative branch also fits.

2026-09-24 - 15:30: narrowed by the independent review (CONFIRMED-NARROWER, `docs/reviews/F404-review-2026-09-24.md`). The all-positive minimum violation was corrected from $1.9\times10^{-3}$ (a penalty compromise that abandoned the CKM) to $2.1\times10^{-2}$, which strengthens (iii). "Every admissible pair fits" was replaced by the band result in (iv).

`open`, first issued 2026-09-24 with F404. The route is kept as a fork (`forks/particles/koide_pseudomass_fork.py`, `fork_live`) because it preserves the exact constraints (i), (ii) and the Schur–Horn exclusion of a universal δ\* with all-positive down amplitudes, which any future quark mechanism in the model must satisfy.

## Sources

- `findings/F404-koide-pseudomass-quark-fork.md`
- `reports/Quark neutrino hierarchy lattice fit.md` (2026-09-24), route 1
- PDG 2025 quark masses and CKM review; Antusch–Hinze–Saad arXiv:2510.01312 (running masses at $M_Z$)
