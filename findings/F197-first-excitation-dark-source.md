# F197 — The first excitation channel as a unified dark sector: a near-vacuum channel can be both dark energy and dark matter **iff** it has a gapped branch — the F93 $E_g$ condensate qualifies (VEV → $w=-1$ smooth; gapped amplitude+angular modes → $w\to0$ cold, clustering, collisionless), the F69 paired-spinor channel is excluded (gapless/luminal → radiation)

**Date:** 2026-06-30 - 19:20
**Numbering:** **F197** (re-checked; prior max F196).
**Status:** **Discriminator built; one channel selected.** Structural demonstration (toy galactic profiles, illustrative not a fit — same posture as F191). The equation-of-state split is exact; the channel comparison is decisive; the relic abundance is the named open obstruction. 5/5 checks PASS.
**Module:** `ca-simulation/forks/gr_fork_F197_first_excitation_dark.py` (self-contained, real arithmetic; mirrors `gr_fork_F193/F196`).
**Tests / results:** `tests/findings/test_F197_first_excitation_dark.py` → `test-results/F197_first_excitation_dark_test.json` (5/5); fork dump `test-results/F197_first_excitation_dark.json`.
**Cross-references:** [[F193-ontic-vacuum-gravitates-as-zero]] (§E poses this exact question; §73 the local-dielectric no-go for the homogeneous mode — used directly), [[F196-dilution-exponent-derived]] (the $w=-1$ residual is the dark-energy slot; this finding leaves it untouched and asks only about excitations), [[F191-dark-matter-rotation-curves-bullet]] (the dark-**source** requirement and the Bullet-Cluster collisionless test — the bar this finding must clear), [[F93-orthorhombic-Eg-vacuum]] (the $E_g$ second-shell condensate and its Landau energy — Channel A), [[F96-second-shell-Eg-gap-saturation]] (the gap), [[F73-spin0-bound-pair-scalar]] (the amplitude/Higgs-like mode), [[F69-paired-spinor-photon]] / [[F169-photon-interacting-two-body-wavefunction]] (Channel B — the marginal-binding photon channel), [[F150-eg-sextic-brake-from-architecture]] / [[F154-residuals-A-B-built-and-solved]] (the sextic $\lambda_6$ that sets the light angular-mode mass), [[F64-em-connection-gravity]] / [[F106-psi-K-sourcing]] (the dielectric the clump sources), [[F178-gravity-full-tensor-adoption]] (exact GR + constant $G$). External: rotation-curve flatness; Clowe et al. 2006 (Bullet Cluster).

---

## The question, sharpened from F193 §E

F193 derived that the **empty** ontic lattice gravitates as exactly zero, and F196 showed the small residual $\rho_\Lambda$ is the holographic back-reaction — a homogeneous, $w=-1$, **dark-energy** term. So the "empty plate weighs nothing" is a theorem, and a *uniform* base weight could only ever be dark energy: F193 §73 proves a spatially constant $T^{00}$ has **no normalizable static-dielectric solution** ($\nabla^2\ln K=-\kappa\rho_\text{const}$ grows like $r^2$), so it feeds only the homogeneous Friedmann mode and **cannot** make a galactic halo. F191 independently requires dark *matter* to be a **clustering, collisionless source** (the Bullet-Cluster lensing offset rules out a pure dielectric reweighting of baryons).

The dark-matter question is therefore not about the empty lattice but about its **first excitation above vacuum**. F193 §E named the make-or-break: can *one* near-vacuum channel be $w\simeq-1$ smooth on cosmic scales **and** clustering on galactic scales? This finding builds the discriminator and compares the two model-native candidates.

## The discriminator: equation of state follows from the excitation's nature

The single physical fact doing the work is that $w=p/\rho$ is fixed by *what* the excitation is:

