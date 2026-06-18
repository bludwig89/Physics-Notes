# F134 — Unified real-space integration: the full chain on one BCC lattice (proton quarks ↔ gluon, charge ↔ photon ↔ electron), and where real-space binding actually comes from

**Date:** 2026-06-11 - 18:53
**Status:** Confirmed — 3/3 checks PASS. U0 structural (machine-precision norm conservation, all four loops live, exact neutrality); U1 quantified-null (no confinement from the linearised sourced gluon — coupled ≡ free); U2 quantified-positive (the Coulomb loop measurably attracts the electron). This is a **real-time real-space** result, complementary to — not a replacement for — the reduced spectral solves F122 (baryon) and F125 (atom).
**Module:** `src/casim/particles/channel.py` (new `unification_readout` observer); no new physics kernels — assembles audited channels.
**Scenarios:** `scenarios/unified_hydrogen.yaml`, `scenarios/unified_hydrogen_free.yaml` (control), `scenarios/unified_hydrogen_strongEM.yaml` (U2 probe).
**Script/Test:** `tests/findings/test_F134_unified_real_space.py` (3/3, ~40 s).
**Results:** `test-results/casim_unified_hydrogen{,_free,_strongEM}.json`.
**Cross-references:** [[F122-p2-dynamical-baryon-three-body]] (the spectral proton this puts in real space), [[F125-p5-hydrogen-atom-em-bound-state]] (the spectral atom), [[F74-bound-state-binding]] (the "gauge couplings bind too weakly" near-no-go this confirms in real time), [[F86-colour-dielectric-dual-superconductor]] / [[F94-lattice-gauge-mc-confinement-vs-F86]] / [[F110-realtime-link-hamiltonian-confinement]] (the non-perturbative confinement sector that the linearised gluon is **not**), [[F43-fg7-dynamical-gluons]] (the linearised sourced-gluon kernel used here), [[F69-photon-pair]]/[[f87-charge-coupling-paired-photon]] (the even-law Coulomb loop), [[F133-blockspin-casim-engine-kernel]] (the block-spin multigrid that U4 needs), `docs/roadmaps/roadmap-unified-real-space.md` (the U0–U4 plan).

---

## 1. What this closes (and what it does not)

The matter-binding roadmap is complete *in pieces*: F122 gives the proton/neutron as an explicitly-correlated-Gaussian three-body solve, F125 gives hydrogen as a radial finite-difference Coulomb solve. Neither is a single real-space lattice carrying the objects at once — the project's stated "universe in a bottle" goal. This finding takes the first concrete step: **one BCC lattice on which all the coupling loops run simultaneously in real time**, with an instrument (`unification_readout`) that measures whether the emergent bound objects actually form. It is the U0–U2 deliverable of `roadmap-unified-real-space.md`. It does **not** yet produce a stationary bound proton or a stationary atomic orbit — and the result explains precisely why, which is the value.

## 2. The integration (U0) — every loop live on one lattice

