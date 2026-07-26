# F221 — The engine gains **fault-tolerance machinery**: Kraus decoherence channels + stabilizer codes built on the native gate set. The 3-qubit code's corrected fidelity matches the exact closed form $F=(1-3p^2+2p^3)+(3p^2-2p^3)(2ab)^2$ to machine precision with logical infidelity suppressed to $O(p^2)$ (vs uncorrected $O(p)$); the 9-qubit Shor code corrects an **arbitrary** single-qubit error (all $27=\{X,Y,Z\}\times9$) to $<10^{-12}$; and a live `error_correction` channel holds a logical qubit at $F=0.995$ over 8 noise rounds while the uncorrected control decays to $0.27$

**Date:** 2026-07-01 - 20:15
**Numbering:** **F221** (re-checked per CLAUDE.md; F215/F216 concurrent-session findings, F217–F220 this session — F221 verified free).
**Status:** Confirmed — 5/5 checks PASS. Channels are exact CPTP ($\sum E^\dagger E=I$ to $10^{-16}$); 3-qubit code fidelity **exact-algebraic** ($4.4\times10^{-16}$ vs closed form); Shor arbitrary single-error correction to $4.4\times10^{-16}$; pseudo-threshold and live decay/hold demonstrated; checkpoint bit-identical.
**Modules:** `ca-simulation/ca_quantum_noise.py` (Kraus channels, native-gate encoders, stabilizer recovery, analytic references); `src/casim/engine/manybody.py` (`ErrorCorrectionChannel` + `ErrorCorrectionObserver`).
**Test / results:** `tests/findings/test_F221_noise_error_correction.py` (5/5) → `test-results/F221_noise_error_correction.json`
**Cross-references:** [[f220-field-native-execution]] (the native decoherence source — virtual doublon leakage — this formalises), [[f218-algorithm-through-the-engine]] / [[f222-scaled-quantum-algorithms]] (the exact-unitary sectors this adds noise to), [[f212-dynamical-entanglement-generation]] (the native gate set the codes are built from). External: Shor 1995 (9-qubit code); Nielsen & Chuang (stabilizer formalism); Knill–Laflamme error-correction conditions.

---

## What F218/F222/F220 left open

F218's third open item was **noise / error correction**: the register sectors are exact-unitary, so the engine had no way to study fault tolerance. F220 made the need concrete by exposing a *native* decoherence source — virtual **doublon leakage** out of the one-per-site qubit subspace, a genuine charge-fluctuation error carried by the field-native gates. F221 gives the engine the two missing ingredients — an explicit noise channel and error-correcting codes — both built on the model's own native gates (exchange-derived CNOT + SU(2) rotors), so fault tolerance can be studied on the same substrate.

## The construction

**Exact channel averaging.** A decoherence channel is a Kraus set $\{E_k\}$ with $\sum_k E_k^\dagger E_k=I$ acting as $\rho\mapsto\sum_k E_k\rho E_k^\dagger$. The engine carries the full $2^n\times2^n$ density matrix (small $n$), so the channel is applied **exactly** — no Monte-Carlo sampling. Bit-flip, phase-flip, depolarizing, and amplitude-damping channels are provided; the single-qubit Paulis are the model's own (from the SU(2) rotor).

**Codes from native gates.** Encoders are native CNOT fan-outs (+ Hadamards for the phase basis): the 3-qubit bit-flip code ($|0_L\rangle=|000\rangle$, $|1_L\rangle=|111\rangle$; stabilizers $Z_0Z_1,Z_1Z_2$), its Hadamard-dual phase-flip code, and the 9-qubit Shor code (phase-flip code of three bit-flip blocks). Recovery is stabilizer syndrome extraction by projective measurement plus the Pauli correction, on the density matrix as $\rho\mapsto\sum_s C_s P_s\rho P_s C_s^\dagger$ — exact and deterministic.

