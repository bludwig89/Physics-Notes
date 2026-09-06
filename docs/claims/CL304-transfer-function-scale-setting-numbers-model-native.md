---
id: CL304
title: 'Two of the imported EH98 transfer-function scale-setting numbers -- the sound horizon and the hydrogen recombination redshift -- are derived model-natively (direct integration of the model''s own F182/F188 background; Saha equation with the model''s own F125 Rydberg energy), agreeing with Planck to 0.11% and reproducing the textbook ~26% Saha-vs-true recombination bias honestly; the acoustic-oscillation envelope and Silk damping remain imported'
slug: transfer-function-scale-setting-numbers-model-native
tier: supporting
kind: derivation
status: open
domain: [cosmology]
exactness: quantitative
findings: [F369, F288, F182, F188]
tests: [F369-transfer-function-scoping]
modules: [casim.engine.interactions.cosmology_transfer_function]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL254
falsifier: stated
first_issued: '2026-09-05'
last_verified: '2026-09-05'
provenance: authored
review_state: authored
confidence: medium
---

# CL304 — Two of EH98's imported transfer-function scale-setting numbers are now model-native

## Statement

The comoving sound horizon at the baryon-drag epoch, computed by direct numerical integration
of the model's own multi-component Friedmann background (F182/F188) to the (imported) Planck
drag redshift, agrees with Planck's own measured $r_\text{drag}$ to $0.11\%$ -- $16\times$
closer than the closed-form fitting-formula approximation `cosmology_growth.transfer_eh98`
already uses internally ($1.86\%$ off). Separately, the hydrogen recombination redshift,
computed from the plain (equilibrium) Saha equation using the model's own Rydberg energy
(F125, `atom.rydberg_eV` at the physical $e$–$p$ reduced mass) and the model's already-imported
$\eta_{10}$ (F297), reproduces the textbook $\approx26\%$ high bias of equilibrium Saha against
the true (Peebles 1968, non-equilibrium) recombination redshift. Substituting the model-native
sound horizon into the ($\sigma_8$-headline, F288) transfer function shifts $\sigma_8$ by only
$0.013\%$ -- two orders of magnitude below the $\approx1.15\%$ $\sigma_8$-vs-Planck residual --
localising that residual onto EH98's still-imported acoustic-wiggle envelope rather than the
sound-horizon scale.

## What it extends

Extends [[F288-structure-formation-zero-free-functions]] (CL254) by converting two of the three
external inputs `docs/status/open-derivations.md` row S2 names ("THREE NAMED IMPORTS, EACH
PRICED", item (i)) from black-box imports into quantities the model derives from machinery it
already owns elsewhere in the tree (F182/F188's confirmed cosmological background; F125's
machine-precision hydrogen binding energy). It does not extend, and is not claimed to extend,
Eisenstein & Hu (1998)'s transfer-function *shape* itself -- the acoustic-oscillation envelope
and Silk damping scale remain EH98 imports, named in the finding as needing a full multipole
Boltzmann-hierarchy solver this session does not build.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F369-transfer-function-scoping.md` | Full derivation, six checks, two-axis control | quantitative + exact (S1/S2) |
| `tests/registry/interactions.yaml` id `F369-transfer-function-scoping` | Gate-tier registry record, `entry: run`, PASS | quantitative |
| `test-results/F369_transfer_function_scoping.json` | Result artifact: $r_s=146.923$ Mpc vs Planck $147.09$ Mpc; $z_\text{Saha}=1378.62$ vs Planck $z_*=1089.92$; $\sigma_8$ shift $+0.0129\%$ | quantitative |

## Falsifier

A re-measurement of the model's own sound-horizon integral (using the SAME F182/F188 background
already confirmed elsewhere) that disagreed with Planck's $r_\text{drag}$ by more than the
current $0.11\%$ at fixed inputs would indicate an integration or background error, not new
physics -- this is an internal-consistency check, not a test of the model against nature. The
Saha-recombination leg has a stated, non-arbitrary target band ($15$–$40\%$ bias): a value
outside that band at the model's own physical inputs (unperturbed) would mean either the
Rydberg-energy import from `atom.py` or the Saha implementation itself is wrong, since the band
is the well-established literature size of the equilibrium-approximation omission, not a free
parameter of this claim.

## Status & history

`status: open` -- asserted with evidence, but incomplete by design: this claim narrows two of
S2's three named imports, it does not close S2 or promote K11 past `PARTIAL`. The remaining gap
(the acoustic-wiggle / Boltzmann-calibrated envelope, and Silk damping) is explicitly named in
`findings/F369-transfer-function-scoping.md` §2 as requiring a full multipole Boltzmann-hierarchy
solver, scoped but not attempted this session. First issued 2026-09-05; no prior broader form to
narrow from.

## Sources

- `findings/F369-transfer-function-scoping.md`
- `findings/F288-structure-formation-zero-free-functions.md` (the headline claim this rolls up to)
- `docs/status/open-derivations.md` row S2
- Eisenstein & Hu (1998); Hu & Sugiyama (1996); Planck 2018 VI, Table 2; Peebles (1968)