| excitation type | dispersion / state | $w$ | cosmological role |
|---|---|---|---|
| homogeneous condensate VEV ($k=0$ order parameter) | sits at the Landau minimum, $p=-\rho$ | $-1$ | dark **energy** (smooth) |
| **gapped** massive mode, velocity dispersion $\sigma$ | $\hbar^2\omega^2=m^2c^4+\hbar^2c^2k^2$, non-rel. | $\tfrac13(\sigma/c)^2\to0$ | dark **matter** (cold, **clusters**) |
| **gapless** mode (e.g. the F69 luminal photon) | $\omega=c\lvert k\rvert$ | $\tfrac13$ | radiation (neither) |

At galactic $\sigma\approx200$ km/s the cold value is $w=1.5\times10^{-7}\approx0$. The corollary is the whole result:

> **A near-vacuum channel can carry clustering dark matter iff it has a gapped (massive) branch above the vacuum/condensate.** The homogeneous piece of *any* condensate is automatically the $w=-1$ dark-energy piece; its gapped fluctuations are the clustering piece. Same field, two regimes — exactly the §E requirement.

## Channel A — the $E_g$ second-shell condensate (F93): **qualifies**

The orthorhombic order parameter of F93 is an $E_g$ doublet $(e,\delta)$ with Landau energy $F=\tfrac r2 e^2+\tfrac b3 e^3\cos3\delta+\tfrac u4 e^4+\tfrac w6 e^6\cos^23\delta$. Minimizing on the orthorhombic-winning branch ($r<0,\ C>0,\ \lvert B\rvert<2C$) the fork lands at $\delta^*=12.72°$, $\cos3\delta^*=0.7862$ — **reproducing the F93 O7 data value** $12.73°/0.7859$ as a consistency check, not an input. The Hessian at the minimum has **two positive eigenvalues** → two gapped fluctuation modes:

- a heavy **amplitude (breathing/radial) mode** — the F73 spin-0 Higgs-like scalar ($\sim v/2$ scale);
- a lighter **angular (phase) mode** — pinned by the sextic $\cos3\delta$ invariant rather than a continuous symmetry (the $E_g$ break leaves only discrete $Z_3$, so there is **no exact Goldstone**); its mass is set by the small IR sextic $\lambda_6$ (F150/F154), making it the natural **axion-like, light, cold** candidate. Computed mass ratio $m_\text{ang}/m_\text{amp}=0.34$.

So Channel A delivers all three roles from one object: VEV → $w=-1$ dark energy (the F196 residual); gapped modes → $w\to0$ cold dark matter; self-interaction only through the small $\lambda_6$ → $\sigma/m\ll1\ \mathrm{cm^2/g}$ → **collisionless** (Bullet-compatible).

## Channel B — the F69 marginal-binding channel: **excluded**

