# F135b — Real-space confinement (U1): the proton holds together as a scalar-confined three-body bound state, and why vector confinement Klein-tunnels

> **Renumbered F135b at roadmap C8.2 close-out (2026-07-31).** This file shared its number with another finding; the C8 audit found ten such collisions. The `b` suffix keeps the number findable — every existing citation of F135 still resolves — while making the two files distinguishable to tooling. See `docs/design/finding-numbers.yaml`.


**Date:** 2026-06-11 - 18:53
**Status:** Confirmed — 3/3 checks PASS (+ the K1 kernel certificate). K1 machine-precision/bit-for-bit (uniform reduction; unitarity); S1/V1 quantitative (bounded-vs-dispersing cluster; Klein null). Closes the U1 open edge of F134.
**Modules:** `ca-simulation/ca_dirac_bcc.py` (new `dirac_step_3d_bcc_varm_splitstep` + `_mix_eta_chi_3d`); `src/casim/particles/channel.py` (scalar/vector `confine` block on the Dirac/Weyl `ParticleChannel`; `unification_readout` gains a `cluster` config).
**Scenarios:** `scenarios/confined_baryon.yaml`, `scenarios/confined_baryon_free.yaml` (control).
**Test:** `tests/findings/test_F135_realspace_confinement.py` (3/3, ~25 s).
**Results:** `test-results/casim_confined_baryon{,_free}.json`.
**Cross-references:** [[F134-unified-real-space-integration]] (the U1 null this closes — linearised gluon does not confine), [[F86-colour-dielectric-dual-superconductor]] (the dual-superconductor / dielectric mechanism this realises: ε_c→0 ⇒ ∞ effective mass in the vacuum = the scalar bag wall), [[F70-gradient-flow-confinement-string-tension]] (the string tension σ), [[F122-p2-dynamical-baryon-three-body]] (the spectral constituent baryon this puts in real space; "the mass is the string"), [[F110-realtime-link-hamiltonian-confinement]] (the dynamical flux tube this coarse-represents), `docs/roadmaps/roadmap-unified-real-space.md` (U1).

---

## 1. What this closes

F134 ran the full chain on one lattice but found (U1) that the linearised one-gluon-exchange `gluon_sourced` (F43) kernel does **not** confine — the proton's quarks dispersed exactly as if free. The diagnosis matched F74/F122: the proton's binding is the **non-perturbative confining string** (F86/F70/F94/F110), not perturbative exchange. This finding builds that string into the real-time lattice dynamics and shows a three-body cluster **stays bound in real space**, with a sharp accompanying result about *how* the string must couple.

## 2. The derivation — scalar (not vector) confinement

The QCD vacuum is a colour-magnetic condensate; by the dual Meissner effect (F86) it expels colour-electric flux into a tube of fixed energy-per-length σ → the linear potential $V(R)=\sigma R$. The decisive question for a **real-time Dirac** constituent is *how* that linear potential enters the wave equation:

- A **vector** (time-component, $\gamma^0$) linear potential — the naive "potential energy" / phase kick $e^{-iV\,dt}$ — does **not** bind a light fermion: by the **Klein paradox** a steep vector step is transparent (pair-production / transmission), so the packet is only redirected, never slowed. (Confirmed directly: a vector phase kick of any σ leaves the quark dispersion identical to free, V1 below and the F134 σ-scan.)
- A **Lorentz-scalar** linear potential — added to the **mass**, $m_\text{eff}(x)=m+\sigma\,r$ — *does* bind: a position-dependent mass has no Klein transmission (the gap grows with $r$, excluding the wavefunction). This is exactly the **MIT-bag** mechanism, and it is precisely **F86 in the quark's frame**: the colour dielectric $\varepsilon_c\to0$ in the condensed vacuum means the field — and the quark coupled to it — cannot propagate there, i.e. an effectively infinite mass outside the flux tube. The bag wall *is* the scalar confining mass.

So the model-native confining coupling is a **Lorentz-scalar position-dependent mass**, with slope set by the F70/F86 string tension σ. For the baryon the minimal string is the **Y-string** with a junction at the colour-singlet centre of mass, so each constituent feels $m_\text{eff}(x)=m+\sigma\,|x-R_\text{cm}|$ (a single conical well with full inward gradient σ everywhere; the pairwise Δ-string $\sum_{j}(\sigma/2)|x-r_j|$ is the alternative, with partially-cancelling gradients at the centre — it confines more weakly).

## 3. The kernel (K1)