`scenarios/unified_hydrogen.yaml` stacks, on one $L=16$ BCC lattice: three colour quark `ParticleChannel`s ($u_r,u_g,d_b$); a `gluon_sourced` field (sources = the three quarks); a `photon_sourced` field with the open-Poisson Coulomb $\alpha(x)$ sector (sources = quarks **and** electron); a massive electron `ParticleChannel` ($e_L$, $m=0.3$); and a static F64 `gravity_dielectric` background. Channels step in a leapfrog order (sourced fields first, so each particle feels the field built from the prior tick's currents). The loops are two-way by construction: quarks publish $J_\text{colour}$ → gluon accumulates octet $A$ → quarks read $A$ via `su3_rotate_weyl_step`; particles publish $J_\text{em},\rho_\text{em}$ → photon builds $\alpha(x)$ via the audited open-boundary Poisson solver → the electron reads $\alpha$ via `u1_wrap_dirac_step`.

**Checks (U0):**
- **Norm conservation** of every matter channel to machine precision (max relative drift $1.3\times10^{-14}$) — the kernels stay unitary under full coupling.
- **All four loops live:** $\lVert J_\text{colour}\rVert,\ \lVert \text{gluon }A\rVert,\ \lVert J_\text{em}\rVert,\ \lVert\alpha\rVert$ all $>0$ — the currents are genuinely sourcing the fields and the fields are present.
- **Exact neutrality:** the system net charge $\sum_i Q_i = (\tfrac23+\tfrac23-\tfrac13)-1 = 0$ to $<10^{-12}$ ($uud+e$).

## 3. U1 — the linearised gluon does **not** confine (the quantified null)

Run the proton's three quarks with the strong loop ON vs a free control (couplings stripped, identical initial conditions). The combined-quark RMS radius trajectory is **identical to ~$10^{-3}$**: it grows from $1.84$ and saturates near $\approx7$ — i.e. the quarks disperse to fill the periodic box ($L/\sqrt{12}\cdot\sqrt3\approx8$), exactly as if free.

| tick | proton RMS, coupled | proton RMS, free |
|---|---|---|
| 0 | 1.837 | 1.837 |
| 10 | 6.127 | 6.127 |
| 30 | 7.894 | 7.894 |
| 60 | 7.117 | 7.117 |

This is the real-time confirmation of F74's "quantified near-no-go" and the F122 §4 lesson: **the proton's mass and stability are the non-perturbative confining string (F86 colour-dielectric / F94 lattice-gauge MC / F110 link Hamiltonian), not the linearised one-gluon-exchange `gluon_sourced` kernel (F43).** The massless colour-Weyl quarks propagate at $c_\text{lat}$ and the linear sourced-gluon back-reaction is far too weak to hold them. The fix for U1 is to drive the quark dynamics with the confinement sector, not perturbative exchange — the same conclusion F122 reached, now exhibited in real space.

## 4. U2 — the Coulomb loop **is** responsive (the quantified positive)

Drive the EM well hard (`g_coulomb` $6\to80$, $m_e\,0.3\to0.9$, electron started at separation $3$): the EM-on electron is pulled to a **minimum proton–electron separation of $1.86$ — closer than its starting $3.0$** — while the matched free control never drops below its initial $3.0$ (it only moves away). The signature is clearest in a late pull-back (tick $\sim55$): $\text{ep\_sep}$ on $\to1.86$ vs off $\to3.05$; electron RMS-about-proton on $5.89$ vs off $7.14$.

So the electromagnetic binding **mechanism is exhibited and responsive** — the proton's Coulomb $\alpha(x)$ genuinely attracts the electron. It is **not** a clean stationary orbit: at this compressed scale, in a small periodic box, a strongly-driven well over-accelerates the light electron into a scattering quasi-orbit (compact → flung out → pulled back) rather than a steady bound cloud. A stationary orbit requires the U4 scale separation and a properly scaled well (§6).

## 5. Checks

| # | Check | Tier | Result |
|---|---|---|---|
| U0.1 | every matter-channel norm conserved | machine | $1.3\times10^{-14}$ |
| U0.2 | all four loops live ($J_c,A,J_\text{em},\alpha>0$) | structural | PASS |
| U0.3 | system net charge $=0$ ($uud+e$) | exact | $<10^{-12}$ |
| U1 | proton RMS coupled $\equiv$ free (no confinement) | quantitative | $<1\%$; both $\to$ box saturation |
| U2 | Coulomb loop attracts ($\min$ sep $<$ start, $<$ free) | quantitative | $1.86<3.0$; free min $=3.0$ |

## 6. The honest open edge — scale separation (U3/U4)

A single *literal* lattice cannot hold a physical proton ($1.7\times10^{-15}$ m) and a physical Bohr orbit ($5.3\times10^{-11}$ m): they differ in size by $\sim3\times10^4$, so resolving both needs $\gtrsim10^4$–$10^5$ cells across ($\ge10^{12}$ in 3-D) — over every tractable ceiling (`roadmap-scale-to-real-space.md` §0; `roadmap-unified-real-space.md` §2). The U0–U2 runs here are therefore a **compressed-scale** demonstration: they exhibit the loops, their mutual consistency, and the qualitative force signatures (confinement absent at this kernel level; Coulomb attraction present) on one tractable lattice — **structure is the deliverable; absolute fm/eV stay P6-gated** exactly as in F122/F125. The physical, scale-separated atom is **U4**: the electron orbit on an atomic-scale lattice with the confined proton entering as a **block-spin-coarse-grained point charge** (F133 $\mathcal R_b$), and the proton's confinement on its own fine patch — a two-grid CA step. That, plus driving U1 from the confinement sector, is the remaining work to a real "universe-in-a-bottle" hydrogen atom.

## 7. What this adds to the ledger

New `unification_readout` observer in `src/casim/particles/channel.py` (auto-registered); three new scenarios; new suite `tests/findings/test_F134_unified_real_space.py` (3/3). No new physics kernels — the result is an integration + instrument + a quantified statement of where real-space binding originates (confinement sector for the strong loop; a scale-appropriate well for the EM loop). Exactness rows: Tier-3 #75 (real-space coupled-chain consistency: norms machine-precision, neutrality exact, four loops live), #76 (real-space confinement null: linearised gluon coupled $\equiv$ free; EM-loop attraction positive).
