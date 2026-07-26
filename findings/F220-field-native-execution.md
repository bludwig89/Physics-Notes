# F220 — The substrate computes on **genuine matter**: quantum gates and a full Deutsch–Jozsa run directly on the second-quantized fermionic Fock sector — single-qubit gates are exact fermionic operators $\exp(-i\,2\theta\,\hat n\!\cdot\!\mathbf S_s)$ (zero leakage), the two-qubit entangler is the **real Hubbard time-evolution** whose emergent super-exchange becomes the exact exchange gate as $U/t\to\infty$, and the algorithm's threshold verdict is correct despite sub-percent doublon leakage

**Date:** 2026-07-01 - 19:30
**Numbering:** **F220** (re-checked per CLAUDE.md; F215/F216 concurrent-session findings, F217–F222 this session — F220 verified free).
**Status:** Confirmed — 5/5 checks PASS. Single-qubit fermionic gates **exact-algebraic** (match to $8.3\times10^{-16}$, occupation conserved to $10^{-12}$); entangler fidelity $\to1$ and spin entropy $\to\ln2$ as $U/t$ grows; field-native CNOT correct to $<1\%$ (leakage-limited); Deutsch–Jozsa verdict correct on all four oracles; live channel + checkpoint bit-identical.
**Modules:** `ca-simulation/ca_second_quant.py` (`fermionic_rotor`, `spin_register`, `exchange_operator`, `fn_hadamard/fn_x/fn_z/fn_cnot`, `apply_program_fock`); `src/casim/engine/manybody.py` (`FermionAlgorithmChannel` + `FermionAlgorithmObserver`).
**Test / results:** `tests/findings/test_F220_field_native_execution.py` (5/5) → `test-results/F220_field_native_execution.json`
**Cross-references:** [[f217-field-native-fermion-entanglement]] (the Fock space + emergent $J$ this computes on), [[f218-algorithm-through-the-engine]] / [[f222-scaled-quantum-algorithms]] (the abstract-register algorithms this makes field-native), [[f214-superexchange-and-live-entanglement]] (the derived exchange coupling). External: Hubbard model; Anderson super-exchange; Jordan–Wigner; Deutsch–Jozsa 1992.

---

## What F217/F218/F222 left open

