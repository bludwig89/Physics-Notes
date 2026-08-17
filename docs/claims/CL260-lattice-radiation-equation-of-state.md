---
id: CL260
title: 'The continuum radiation equation of state is a theorem of the lattice, with closed-form corrections of order (T/T_lattice)^2'
slug: lattice-radiation-equation-of-state
tier: supporting
kind: derivation
status: live
domain: [QFT, GR]
exactness: exact
findings: [F300, F69, F26, F107]
tests: [F300-lattice-thermodynamics]
modules: [casim.engine.interactions.thermodynamics]
constants: [c_lat, a_over_ellP]
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: 2026-08-06
last_verified: 2026-08-06
provenance: authored
review_state: authored
confidence: high
---

# CL260 — The continuum radiation equation of state is a theorem of the lattice

## Statement

Built on the model's own derived dispersion $\Omega_\text{pair}(\mathbf k)=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$ and on nothing else, the equilibrium photon gas obeys $w=p/u=1/3$ and $u=(\pi^2/30)g(k_BT)^4/(\hbar c_\text{lat})^3$ **exactly** in the infrared, and the leading finite-lattice corrections are closed-form pure numbers times $\Theta^2$, where $\Theta=k_BT\tau/\hbar$ and $\tau=a/(\sqrt3\,c)$ with $a=6.5978\,\ell_P$:

$$\frac{u}{u_\text{SB}}-1=\frac{40\pi^2}{441}\Theta^2,\qquad \frac13-w=\frac{16\pi^2}{1323}\Theta^2,\qquad \frac{s}{s_\text{SB}}-1=\frac{4\pi^2}{49}\Theta^2,\qquad \frac{C_u}{C_w}=\frac{15}{2}.$$

The coefficients follow from the exact low-$k$ expansion $\Omega_\text{pair}=c_\text{lat}|\mathbf k|\bigl[1-A(\hat n)|\mathbf k|^2\bigr]$, $A(\hat n)=\tfrac1{72}\sum_{i<j}\hat n_i^2\hat n_j^2+\tfrac1{24}(\hat n_x\hat n_y\hat n_z)^2$, whose sphere average is exactly $1/315$. $T_\text{lattice}=\hbar/(k_B\tau)=3.719\times10^{31}$ K. Zero free parameters.

The signed statement: **lattice radiation is softer than continuum radiation, never stiffer.**

## What it extends

Stefan–Boltzmann and the $w=1/3$ radiation equation of state are inputs to every standard cosmology, taken from continuum QFT. Here they are *derived* from a discrete dispersion, and the derivation comes with a computed correction that continuum QFT has no way to produce. Concretely it grades one of this project's own inputs: F297 (BBN) assumed the continuum forms, and this claim says the assumption is good to $1.2\times10^{-44}$ in $w$ at the BBN bottleneck, with $w=1/3$ holding to better than 1% for every temperature below $6.2\times10^{30}$ K.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F300-lattice-native-thermodynamics.md` §2.1 | closed-form $A(\hat n)$; $\Omega_\text{pair}$ exactly linear along $\langle100\rangle$ at all $\lvert k\rvert$ ($6.0\times10^{-14}$) | exact / machine |
| `findings/F300-lattice-native-thermodynamics.md` §3 | the three coefficients and the $15/2$ ratio against Brillouin-zone quadrature | exact vs $\le5.0\times10^{-4}$ |
| `findings/F300-lattice-native-thermodynamics.md` §3.1 | the epoch-by-epoch margins | quantitative |
| record `F300-lattice-thermodynamics` (gate) | G10-1 … G10-6b, 15/15 | — |
| `test-results/F300_lattice_thermodynamics.json` | the artifact | — |

The residual between closed form and quadrature is itself measured to scale as $\Theta^2$ ($1.3\times10^{-5}$ at $\Theta=0.002$, $1.3\times10^{-3}$ at $\Theta=0.02$), i.e. it is the next term in the series rather than numerical error. Declared control `linear_control=True` replaces the dispersion by an exactly linear one and turns G10-3/4/5/6 red — the checks can fail.

## Falsifier

**Computational, with a threshold, and it fires every gate run.** Any Brillouin-zone evaluation of the model's own `pair_dispersion` that returns $C_u/C_w$ differing from $15/2$, or any of the three coefficients differing from its closed form by more than $5\times10^{-3}$ relative at $\Theta\le0.02$, kills the claim as stated. That is exactly what record `F300-lattice-thermodynamics` checks (G10-3, G10-4, G10-5, G10-6), and the declared control `linear_control=True` demonstrates the check *can* go red by replacing the dispersion with an exactly linear one. The claim is also hostage to two upstream results: a change to $a$ (F107) rescales $T_\text{lattice}$ and every margin, and a change to the paired-photon dispersion changes $A(\hat n)$ and therefore all three coefficients.

**Observationally it is not falsifiable, and that is said rather than dressed up.** The deviation is a Planck-spectrum distortion of lattice-discreteness type, $\delta I_\nu/I_\nu\propto(\nu\tau)^2$; reaching FIRAS-class sensitivity ($10^{-5}$) needs $T\approx1.2\times10^{29}$ K, roughly 29 orders above the CMB. The 2026-08-04 completeness report had to strike F282's falsifier 5 for being unable to fire, and the lesson is recorded here rather than repeated: the fireable falsifier is the computation, the observational one does not exist, and no threshold is invented to disguise that.

## Status & history

`live` as stated, with one scope boundary made explicit in the card because it is the one a later citation is most likely to blur: **this is the Gibbs measure ON the derived dispersion, not a demonstration that the lattice dynamically reaches it.** F300 §4.1 shows the free sector does *not* — the branch occupations are exactly conserved, so the stationary ensemble is a generalised Gibbs ensemble. See `CL261` for the entropy side and F300 §4 for the dynamics.

Second scope boundary: photon sector only. A full $g_*(T)$ over the model's 48 Weyl fields is the named next step and is not claimed here.

## Sources

- `findings/F300-lattice-native-thermodynamics.md`
- `findings/F69-paired-spinor-photon.md`, `findings/F26-speed-of-light-as-rotation-rate.md`
- `findings/F107-canonical-a-adoption-L4-grb-gate.md` (the ruler that sets $T_\text{lattice}$)
- `findings/F297-bbn-light-element-abundances.md` (the input this grades)
- `docs/status/completeness-2026-08-04.md` row G10