The F69 paired-spinor photon is **massless** (luminal, $c=1/\sqrt3$) and the binding in this channel is **marginal** (F69/F169 threshold bound state), so the first-excitation gap $\to0$. Gapless ⇒ $w=\tfrac13$ ⇒ radiation, not cold matter; and the channel couples electromagnetically ⇒ collisional, not dark. It cannot be the dark-matter source. (This does not touch F69's role as the EM photon — it simply says the photon channel is not where a cold relic lives.)

## The clustering contrast (F193 §73, made concrete)

Using the F106/F193 weak-field law $\nabla^2\ln K=-\kappa\,T^{00}$ spherically:

- **Homogeneous** excitation ($w=-1$ piece): $\ln K=-\tfrac{\kappa\rho_0}{6}r^2\to-\infty$ — **non-normalizable**, no local halo; only the Friedmann/dark-energy mode. (Potential growth diverges as $r^2$.)
- **Localized** gapped-mode clump (cored profile): enclosed mass **converges**, $\ln K\to$ const — normalizable, and the rotation curve **flattens** (flatness $0.93$ vs the baryon-only fall-off $0.58$).

The same field is dark energy in its homogeneous mode and dark matter in its localized gapped overdensity — the contrast is not assumed, it falls out of normalizability.

## What is derived vs computed vs posited

| Piece | Status |
|---|---|
| EoS split: VEV $w=-1$, gapped cold $w=\tfrac13(\sigma/c)^2\to0$, massless $w=\tfrac13$ | **Derived** (kinematic; exact) |
| "clustering DM ⇔ a gapped branch exists" | **Derived** (consequence of the EoS split) |
| $E_g$ condensate has two gapped modes at $\delta^*=12.72°$ ($\cos3\delta^*=0.786$) | **Computed** (Landau Hessian; reproduces F93 O7) |
| angular mode lighter than amplitude ($m$-ratio $0.34$), axion-like | **Computed** (representative $\lambda_6$; ratio robust, value not) |
| F69 channel gapless → excluded as cold DM | **Derived** (F69 masslessness + marginal binding) |
| homogeneous non-normalizable / clump normalizable + flat curve | **Computed** (F193 §73 + toy profile, illustrative) |
| collisionless ($\sigma/m\ll1\ \mathrm{cm^2/g}$ via small $\lambda_6$) | **Posited / NDA** (structural, illustrative scale) |
| **relic abundance** $\Omega_\text{DM}\approx0.26$ ($\sim5\times$ baryons) | **Open — the new named obstruction** |

## The named obstruction

Reduced from "is there a model-native dark source at all?" to a single quantity: the **relic abundance**. Channel A *can* be the unified dark sector, but *why* $\Omega_\text{DM}\approx0.26$ (≈5× baryons) is not derived — it needs the cold-mode production history (misalignment of the light angular mode, à la an axion; and/or thermal freeze-out of the heavy amplitude mode), and the angular-mode mass itself rides on $\lambda_6$ (F150/F154), still unpinned. That is the next step, mirroring how F193→F196 reduced the CC problem to the $\Omega_\Lambda$ coincidence.

## Caveats (honest scope)

- Toy galactic profiles (exponential disk + cored clump); the flatness number is illustrative, not a fit — as in F191.
- The collisionless cross-section is an NDA proxy; the precise $\sigma/m$ needs the actual $\lambda_6$ and the mode mass.
- The amplitude mode at the $\sim v/2$ scale is too heavy to be the dominant cold relic without a production mechanism; the **light angular mode** is the realistic DM candidate, and its mass is not yet pinned.
- This finding does **not** derive the abundance or the mass — it establishes which *channel* can play the role and that the model selects exactly one.

## Test summary

| Check | Statement | Result |
|---|---|---|
| E1 | EoS split: VEV $-1$; gapped cold $1.5\times10^{-7}$; massless $1/3$ | PASS |
| E2 | $E_g$ condensate: two gapped modes at $\delta^*=12.72°$, angular lighter ($0.34$) | PASS |
| E3 | F69 channel gapless ($\text{gap}=0$) → radiation, not cold DM | PASS |
| E4 | homogeneous non-normalizable; clump mass converges + rotation flatness $0.93$ | PASS |
| E5 | verdict: $E_g$ = unified dark sector (DE+DM); F69 excluded | PASS |

**Overall 5/5 PASS.**

## Relation to other findings

Answers the make-or-break flagged in **F193 §E** and **F191**: the model *does* have a near-vacuum channel that can be both the **F196** dark-energy residual and a clustering, collisionless dark-matter source — the **F93** $E_g$ second-shell condensate — and it is the *unique* such channel (the **F69** photon channel is gapless and excluded). Uses **F193 §73**'s local-dielectric no-go as the clustering discriminator, **F73**'s amplitude mode and the **F150/F154** sextic for the angular mode, and **F64/F106/F178**'s dielectric as what the clump sources. Leaves the relic abundance $\Omega_\text{DM}$ as the sole remaining obstruction, the dark-matter analog of the **F196** $\Omega_\Lambda$ coincidence.
