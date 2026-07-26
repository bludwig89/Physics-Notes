# F218 — The substrate **computes**: CZ/CNOT compile **exactly** from the lattice exchange interaction ($\boldsymbol\sigma\!\cdot\!\boldsymbol\sigma$ commutes with $ZZ$; two exchange gates + a $\sigma_z$ give $e^{i\pi/4\,ZZ}$), and 2-qubit Grover + Deutsch–Jozsa run **live through the `casim` engine** — Grover finds every marked item with probability 1, checkpoint/resume mid-algorithm bit-identical

**Date:** 2026-07-01 - 17:45
**Numbering:** **F218** (re-checked per CLAUDE.md; F215/F216 taken by concurrent sessions, F217 is the fermion-sector finding from this session — F218 verified free).
**Status:** Confirmed — 5/5 checks PASS. Native gate compilation **exact-algebraic** (CZ/CNOT to $<10^{-12}$; $6\times10^{-16}$); Grover/DJ deterministic (probabilities exactly $0$/$1$); checkpoint/resume bit-identical.
**Modules:** `ca-simulation/ca_entanglement.py` (native `native_cz`/`native_cnot`/`native_hadamard`/`native_zz_quarter` + circuit runner); `ca-simulation/ca_quantum_algorithms.py` (Grover, Deutsch–Jozsa); `src/casim/engine/manybody.py` (`QuantumCircuitChannel` + `CircuitReadoutObserver`).
**Test / results:** `tests/findings/test_F218_algorithm_through_engine.py` (5/5) → `test-results/F218_algorithm_through_engine.json`
**Cross-references:** [[f212-dynamical-entanglement-generation]] (perfect-entangler universality certificate — this finding is the constructive complement), [[f214-superexchange-and-live-entanglement]] / [[f217-field-native-fermion-entanglement]] (the entangler and its derivation), [[F133-blockspin-casim-engine]] (schedulable engine-op precedent). External: DiVincenzo et al. (√SWAP universality); Grover 1996; Deutsch–Jozsa 1992.

---

## From generating entanglement to computing with it

F212 proved the exchange gate is a *perfect entangler* (universality by existence theorem). F218 makes it **constructive and operational**: it compiles a universal gate set exactly, and runs genuine algorithms through the production engine. This is the step from "the substrate can entangle" to "the substrate computes."

## Exact exchange → CNOT compilation

The lattice exchange operator is $\boldsymbol\sigma_A\!\cdot\!\boldsymbol\sigma_B=XX+YY+ZZ$. Two facts make it exactly compilable:

1. $[XX+YY+ZZ,\;ZZ]=0$ (the $X$–$Z$ anticommutation makes $XXZZ=ZZXX$, likewise $YY$).
2. Conjugation by $\sigma_z\otimes I$ flips the $XX,YY$ signs: $(\sigma_z\!\otimes\!I)(XX+YY+ZZ)(\sigma_z\!\otimes\!I)=-XX-YY+ZZ$.

Because the two exponents commute, two native exchange gates sandwiching a $\sigma_z$ give a **pure $ZZ$ interaction**:

$$e^{+i\frac{\pi}{8}\boldsymbol\sigma\cdot\boldsymbol\sigma}\,(\sigma_z\!\otimes\!I)\,e^{+i\frac{\pi}{8}\boldsymbol\sigma\cdot\boldsymbol\sigma}\,(\sigma_z\!\otimes\!I)=e^{i\frac{\pi}{4}ZZ},$$

verified to $5\times10^{-16}$. Then $\mathrm{CZ}=e^{i\pi/4}e^{i\frac{\pi}{4}ZZ}\,(R_z(\tfrac\pi2)\!\otimes\!R_z(\tfrac\pi2))$ and $\mathrm{CNOT}=(I\!\otimes\!H)\,\mathrm{CZ}\,(I\!\otimes\!H)$, with $\sigma_z$, $R_z$, $H$ all native SU(2) rotors. The assembled gates match the textbook CZ/CNOT to $6\times10^{-16}$ (G1) — a *constructive* proof that the lattice exchange interaction plus single-cell rotations is universal.

## Algorithms live in the engine (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | native gate set exact | $e^{i\pi/4 ZZ}$, CZ, CNOT, H from exchange+rotors to $<10^{-12}$ ($6\times10^{-16}$); all unitary | **exact-algebraic** |
| G2 | 2-qubit Grover (direct) | every marked item $w\in\{0,1,2,3\}$ found with $P=1$ after one iteration ($<10^{-12}$) | machine |
| G3 | **Grover LIVE in engine** | `quantum_circuit` channel runs the circuit one layer per tick; final argmax $=w$, $P=1$; norm conserved | machine |
| G4 | Deutsch–Jozsa (1 query) | all four oracles classified correctly: const→$P(q_0{=}1)=0$, balanced→$1$ (deterministic) | machine |
| G5 | engine integrity | checkpoint mid-circuit → resume is **bit-identical** ($\Delta\psi=0$) and still returns the right answer | machine |

The `QuantumCircuitChannel` holds the genuine $2^n$ register and applies one circuit layer per CA tick; the `CircuitReadoutObserver` records the computational-basis probabilities as the algorithm executes. A 4-item Grover search collapses onto the marked state with certainty (the exact single-iteration rotation $\theta=\arcsin\tfrac12$), and Deutsch–Jozsa decides constant-vs-balanced with a single oracle query — both running inside the same engine that carries the photon, gauge, and gravity sectors, with every gate reduced to the lattice exchange interaction.

## Why it matters

This closes the quantum-computing cross-test loop end to end. The arc is now: the model *permits* QC (F212, perfect entangler), the entangler's coupling is *derived* from the `ca_dirac` hopping (F214) and *emerges* from genuine second quantization (F217), and the substrate *runs* real quantum algorithms with a universal gate set compiled exactly from its own exchange interaction (F218). Nothing here is imported from textbook quantum computing except the algorithm *definitions*; the gate *hardware* is the lattice. The exponential $2^n$ Hilbert space is allocated, evolved, checkpointed, and made to compute — the sharpest possible statement that the model supports quantum computation, and a reminder that it does so by paying the full exponential cost, not by any classical shortcut.

## What remains open

1. **Scale.** Only 2-qubit algorithms are exercised; multi-controlled gates and $n\ge3$ algorithms (Grover on more items, Bernstein–Vazirani, small QFT) are the next step (the channel already supports arbitrary $n$ and CNOT chains).
2. **Field-native execution.** Gates act on the abstract register; running an algorithm on the `fermion_chain` (F217) Fock sector — computation on genuine second-quantized matter — is the deep tier.
3. **Noise / error correction.** The register is exact-unitary; adding a decoherence channel and a small stabilizer code would let the engine study fault tolerance, the frontier the 2026 hardware is on.

## Files

- `ca-simulation/ca_entanglement.py` — `native_hadamard`, `native_zz_quarter`, `native_cz`, `native_cnot`, `apply_layer`, `run_circuit`, `probabilities`.
- `ca-simulation/ca_quantum_algorithms.py` — `grover_2q`, `deutsch_jozsa_1`, `measured_bit0_probability`.
- `src/casim/engine/manybody.py` — `QuantumCircuitChannel` (`quantum_circuit`) + `CircuitReadoutObserver` (`circuit_readout`).
- `tests/findings/test_F218_algorithm_through_engine.py` (5/5); `test-results/F218_algorithm_through_engine.json`.
