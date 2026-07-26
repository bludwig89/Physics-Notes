# F222 — The substrate's quantum algorithms **scale**: a native controlled-phase + fully-compiled native CCZ extend the exact universality proof to 3-qubit controlled gates, and multi-controlled Z/X (the exact action of the native Barenco ladder) let $n$-qubit Grover, Bernstein–Vazirani, QFT and GHZ run to $n\approx12$ with the $2^n$ register staying stable to machine precision (norm, unitarity, correct answers, bit-identical checkpointing)

**Date:** 2026-07-01 - 18:40
**Numbering:** **F222** (re-checked per CLAUDE.md; F215/F216 taken by concurrent sessions, F217/F218 are this session's fermion-sector and algorithm findings — F222 verified free).
**Status:** Confirmed — 5/5 checks PASS. Native CCZ/controlled-phase **exact-algebraic** ($<10^{-12}$; $2.2\times10^{-15}$); Grover matches the analytic success probability to $<10^{-6}$; QFT matches the DFT to $<10^{-10}$; BV deterministic; checkpoint bit-identical.
**Modules:** `ca-simulation/ca_entanglement.py` (`native_zz`, `native_cphase`, `native_ccz`, `apply_mcz`, `apply_mcx`, extended circuit runner); `ca-simulation/ca_quantum_algorithms.py` (`grover_nq`, `bernstein_vazirani`, `qft_circuit`, `ghz_circuit`); runs through the existing `quantum_circuit` casim channel unchanged.
**Test / results:** `tests/findings/test_F222_scaled_quantum_algorithms.py` (5/5) → `test-results/F222_scaled_quantum_algorithms.json`
**Cross-references:** [[f218-algorithm-through-the-engine]] (the 2-qubit predecessor this scales), [[f212-dynamical-entanglement-generation]] (perfect-entangler certificate), [[f214-superexchange-and-live-entanglement]] / [[f217-field-native-fermion-entanglement]] (the derived/emergent entangler). External: Grover 1996; Bernstein–Vazirani 1993; Coppersmith QFT; Barenco et al. 1995 (multi-controlled decomposition).

---

## What F218 left open

F218 exercised only 2-qubit algorithms. Its first open item was **scale**: multi-controlled gates and $n\ge3$ algorithms, and — the physics question — whether the genuine $2^n$ register stays stable as $n$ grows, or whether the exact-unitary story degrades into floating-point mush at the exponential cost. F222 closes it constructively.

## Extending the native gate set

Two new exactly-compiled primitives extend the F218 universality proof upward:

**General native controlled-phase.** Using $a\wedge b=\tfrac14(I-Z_a-Z_b+Z_aZ_b)$,

$$\mathrm{CP}(\varphi)=e^{i\varphi/4}\,e^{i\frac{\varphi}{4}Z_aZ_b}\,e^{-i\frac{\varphi}{4}Z_a}\,e^{-i\frac{\varphi}{4}Z_b},$$

where the $ZZ$ piece is `native_zz`$(\varphi/4)$ — two lattice exchange gates sandwiching a $\sigma_z$ conjugation, exactly as in F218 but at arbitrary angle — and each single-$Z$ piece is a native SU(2) rotor $\exp(-i\tfrac{\varphi}{4}\sigma_z)$. (`native_zz` carries a constant, angle-independent global $-1$ from its two $-i$ conjugation factors; it is absorbed so the primitive lands exactly on $\exp(i\theta\,\sigma_z\!\otimes\!\sigma_z)$.)

**Native CCZ.** With $V=\sqrt{Z}=S=\mathrm{CP}(\pi/2)$ and the native CNOT, the Barenco three-qubit construction

$$\mathrm{CCZ}=\mathrm{CS}_{2,3}\,\mathrm{CNOT}_{1,2}\,\mathrm{CS}^\dagger_{2,3}\,\mathrm{CNOT}_{1,2}\,\mathrm{CS}_{1,3}$$

reproduces $\mathrm{diag}(1,\dots,1,-1)$ to $2.2\times10^{-15}$ — a genuine **3-qubit** controlled gate built entirely from the lattice exchange interaction plus single-cell rotations, lifting F218's 2-qubit universality certificate one level.

**Multi-controlled Z/X at scale.** A general $\mathrm{MCZ}$/$\mathrm{MCX}$ decomposes (Barenco) into CCZ + CNOT ladders, whose *action* on the state vector is exact and cheap: $\mathrm{MCZ}$ flips the sign of the all-controls-$=1$ block, $\mathrm{MCX}$ swaps the target slices there. The circuit runner applies these directly to the $2^n$ vector (`apply_mcz`/`apply_mcx`), so algorithms scale without ever forming a $2^n\times2^n$ matrix. This is the same discipline as F218's `CNOT_REF`: the exact action of a gate whose native compilation is certified constructively at small $n$ (here CCZ) and guaranteed to exist at all $n$.

## Results (5/5 PASS)

| # | Check | Result | Tier |
|---|---|---|---|
| G1 | native CCZ + CP exact | `native_ccz` $=\mathrm{diag}(1,\dots,-1)$ to $2.2\times10^{-15}$; `native_cphase`$(\varphi)$ to $5.6\times10^{-16}$ over four angles; both unitary | **exact-algebraic** |
| G2 | $n$-qubit Grover | $n=3\ldots12$: argmax $=$ marked, success $P$ matches the analytic $\sin^2\!\big((2r{+}1)\arcsin 2^{-n/2}\big)$ to $<10^{-6}$ ($P=0.945\to0.99995$); worst norm error $1.5\times10^{-13}$ | machine |
| G3 | QFT correct + invertible | $n=3\ldots8$: matches the DFT to $<10^{-10}$ and $\mathrm{QFT}^\dagger\mathrm{QFT}=I$ (round-trip $<10^{-10}$) | machine |
| G4 | Bernstein–Vazirani | $n=4\ldots12$: secret string recovered in **one** oracle query, input-register marginal deterministic ($P=1$) | machine |
| G5 | stability + engine | GHZ every-cut entropy $=\ln 2$ to $n=12$; **live** 8-qubit Grover through the engine returns the marked item ($P=0.9999$); checkpoint mid-algorithm resumes **bit-identical** ($\Delta\psi=0$) | machine |

## The crux — exponential cost, no exponential error

The register is the honest $2^n$ object; nothing is factorised or approximated. The finding's content is that paying the full exponential cost does **not** buy exponential floating-point error: across a 12-qubit Grover (50 iterations, ~600 gate layers) the norm drifts by $10^{-13}$ and the success probability tracks the closed-form Grover rotation to $<10^{-6}$; the QFT reproduces the discrete Fourier transform to $10^{-10}$ and inverts exactly; GHZ holds $\ln 2$ on every cut out to 12 qubits. The substrate is a *stable* universal quantum computer at scale, not merely a 2-qubit proof of concept — and it remains checkpoint-exact mid-computation, so long algorithms are reproducible bit-for-bit.

## Why it matters

F218 established *that* the lattice computes; F222 establishes that it **keeps** computing as the register grows, with the exact-unitary guarantees intact. The native gate set is now genuinely universal in practice — arbitrary controlled-phase, CCZ, and multi-controlled logic — and four textbook algorithm families run through the same engine that carries the photon, gauge, and gravity sectors. This is the platform the noise / error-correction tier (the remaining F218 frontier) is built on: you cannot study fault tolerance until the noiseless machine is demonstrably stable at scale, which it now is.

## What remains open

1. **Field-native execution.** These gates act on the abstract register; running a scaled algorithm on the `fermion_chain` (F217) Fock sector is the companion finding (F220).
2. **Noise / error correction.** The register is exact-unitary; a decoherence channel + stabiliser code is the fault-tolerance frontier (F221).
3. **Deeper circuits.** Only single-marked Grover, one-query BV/DJ, and the bare QFT are exercised; period-finding / phase-estimation stacks built on the QFT are the next algorithmic layer.

## Files

- `ca-simulation/ca_entanglement.py` — `native_zz`, `native_cphase`, `native_ccz`, `apply3`/`_embed_2q` (matrix assembly), `apply_mcz`, `apply_mcx`, and the extended `_gate_matrix`/`apply_layer` (specs `cphase`, `ccz`, `mcz`, `mcx`).
- `ca-simulation/ca_quantum_algorithms.py` — `grover_iterations`, `grover_nq`, `bernstein_vazirani`, `qft_circuit`, `ghz_circuit`.
- `tests/findings/test_F222_scaled_quantum_algorithms.py` (5/5); `test-results/F222_scaled_quantum_algorithms.json`.
