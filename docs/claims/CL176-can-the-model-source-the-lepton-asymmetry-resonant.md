---
id: CL176
title: 'The model''s own Sakharov ingredients are structurally present, but neither of the two free residuals — CP phase, N₂,₃ degeneracy — reaches the observed baryon asymmetry at the model''s own native F201 masses without further, unexplained fine-tuning'
slug: 'can-the-model-source-the-lepton-asymmetry-resonant'
tier: supporting
kind: no_go
status: narrowed
domain: [SM, cosmology]
exactness: bracketed
findings: [F202, F364, F201, F47, F53, F320]
tests: [F364-baryogenesis-boltzmann]
modules: [src/casim/engine/forks/darkmatter/dm_fork_F364_baryogenesis_boltzmann.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-08-04'
last_verified: '2026-09-04'
provenance: authored
review_state: authored
confidence: medium
---

# CL176 — Can the model source the lepton asymmetry? Ingredients yes; native magnitude no

## Statement

All three Sakharov conditions for the observed baryon asymmetry are met by the model's own
structure: L-violation is **derived** (F47's anti-linear Majorana seesaw step), CP violation is
**available** (F53: the three-generation lepton sector carries 1 Dirac + 2 Majorana phases), and
out-of-equilibrium decay plus fast SU(2)_L sphalerons ($\Gamma_\text{sph}/H\sim10^{16}$ at
$T_\text{sph}=131.7$ GeV, using the model's own $\sin^2\theta_W=2/9$, F320) supply the rest. F364
turns this from a conditions checklist into an actual computed $Y_B=n_B/s$ using a leading-order,
unflavoured resonant-leptogenesis Boltzmann code: Casas–Ibarra Yukawas fit exactly to measured
oscillation data, sitting on top of the model's **own**, untuned F201 Z₃/E_g heavy-neutrino masses
($M_2\approx0.40$ GeV, $M_3\approx5.60$ GeV, native split $\Delta M/M\approx1.73$, order-unity).
Neither of the two free residuals F202 named — the CP phase, the $N_{2,3}$ mass-splitting — reaches
the observed $Y_B=8.7\times10^{-11}$ on its own at that native point: the CP-phase lever caps
$\sim10$–$11$ decades short even pushed to the edge of perturbativity, and the degeneracy lever
*can* resonantly reach/exceed the observed value, but only in a window $\Delta M/M\in[3\times10^{-18},\,
3\times10^{-17}]$ — roughly $16$–$17$ orders of magnitude finer than the texture's own native split.

## What it extends

Standard thermal/resonant leptogenesis (Fukugita–Yanagida 1986; Pilaftsis 1997; Pilaftsis–Underwood
2004's mass-splitting-regulated CP asymmetry, valid at any $\Delta M$, not only exact degeneracy;
the "vanilla" Boltzmann transport equations of Kolb–Wolfram 1980 and Buchmuller–Di Bari–Plümacher
2004; the ARS/νMSM GeV-seesaw picture of Akhmedov–Rubakov–Smirnov 1998, Asaka–Shaposhnikov 2005,
and Drewes–Garbrecht 2013's freeze-in-without-imposed-degeneracy treatment) applied, without
modification to the transport equations themselves, on top of this model's own derived Type-I
seesaw sector (F47) and its own texture-fixed heavy masses (F201) rather than free input masses.
The physics being extended is the standard Boltzmann-equation machinery of baryogenesis via
leptogenesis; what is model-specific is only the input mass spectrum and Yukawa freedom, both taken
from the model's own prior structure rather than tuned to fit $Y_B$.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F202-leptogenesis-from-intrinsic-L-violation.md` | All three Sakharov conditions met structurally; magnitude explicitly not attempted (5/5 PASS, structural — not re-attacked here) | unset |
| `findings/F364-baryogenesis-boltzmann.md` | Full Boltzmann computation of $Y_B$ from the model's own F201 masses + Casas–Ibarra Yukawas; CP-phase scan and mass-splitting resonance scan, both bracketed | bracketed |
| `tests/findings/test_F364_baryogenesis_boltzmann.py` → `test-results/F364_baryogenesis_boltzmann_test.json` | 7/7 checks PASS: seesaw round-trip, fast sphalerons, native split order-unity, CP-phase shortfall bracketed, resonance peak $\ge$ observed, required-degeneracy window $\ge10^{10}\times$ finer than native, solver success | bracketed |
| `test-results/F364_baryogenesis_boltzmann.json` | Full scan data: CP-phase table, mass-splitting resonance table, sphaleron rate table | bracketed |

## Falsifier

The claim (native-parameter shortfall) would be falsified by either lever closing the gap without
the fine-tuning identified: a revised/independent computation showing the CP-phase-only channel
reaching $|Y_B/Y_B^\text{obs}|\gtrsim1$ at the model's own native F201 masses without invoking
non-perturbative Yukawas, or a re-derivation of the F201 texture (at the same keV-DM-producing
node, $M_{R0}=1$ GeV, $\delta_\nu=134.86°$) showing a native $N_{2,3}$ split below
$\Delta M/M\sim10^{-16}$ rather than the found $\Delta M/M\approx1.73$. Separately, the *specific*
resonance window found here ($\Delta M/M\in[3\times10^{-18},3\times10^{-17}]$ for $Y_B\ge Y_B^\text{obs}$)
is itself a falsifiable computation: a re-run with the same inputs landing outside this window would
falsify the F364 result on its own terms.

## Status & history

**Narrowed 2026-09-04 (F364).** The claim as first stated (2026-08-04, `unreviewed-seed`, extracted
mechanically from F202's title) was: *"Can the model source the lepton asymmetry? Yes — all three
Sakharov conditions are met."* That qualitative "yes" still stands and is unchanged (F202's 5/5 PASS
was not re-attacked). What was too broad is the implication, latent in the unqualified "Yes," that
the model's own natural parameter landing point is *sufficient* — F364 shows it is not: at F201's
own native masses, neither free residual (CP phase alone; mass-splitting alone) reaches the observed
asymmetry without an additional, currently unexplained input (either near-maximal CP violation deep
in a washout-limited regime, or a $\sim16$-order-of-magnitude finer $N_{2,3}$ degeneracy than the
texture naturally supplies). The narrow, now-quantified form of the claim is stated above.

Original seed status line, quoted for the record:
> **Sakharov-conditions check passes structurally; magnitude not derived.** This certifies that the
> ingredients exist in the model's own established structure; it is not a Boltzmann computation of
> the asymmetry. 5/5 checks PASS.

Seeded 2026-08-04 as part of standing up the claims layer (D12). Promoted to `review_state: authored`
2026-09-04 alongside F364, which supplies the independent evidence, computed magnitude, and stated
falsifier this card previously lacked.

## Sources

- `findings/F202-leptogenesis-from-intrinsic-L-violation.md`
- `findings/F364-baryogenesis-boltzmann.md`
- `findings/F201-kev-sterile-from-eg-texture.md`
- `findings/F47-majorana-seesaw-higgs-free.md`
- `findings/F53-fg9-C-CP-per-species.md`
- `docs/claims/README.md` — the promotion contract (`unreviewed-seed` → `authored`)
