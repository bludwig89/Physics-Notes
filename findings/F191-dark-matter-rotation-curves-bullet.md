# F191 — Dark matter under F178: rotation curves cannot separate a dark halo from modified gravity, but the Bullet-Cluster lensing offset favours a dark *source* over a dielectric reweighting (scenario S8, speculative)

**Date:** 2026-06-30 - 04:45
**Numbering:** **F191** (re-checked).
**Status:** Confirmed (as a demonstration/assessment) — 3/3 checks PASS. Toy galactic/cluster models; the conclusion is a qualitative discriminator, not a fit.
**Module:** `ca-simulation/ca_darkmatter.py`
**Script:** `tests/findings/test_F191_darkmatter.py`
**Results:** `test-results/F191_darkmatter.json`
**Cross-references:** gravity-sector catalog §4 (the dark-matter question), [[F178-gravity-full-tensor-adoption]] (exact GR + constant $G$), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] / [[F192-vacuum-energy-full-tensor]] (the candidate dark vacuum/condensate source). External: rotation-curve flatness; Clowe et al. 2006 (Bullet Cluster 1E 0657−56).

---

Scenario S8. Tests the catalog §4 assessment: under F178 the gravity sector is exact GR with constant $G$, so the dielectric only *responds* to mass — it is not itself the dark matter. The discriminator is the Bullet Cluster.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| D1 | Rotation curves: baryons alone fall ($v_{30\rm kpc}/v_{\max}=0.58$); an NFW dark halo **and** a MOND-type modified gravity **both** flatten the curve ($>0.85$) — so rotation curves alone do not decide | PASS |
| D2 | Bullet Cluster (toy): the collisional gas (X-ray) piles at the centre while the collisionless mass passes through; the lensing (total-mass) peak sits $0.34$ Mpc **offset** from the gas peak | PASS |
| D3 | Under exact GR + constant $G$, visible matter is insufficient ($v$ falls) → a dark gravitating **source** is required | PASS |

## Result

The honest verdict the catalog anticipated, made concrete. Flat rotation curves are reproduced equally by a collisionless dark halo and by a modified-gravity/dielectric reweighting of the baryons — they cannot tell the two apart. The **Bullet Cluster breaks the degeneracy**: because the lensing mass tracks the collisionless component and is offset from the dominant baryons (gas), a pure dielectric reweighting of visible matter (which would put the lensing peak on the gas) is disfavoured, while a dark gravitating *source* (a collisionless particle or a dark vacuum/condensate that sources the dielectric) fits. So under F178 the model needs a dark **source**, not modified gravity; the natural model-native candidate is a gravitating-yet-dark vacuum/condensate tied to the F164/F192 vacuum sector, or a sterile-sector excitation.

## Honest scope
Toy models (exponential disk, NFW halo, two-Gaussian cluster collision); the numbers are illustrative, not fits. The result is the *direction* of the evidence, not a parameter determination. Building a real dark-condensate halo and confronting CMB + structure growth is the next, much larger step.

## Open / next
- A clustering dark-vacuum-condensate halo sourcing $K$; rotation-curve fit + CMB third-peak + structure growth as the make-or-break battery.
- IR-running of the induced $G$ (emergent-gravity route) as the gravity-side alternative.

## Files
- Module: `ca-simulation/ca_darkmatter.py` · Test: `tests/findings/test_F191_darkmatter.py` · Results: `test-results/F191_darkmatter.json`
