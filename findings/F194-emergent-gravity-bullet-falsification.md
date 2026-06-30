# F194 — The model-native emergent-gravity ("dark matter without dark matter") route, falsified by the Bullet-Cluster lensing/gas offset

**Date:** 2026-06-30 - 15:10
**Numbering:** drafted as F193, but a concurrent session claimed F193 for `F193-ontic-vacuum-gravitates-as-zero` (the CA-native vacuum candidate (i)); renumbered to **F194** on merge (re-checked per CLAUDE.md).
**Status:** Confirmed — 5/5 checks PASS. The acceleration-scale derivation (E1) and the QUMOND solver self-consistency (E3) are quantitative/machine-level; the Bullet-Cluster falsifier (E4) is a 3D toy whose **conclusion is a robust topological discriminator**, not a parameter fit. This builds the one gravity-*side* dark-matter candidate that the catalog (§4) and [[F191-dark-matter-rotation-curves-bullet]] left open, and shows it fails the same test that breaks MOND at cluster scales.
**Module:** `ca-simulation/ca_emergent_gravity.py`
**Script:** `tests/findings/test_F194_emergent_gravity_bullet.py` (~3 s; numpy only — real arithmetic; FFT used only for the linear real Newtonian Poisson solve, no chiral/complex transforms)
**Results:** `test-results/F194_emergent_gravity_bullet.json`
**Figure:** `test-results/figures/F194_emergent_gravity_bullet.png`
**Cross-references:** [[F191-dark-matter-rotation-curves-bullet]] (the assessment this makes specific — a dark *source* is needed, not modified gravity), [[F178-gravity-full-tensor-adoption]] (exact GR + constant $G$ canonical), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] / [[F192-vacuum-energy-full-tensor]] (the vacuum sector that sets the emergent-gravity acceleration scale), [[F59-induced-eh-prefactor-and-f10-selection]] / [[F79-structural-newton-constant]] (the *induced* $G$ whose IR enhancement this route would need). External: Milgrom 1983 (MOND), Milgrom 2010 (QUMOND), Verlinde 2016 (emergent gravity), Clowe et al. 2006 (Bullet Cluster 1E 0657−56, lensing/gas offset at 8σ).

---

## The candidate

After [[F178-gravity-full-tensor-adoption]] the gravity sector is exact GR with a **constant** induced $G$, so a vacuum dielectric that merely re-weights visible matter is not dark matter (F191). The single surviving gravity-*side* idea was the catalog's §4 note: because $G$ is **induced** (Sakharov; $G=a^2c^3/8\pi\sqrt3\,\hbar$, F59/F79), it could be **scale/curvature-dependent**, with an IR enhancement at the very low accelerations of galactic and cluster outskirts — the model-native cousin of Verlinde's emergent gravity. Operationally: baryons drag the lattice's induced response harder when the local curvature is small, so the lattice "weighs more" than its baryons, mimicking a dark halo with **no new matter**. This finding builds that idea and confronts it with the Bullet Cluster.

## The construction (model-native content)

**1. The acceleration scale comes from the model's own vacuum sector.** Emergent gravity needs a critical acceleration $a_0$. In this model it is *not* a free parameter: the de Sitter / vacuum-energy scale that the cosmological-constant work (F164/F192) is about sets it. With $\rho_\Lambda$ fixing $H_0$ through $H_0^2=8\pi G\rho_\text{crit}/3c^2$ and the Verlinde coefficient $a_0=cH_0/6$,

$$a_0^\text{model}=1.16\times10^{-10}\ \mathrm{m/s^2}\quad\text{vs}\quad a_0^\text{empirical}\approx1.2\times10^{-10}\ \mathrm{m/s^2}\ \ (\text{ratio }0.97).$$

So **dark energy and the emergent-gravity "dark matter" scale would be one number** — the elegant-design appeal that motivated building this rather than dismissing it. (E1.)

**2. The IR-running coupling.** Implemented as the QUMOND enhancement $g=\nu(\lvert g_N\rvert/a_0)\,g_N$ with $\nu(y)=\tfrac12+\sqrt{\tfrac14+1/y}$ — i.e. $G_\text{eff}/G=\nu\ge1$ grows as the acceleration falls ($\nu\to1$ in the Solar System, $\nu\to\sqrt{a_0/g_N}$ in the deep field). From baryons alone this flattens the rotation curve (flatness $0.99$) and obeys the baryonic Tully-Fisher relation ($v_\text{flat}^4=GM_b a_0$, ratio $1.0$). (E2.) **This route is therefore a genuine dark-matter mimic at galaxy scales — not a strawman.**

## The falsifier (E4)

In any such theory the lensing (dynamical) mass is the QUMOND **phantom density**

$$\rho_\text{dyn}=-\frac{1}{4\pi G}\,\nabla\!\cdot\!\big(\nu(\lvert g_N\rvert/a_0)\,g_N\big),\qquad g_N=-\nabla\Phi_N[\rho_\text{baryon}],$$

a **local functional of the baryons** (with $\nu\equiv1$ it returns $\rho_\text{dyn}=\rho_\text{baryon}$ exactly — verified to $0.4\%$, correlation $0.9999$, E3). Lensing therefore tracks the baryons. In a cluster the baryons are dominated by the **X-ray gas**, not the galaxies, so emergent gravity predicts the **lensing peak on the gas**.