## Results (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | channels are CPTP | $\sum_k E_k^\dagger E_k=I$ to $1.1\times10^{-16}$ for all four channels; $\rho$ stays Hermitian, trace-1, PSD | exact |
| G2 | 3-qubit code exact + $O(p^2)$ | corrected fidelity $=(1{-}3p^2{+}2p^3)+(3p^2{-}2p^3)(2ab)^2$ to $4.4\times10^{-16}$; logical infidelity $\propto p^2$ (ratio $\to0.087$) vs uncorrected $O(p)$ | **exact-algebraic** |
| G3 | Shor arbitrary single-error | every $\{X,Y,Z\}$ on every one of the 9 qubits (27 errors) corrected with fidelity 1 to $4.4\times10^{-16}$ | **exact-algebraic** |
| G4 | pseudo-threshold | $F_\text{corr}>F_\text{uncorr}$ for all tested $p$ (0.05–0.3), for both bit-flip and phase-flip codes | quantitative |
| G5 | live in engine | `error_correction` channel holds a logical qubit at $F=0.9947$ over 8 noise rounds while the uncorrected control decays to $0.2690$; trace preserved; checkpoint mid-run **bit-identical** ($\Delta\rho=0$) | quantitative + machine |

## The crux — the exact fidelity formula and its quadratic suppression

The finding's sharpest content is G2. Naively one expects the 3-qubit code to succeed whenever $\le1$ physical flip occurs (probability $1-3p^2+2p^3$). But the density-matrix computation gives a *higher* fidelity, and the reason is exact and instructive: the $\ge2$-flip events **miscorrect to the logical-flipped state** $X_L|\psi\rangle$, which still overlaps the target by $(2ab)^2$. So

$$F_\text{corr}(p)=(1-3p^2+2p^3)+(3p^2-2p^3)(2ab)^2,$$

matching the simulated density matrix to $4.4\times10^{-16}$. The logical **infidelity** is therefore $1-F_\text{corr}=(3p^2-2p^3)\big(1-(2ab)^2\big)=O(p^2)$ — the quadratic error suppression that is the entire purpose of a code, turning a physical error rate $p$ into a logical rate $\sim p^2$ below the pseudo-threshold. The engine reproduces this exactly, and the Shor code lifts it to correction of an *arbitrary* single-qubit error (G3), satisfying the Knill–Laflamme conditions to machine precision.

## What needs to be put in place (the frontier)

This establishes the ingredients; the honest fault-tolerance programme still needs:

1. **Fault-tolerant gates + syndrome extraction.** Here syndromes are read by ideal projective measurement; a real scheme needs noisy ancilla-based syndrome circuits and transversal/lattice-surgery logical gates so the *correction* is itself error-resilient.
2. **A distance-scaling code (surface code).** The 3-/9-qubit codes fix a single error; a threshold theorem needs a code family whose distance grows, with a decoder — the surface code on the lattice is the natural fit and the next build.
3. **Coupling the code to the native noise.** The physically-motivated channel is the F220 **doublon leakage** (a leakage error, not a Pauli error); a leakage-reduction unit + a code that tolerates leakage is what the field-native sector actually calls for.
4. **Repeated-round / circuit-level noise.** G5 applies noise between ideal corrections; interleaving noisy gates, idle errors, and measurement errors per round is needed for a real logical-error-rate curve.

## Why it matters

The quantum-computing cross-test is now complete end to end: the model *permits* QC (F212), the entangler is *derived* (F214) and *emerges* (F217), the substrate *runs universal algorithms at scale* (F218/F222) *on genuine matter* (F220), and now it can *protect* a logical qubit against decoherence with codes built from its own native gates (F221) — reproducing the exact quadratic error suppression and arbitrary-single-error correction that define quantum error correction. The engine that carries the photon, gauge, and gravity sectors now also carries a working, if minimal, fault-tolerance laboratory, with a clearly scoped path (surface code + leakage handling) to a genuine threshold study.

## Files

- `ca-simulation/ca_quantum_noise.py` — `kraus_bitflip/phaseflip/depolarizing/amp_damp`, `apply_channel(_all)`, `encode_bitflip/phaseflip/shor`, `recover_bitflip/phaseflip/shor`, `bitflip_corrected_fidelity`/`bitflip_uncorrected_fidelity`, `fidelity`, `embed`/`embed2`/`density`.
- `src/casim/engine/manybody.py` — `ErrorCorrectionChannel` (`error_correction`) + `ErrorCorrectionObserver` (`error_correction_fidelity`).
- `tests/findings/test_F221_noise_error_correction.py` (5/5); `test-results/F221_noise_error_correction.json`.