`dirac_step_3d_bcc_varm_splitstep` realises the scalar mass on the 3D BCC lattice by Strang splitting around the audited constant-mass exact-QCA propagator:

$$\text{Mix}(\delta m,\tfrac{dt}{2})\;\to\;\text{Kinetic}(m_0,dt)\;\to\;\text{Mix}(\delta m,\tfrac{dt}{2}),$$

where Mix is the per-cell η↔χ rotation $\exp(-i\beta\,\delta m\,dt/2)$ (dimension-agnostic, identical to the audited 2D `ca_dirac._mix_eta_chi`) and $\delta m(x)=m_\text{eff}(x)-m_0$. The kinetic mass $m_0$ obeys QCA admissibility $|m_0|\le1$, but the **Mix carries the entire confining profile with no bound** — a real rotation is always unitary, which is what lets the scalar mass rise to the bag wall. **Certificate:** on a uniform field it is bit-for-bit `dirac_step_3d_bcc_splitstep` (residual $0.0$), and a strong linear well conserves norm to $<10^{-12}$ over 100 steps.

## 4. The result — a real-space confined baryon (S1, V1)

Three massive Dirac constituents ($m=0.9$, in the F122 constituent window $m/\sqrt\sigma\approx$ O(1); colour-blind stand-ins — the binding is the string, per F122 "the mass is the string, not the constituents") confined toward the singlet COM with $\sigma=0.5$, $dt=0.5$:

| tick | confined cluster RMS | free control RMS |
|---|---|---|
| 0 | 2.02 | 2.02 |
| 50 | 3.54 | 6.62 |
| 100 | 3.69 | 7.95 |
| 200 | 3.71 | 7.84 |
| 300 | 3.74 | 7.16 |

The confined cluster **rises to ≈3.7 and plateaus** (a stationary, non-dispersing bound state — capped at 3.74 over 300 ticks), while the free control disperses to box saturation (~7–8 on $L=16$). The binding radius is set by the constituent mass + string tension (a light constituent has large zitterbewegung — the same physics that makes the real proton ≈1 fm rather than a point, and why F122 used heavy *constituent* quarks). **Vector mode** (the same σ as a phase kick) reproduces the free dispersal (within 15%) — the Klein null, confirming the scalar coupling is essential.

## 5. Checks

| # | Check | Tier | Result |
|---|---|---|---|
| K1 | `varm` step == constant-m step on uniform field; unitary under a strong well | machine / bit-for-bit | $0.0$; norm drift $<10^{-12}$ |
| S1 | scalar confinement binds: cluster RMS bounded vs free dispersal | quantitative | confined max $3.74$ (plateau) vs free $>7$; ratio $<0.65$ |
| V1 | vector confinement Klein-tunnels (no binding) | quantitative | vector $\equiv$ free within $15\%$ |
| N1 | every constituent norm conserved | machine | $<10^{-10}$ (engine run $\sim10^{-14}$) |

## 6. The honest open edge

The binding is exhibited with **colour-blind massive Dirac constituents** (the string does the binding; colour only labels the singlet). Wiring the scalar string onto genuine **SU(3) colour-triplet** quarks — a colour×Dirac quark that simultaneously carries the F43 gluon coupling and the scalar bag mass — is the remaining engine step to a fully colour-dynamical real-space proton. The string here is a **mean-field** coarse-representation of the F110 dynamical flux tube / F86 dielectric (σ is an input, the F70/F86 tension), not the self-consistent flux-tube field; promoting it to the live dielectric channel is the deeper (U3/U4) work. And the scale separation of F134 §6 still stands: this confined object is a compressed-scale baryon — the physical fm scale and the atomic orbit are restored only at U4 via the block-spin multigrid (F133).

## 7. What this adds to the ledger

New kernel `dirac_step_3d_bcc_varm_splitstep` (`ca_dirac_bcc.py`); scalar/vector `confine` coupling on the `ParticleChannel`; `unification_readout` `cluster` option; two scenarios; new suite `tests/findings/test_F135_realspace_confinement.py` (3/3). With U1 closed, the real-space programme has: U0 (full chain, F134), U1 (confined baryon, this finding), U2 (responsive EM loop, F134) — the open phases are U3 (neutral hydrogen at one scale) and U4 (the block-spin multigrid that restores physical scale separation). Exactness rows: Tier-1 #77 (`varm` uniform reduction bit-for-bit + unitarity), Tier-3 #78 (scalar-confined bounded cluster vs free dispersal; vector Klein null).
