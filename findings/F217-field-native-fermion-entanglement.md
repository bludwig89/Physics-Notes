# F217 — Field-native second quantization: the super-exchange $J$ and two-site spin entanglement **emerge** from genuine fermion hopping (Jordan–Wigner Fock space, Hubbard $H$ with $t$ from `ca_dirac` and $U=2\arcsin m$), reproducing the F214 effective spin model exactly in the large-$U$ limit and wired live into `casim` as the `fermion_chain` channel

**Date:** 2026-07-01 - 17:05
**Numbering:** **F217** (re-checked per CLAUDE.md; F215/F216 taken by concurrent sessions — Eliashberg superconductivity / massive spin-2 dark-mode — F217 verified free).
**Status:** Confirmed — 5/5 checks PASS. Fermion algebra and $J$-emergence **exact** (machine zero / $<10^{-12}$); large-$U$ convergence to $\ln 2$ quantitative; live channel + checkpoint/resume bit-identical.
**Modules:** `ca-simulation/ca_second_quant.py` (genuine Fock-space Hubbard engine); `src/casim/engine/manybody.py` (`FermionChainChannel` + `FermionEntanglementObserver`).
**Test / results:** `tests/findings/test_F217_field_native_fermion_entanglement.py` (5/5) → `test-results/F217_field_native_fermion_entanglement.json`
**Cross-references:** [[f214-superexchange-and-live-entanglement]] (the effective spin model this finding derives from first principles), [[f212-dynamical-entanglement-generation]] (the exchange gate recovered in the large-$U$ limit), F9/Paper-1 (`ca_dirac` exact hopping), [[F26-speed-of-light-as-rotation-rate]] (mass gap $2\arcsin m$), `ca_manybody.py` (the mean-field sectors this is the exception to), [[F133-blockspin-casim-engine]] (first-class engine-op precedent). External: Hubbard model; Anderson super-exchange; Jordan–Wigner transformation.

---

## What F214 left open

F214 derived the entangler's coupling $J$ from an **effective** two-site Hubbard model — a spin model, valid at half filling. That leaves a gap: is $J$ (and the entanglement) genuinely a property of the model's fermions, or an artefact of the effective description? F217 closes it by building the real thing — a fermionic Fock space with Pauli exclusion — and showing $J$ and the entanglement **emerge**, with the effective spin model recovered only as the large-$U$ limit.

## The field-native construction

For `n_sites` cells with spin-½ fermions there are $2\,n_\text{sites}$ spin-orbitals ordered $(0\!\uparrow,0\!\downarrow,1\!\uparrow,1\!\downarrow,\dots)$. The Fock space is the full $2^{2n_\text{sites}}$ occupation space; fermionic antisymmetry is carried exactly by Jordan–Wigner string signs. The minimal field-native Hamiltonian is the Hubbard model

$$H=-t\!\!\sum_{\langle ij\rangle,\sigma}\!\big(c^\dagger_{i\sigma}c_{j\sigma}+\text{h.c.}\big)\;+\;U\sum_i n_{i\uparrow}n_{i\downarrow},$$

with **both couplings taken from the model, not fitted**: $t$ is the `ca_dirac` nearest-neighbour hopping amplitude (measured, F214) and $U=2\arcsin m$ is the mass gap (the double-occupancy cost).

## Results (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | Genuine fermions | $\{c_i,c_j^\dagger\}=\delta_{ij}$, $\{c_i,c_j\}=0$ to **machine zero** ($0.0$) | exact |
| G2 | Pauli + product init | $\lvert\!\uparrow,\downarrow\rangle$ has zero double occupancy, $\langle\mathbf S_0\!\cdot\!\mathbf S_1\rangle=-\tfrac14$, spin entropy $=0$ (a single Slater determinant) | machine |
| G3 | **$J$ emerges** | full 2nd-quantized singlet–triplet gap $=$ F214 closed form $\tfrac12(\sqrt{U^2+16t^2}-U)$ to $<10^{-12}$ (worst $4.7\times10^{-16}$), every $m$ | **exact-algebraic** |
| G4 | large-$U$ limit | as $U/t$ grows the spin dynamics $\to$ the pure exchange gate: peak spin entropy $\to\ln 2$ ($0.693147$ at $m{=}0.98$, $U/t{=}44.7$), doublon leakage $0.127\to0.002$ | quantitative |
| G5 | **LIVE `fermion_chain`** | from $\lvert\!\uparrow,\downarrow\rangle$ real hopping generates two-site spin entanglement $0\to0.692$ live; norm conserved; checkpoint/resume **bit-identical** ($\Delta\psi=0$) | quantitative + machine |

## The crux — the effective model is a limit, not an assumption

The genuine second-quantized diagonalisation returns **exactly** the F214 super-exchange $J$ (G3, to $10^{-16}$): the effective spin model was correct, and is now derived from the fermion algebra rather than posited. But the field-native dynamics is *richer* than the spin model at finite $U$: starting from the Fock product $\lvert\!\uparrow,\downarrow\rangle$, the real hopping generates two-site spin entanglement while also admitting virtual **double occupancy** (charge fluctuations). The spin sector reaches only $S\approx0.68$ at $m=0.5$ because $\sim19\%$ of the weight has leaked into doublon states. As $U/t\to\infty$ (large mass) the leakage vanishes and the peak entanglement converges cleanly to $\ln 2$ (G4) — the exact point where the Hubbard dynamics reduces to the F212/F214 exchange gate $e^{-i(J/4)\boldsymbol\sigma_A\cdot\boldsymbol\sigma_B}$. So the tower is now complete and internally consistent:

$$\underbrace{\text{`ca\_dirac` hopping}}_{t}\;\xrightarrow{\text{2nd quantization}}\;\underbrace{\text{Hubbard Fock dynamics (F217)}}_{\text{charge + spin}}\;\xrightarrow{U/t\to\infty}\;\underbrace{\text{exchange gate (F212/F214)}}_{J=4t^2/U,\ \text{pure spin}}.$$

## Why it matters

This makes the entanglement in the model **field-native**, not a spin-model convenience: it lives in a genuine antisymmetrised fermionic Fock space, generated by the same hopping that sets $c$ and the mass gap, with Pauli exclusion enforced by the operator algebra to machine zero. `casim` now carries two complementary many-body sectors beyond the mean-field stack — the effective `entanglement_register` (F214) and the first-principles `fermion_chain` (F217) — both schedulable and checkpoint-safe. It is the honest bottom of the quantum-computing cross-test: the exponential Fock space is real, allocated, and evolves under a derived Hamiltonian.

## What remains open

1. **Longer chains / doping.** Only two sites at half filling are exercised in depth; ring-exchange, $t$–$J$ reduction, and away-from-half-filling entanglement are the next steps ($n_\text{sites}\ge3$ already runs).
2. **Coupling to the live spatial lattice.** The Fock chain sits on designated cells; binding it to the propagating `ca_dirac` field (a genuine space-time second-quantized sector) is the deep remaining tier.
3. **A model algorithm** composed of these gates run entirely through the engine (the companion follow-up).

## Files

- `ca-simulation/ca_second_quant.py` — `jw_annihilation`, `FermionChain` (Hubbard $H$, evolve, double occupancy, spin operators/correlation, spin entanglement), `two_site_singlet_triplet_gap`, `hopping_and_gap`.
- `src/casim/engine/manybody.py` — `FermionChainChannel` (`fermion_chain`) + `FermionEntanglementObserver` (`fermion_entanglement`).
- `tests/findings/test_F217_field_native_fermion_entanglement.py` (5/5); `test-results/F217_field_native_fermion_entanglement.json`.