F217 built the genuine fermionic Fock space; F218 and F222 ran quantum algorithms, but on an **abstract** $2^n$ register sitting on designated cells. The deep open tier (F217 #2, F218 #2) was to run the gates — and an actual algorithm — **directly on the second-quantized matter**: computation whose logical qubits are physical fermion spins and whose gates are genuine fermionic operators. F220 closes it.

## The construction

A logical qubit is the **spin of a singly-occupied site**. In the one-fermion-per-site sector the fermionic spin operators $\mathbf S_s=\tfrac12(c^\dagger_{s\alpha}\boldsymbol\sigma_{\alpha\beta}c_{s\beta})$ act as $\tfrac12\boldsymbol\sigma$, so:

**Single-qubit gates are exact.** $U_s(\theta,\hat n)=\exp(-i\,2\theta\,\hat n\!\cdot\!\mathbf S_s)$ equals the abstract rotor $\exp(-i\theta\,\hat n\!\cdot\!\boldsymbol\sigma)$ on the qubit subspace, and because $S^\pm=c^\dagger_\uparrow c_\downarrow,\,c^\dagger_\downarrow c_\uparrow$ and $S^z$ all conserve the per-site occupation, the one-per-site sector is left **exactly invariant** — the gate is a genuine fermionic operator with zero leakage (verified to $8.3\times10^{-16}$, weight $=1$ to $10^{-12}$).

**The entangler is the real Hubbard dynamics.** The two-qubit gate is not written down as a matrix — it is executed by evolving $e^{-iHt}$ under the genuine Hubbard $H$ (hopping $t$ from `ca_dirac` + on-site $U$ from the mass gap). The emergent super-exchange (F214/F217) gives $H_\text{eff}=\tfrac{J}{4}\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B$, so evolving for $t=4\theta/J$ realises $\exp(-i\theta\,\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B)$. At finite $U$ the real dynamics also excites **virtual doublons** (charge fluctuations leaking out of the one-per-site sector); as $U/t\to\infty$ the leakage vanishes and the entangler becomes the exact exchange gate.

The logical readout is the isometry `spin_register`: project the Fock state onto the one-per-site sector and read the $2^{n_\text{sites}}$ spin amplitudes, reporting the leakage weight alongside.

## Results (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | single-qubit exact | fermionic $\exp(-i2\theta\hat n\!\cdot\!\mathbf S)$ $=$ abstract `su2_rotor` to $8.3\times10^{-16}$ over 12 (axis, angle) cases; one-per-site weight $=1$ (no leakage) | **exact-algebraic** |
| G2 | entangler = Hubbard dynamics | genuine $e^{-iHt}$ from $\lvert\!\uparrow\downarrow\rangle$: fidelity to the ideal exchange gate $0.979\to1.0000$ and spin entropy $\to\ln2$ as $U/t$: $3.9\to44.7$ — a **Bell pair generated on matter** | quantitative |
| G3 | field-native CNOT | exchange-derived CZ + fermionic-$H$ dressing acts as the textbook CNOT on the site-spin register to $<1\%$ (worst $0.005$), leakage-limited | quantitative |
| G4 | field-native Deutsch–Jozsa | all four oracles classified correctly (const$\to$constant, balanced$\to$balanced) with the **entire computation in the Fock space** | machine (verdict) |
| G5 | live in engine | `fermion_algorithm` channel runs DJ one layer/tick, returns the right verdict live (weight $0.9975$); checkpoint mid-run resumes **bit-identical** ($\Delta\psi=0$) | machine |

## The crux — the algorithm's answer survives the leakage

The sharp result is G4/G5: even though the field-native entangler is only sub-percent-accurate at finite $U$ (G3), the **Deutsch–Jozsa verdict is exactly correct** on all four oracles. The constant oracles use only single-qubit gates, which are exact (zero leakage, $P(\text{input}{=}1)=0$ identically); the balanced oracles route through the leaky CNOT but the algorithm's answer is a *threshold decision* ($P>\tfrac12$), which the $\sim0.3\%$ doublon leakage cannot flip. This is the honest picture of computing on genuine matter: the gate hardware carries real charge-fluctuation error, and a well-designed algorithm's discrete output is robust to it — the same reason real fault-tolerant schemes decode to a threshold.

## Why it matters

This is the deepest statement of the quantum-computing cross-test. The arc is now: the model *permits* QC (F212), the entangler is *derived* (F214) and *emerges* from second quantization (F217), the substrate *runs* universal algorithms at scale (F218/F222), and now it *computes on genuine second-quantized matter* (F220) — logical qubits that are physical fermion spins, single-qubit gates that are exact fermionic operators, and an entangler that is literally the lattice's own Hubbard time-evolution, with virtual doublons as the native noise source. The exponential Fock space ($2^{2n_\text{sites}}$) is allocated, evolved under a derived Hamiltonian, and made to decide Deutsch–Jozsa — paying the full cost, on real matter.

## What remains open

1. **Noise / error correction.** The doublon leakage seen here is a *native* decoherence channel; formalising it and adding a stabiliser code is the fault-tolerance frontier (F221).
2. **More sites / deeper circuits.** Only two logical qubits (one entangling bond) are exercised in depth; $n_\text{sites}\ge3$ chains and ring-exchange multi-qubit gates are the next step (the machinery is $n$-general).
3. **Leakage suppression.** A pulse-shaped / composite exchange sequence that cancels the leading doublon leakage would push the field-native CNOT toward machine precision at fixed $U/t$.

## Files

- `ca-simulation/ca_second_quant.py` — `fermionic_rotor`, `superexchange_J`, `exchange_time_for_angle`, `exchange_operator`, `fermionic_exchange`, `spin_register`, `fn_hadamard`/`fn_x`/`fn_z`/`fn_cnot`, `apply_program_fock`.
- `src/casim/engine/manybody.py` — `FermionAlgorithmChannel` (`fermion_algorithm`) + `FermionAlgorithmObserver` (`fermion_algorithm_readout`).
- `tests/findings/test_F220_field_native_execution.py` (5/5); `test-results/F220_field_native_execution.json`.