A 3D toy Bullet Cluster (collision axis $x$; galaxies = collisionless baryon clumps at $x=\pm0.37$ Mpc, gas = dominant baryons dragged to $x=\pm0.18$ Mpc, $M_\text{gas}=6\,M_\text{star}$) gives:

| component / model | lensing peak $x$ | offset from gas |
|---|---|---|
| gas (X-ray) | $0.177$ Mpc | — |
| galaxies (collisionless) | $0.366$ Mpc | — |
| **emergent gravity (predicted lensing)** | **$0.177$ Mpc** | **$0.000$ Mpc — on the gas** |
| **observation** (Clowe 2006) | on the galaxies | **$0.189$ Mpc** |
| $\Lambda$CDM (real dark source on galaxies) | $0.343$ Mpc | $0.165$ Mpc ✓ |

Emergent gravity places the lensing peak **on the gas**; the observed peak is **on the collisionless galaxies**, $\approx0.19$ Mpc away. The route mispredicts the lensing-mass location by the full galaxy–gas separation, while $\Lambda$CDM (a real collisionless dark *source*) reproduces the observed offset. **The model-native emergent-gravity dark matter is falsified.**

## Checks (5/5)

| # | Check | Result | Tier |
|---|---|---|---|
| E1 | $a_0$ from the vacuum/de Sitter scale (F164/F192) = $1.16\times10^{-10}$ m/s², ratio $0.97$ to empirical | PASS | quantitative |
| E2 | emergent gravity flattens the rotation curve (flatness $0.99$) + baryonic Tully-Fisher (ratio $1.0$) from baryons alone | PASS | quantitative |
| E3 | Newtonian limit ($a_0\to0$, $\nu\to1$): $\rho_\text{dyn}/\rho_\text{baryon}=0.996$, corr $0.9999$ (solver validation) | PASS | machine-ish |
| E4 | **Bullet falsifier:** EG lensing on the gas (offset $0.000$ Mpc); observed on galaxies ($0.189$ Mpc); $\Lambda$CDM matches; misprediction $0.189$ Mpc | PASS | toy, robust direction |
| E5 | verdict: model-native emergent gravity **FALSIFIED**; a dark *source* is required | PASS | — |

**Overall 5/5 PASS.**

## Why the conclusion is robust (not an artifact of the toy)

The peak location is **topological**, not a fit: $\rho_\text{dyn}$ is a local functional of $\rho_\text{baryon}$, so its peak can never migrate to the offset galaxies where there is little baryonic mass — *regardless* of $a_0$, the interpolation function, or the clump shapes. The MOND/EG phantom adds an extended $1/r^2$ halo around the baryons (visible as the broad black tail in the figure) but does not move the centroid off the gas. This is exactly why MOND-class theories fail the Bullet Cluster in the literature; the model-native induced-$G$ version inherits the failure because it shares the defining property — gravity sourced by baryons only. The two numerical subtleties were handled honestly: the Newtonian Poisson solve uses **isolated (zero-padded) boundaries** (periodic images otherwise ramp the vacuum phantom), and peaks are compared **within the cluster field of view** (the deep-field $\nu$-divergence produces a real but irrelevant extended tail). The $\nu\equiv1$ self-consistency (E3) confirms the solver returns the baryons exactly in the Newtonian limit.

## Consequence for the model

This closes the gravity-side dark-matter option. Under F178 the model **needs a dark gravitating source**, not modified gravity — confirming and sharpening F191. The natural model-native source is the **gravitating-yet-dark vacuum/condensate** tied to the F164/F192 sector (a component that sources $T_{\mu\nu}$, lenses, clusters collisionlessly, and is electromagnetically invisible). The appealing $a_0$–$\rho_\Lambda$ coincidence (E1) is *not* wasted: it suggests the same vacuum sector still sets the relevant scale, but it must enter as a **clustering dark source**, not as an IR-running of $G$. That makes the F164/F192 vacuum-energy investigation the single highest-value next step for both dark energy *and* dark matter.

## Open / next

- **Dark-condensate halo (the surviving candidate):** source the metric from a collisionless dark vacuum/condensate (F164/F192 sector); fit a rotation curve **and** pass the Bullet Cluster (lensing on the collisionless component, which it would by construction) **and** the CMB third peak + linear structure growth. The Bullet test that kills emergent gravity is automatically passed by a real source; CMB/growth is the remaining make-or-break.
- **Curvature- vs acceleration-running:** this finding tested an *acceleration*-scale running (MOND/EG form). A pure *curvature*-scale running of the induced $G$ (Ricci-dependent) is a distinct, weaker variant; it faces the same baryon-sourcing obstruction at clusters but could be checked for completeness.
- Tie the $a_0=cH_0/6$ coincidence to a first-principles derivation of $H_0$ from the F164/F192 vacuum density (currently uses the observed $\rho_\Lambda$).

## Files
- Module: `ca-simulation/ca_emergent_gravity.py`
- Test: `tests/findings/test_F194_emergent_gravity_bullet.py`
- Results: `test-results/F194_emergent_gravity_bullet.json`
- Figure: `test-results/figures/F194_emergent_gravity_bullet.png`
