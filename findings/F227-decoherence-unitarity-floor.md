# F227 — Route 4: the discrete substrate has **no observable intrinsic-decoherence floor** — the effective-theory unitarity floor is exactly zero, any residual is Planck-suppressed to $\lesssim10^{-40}\,\text{s}^{-1}$ (F130 LIV-irrelevance), the Lieb–Robinson velocity $=c_\text{lat}=1/\sqrt3$ exactly, and the only material-scale channel is the emergent doublon leakage (separated by $\sim50$ orders)

**Date:** 2026-07-02 - 14:20
**Numbering:** **F227** (re-checked per CLAUDE.md; F215–F226 taken/created — F227 free). Companion to F226 (Route 3). Executes Route 4 of `docs/roadmaps/qc-routes-3-4-prompt.md`.
**Status:** Confirmed — 5/5 checks PASS. The Lieb–Robinson speed identity $d\Omega/d\lvert k\rvert=c_\text{lat}$ is **exact** ($10^{-16}$); the strict causal cone ($C=0$ for $r>4t$) is **machine-precision exact**; the intrinsic-rate magnitudes and experimental confrontation are quantitative.
**Verdict:** The model predicts **no intrinsic decoherence floor** at any observable level — it is a **unitary theory with no objective collapse**. The floor sits $\gtrsim9$ orders below the best measured decoherence and $\gtrsim20$ orders below the deepest collapse-model rate, so this route does **not** yield a near-term test. That null result is the deliverable.
**Modules:** `ca-simulation/ca_decoherence_floor.py` (intrinsic-rate estimates; Lieb–Robinson cone; collapse-model + experiment confrontation; doublon-leakage separation).
**Test / results:** `tests/findings/test_F227_decoherence_floor.py` (5/5) → `test-results/F227_decoherence_floor.json`.
**Cross-references:** [[F180-gravitational-wave-speed]] (the signal-speed machinery reused: $c_\text{grav}=c_\text{lat}$, slope identity), [[F130-blockspin-rg-gauge-gravity]] (LIV operators RG-irrelevant, $\lambda_n=b^{-n}$), [[F26-speed-of-light-as-rotation-rate]] ($c_\text{lat}=1/\sqrt3$), [[F222-scaled-quantum-algorithms]] (register norm drift $\sim10^{-13}$ = floating point), [[F220-field-native-execution]] / [[F225-doublon-leakage-spinqubit]] (the emergent doublon-leakage channel), [[F123-p6-si-scale-matter-sector]] / [[F107-canonical-a-adoption-L4-grb-gate]] (SI bridge $\tau,a$). External: GRW; Adler CSL $\lambda=10^{-8\pm2}\,\text{s}^{-1}$ (X-ray-excluded); Diósi–Penrose $R_0\gtrsim4$ Å; Sr optical-lattice clock $T_2^*=118$ s (2025); transmon $T_{2,\text{echo}}=1.06$ ms (2025); Lieb–Robinson bound.

---

## The question (Route 4)

If the lattice is physical, does a long quantum computation show any intrinsic departure from perfect unitarity — a minimum decoherence rate, a maximum entangling velocity (a Lieb–Robinson bound $=c_\text{lat}$), or a gate-error floor — set by the spacing $a$ and $c_\text{lat}$? F222 finds the register's norm drift is pure floating point ($\sim10^{-13}$): the model asserts **no** intrinsic floor. This finding makes that assertion quantitative and bounds it against experiment.

## 1. The intrinsic unitarity floor is zero / Planck-suppressed (G1)

**Effective theory: exactly zero.** The emergent gates ($U_\text{exch}$, the SU(2) rotors, and everything compiled from them) are *exact unitaries*. At the level where the model reproduces QM there is **no** intrinsic decoherence; the F222 register norm drift $\sim10^{-13}$ is floating-point round-off, not physics.

**Substrate: Planck-suppressed.** The only way discreteness could induce non-unitarity is through Lorentz-violating (LIV) operators in the underlying walk, and F130 proves these are **RG-irrelevant** ($\lambda_n=b^{-n}$, $n\ge2$). Coarse-graining from the Planckian cell to a physical scale (resolution factor $b^N=E_\text{lat}/E$) suppresses the leading ($n=2$) operator by $(E/E_\text{lat})^2$, so any residual decoherence rate is at most

$$\Gamma_\text{intrinsic}\ \lesssim\ \frac{E}{\hbar}\Big(\frac{E}{E_\text{lat}}\Big)^{2}=\frac{E^{3}}{\hbar\,E_\text{lat}^{2}},\qquad E_\text{lat}\equiv\frac{\hbar}{\tau}=3.20\times10^{27}\ \text{eV}.$$

For an optical-scale qubit ($E=1.8$ eV) this is $\Gamma_\text{LIV}\approx8.6\times10^{-40}\,\text{s}^{-1}$. A deliberately pessimistic single-power ceiling $\Gamma\lesssim E^2/(\hbar E_\text{lat})=E^2\tau/\hbar^2\approx1.5\times10^{-12}\,\text{s}^{-1}$ still leaves the floor unobservable. The **exponent is the message**: the floor is not merely small, it is suppressed by (at least) two powers of the Planckian hierarchy, exactly as F130's irrelevance requires.

## 2. Lieb–Robinson / maximum entangling velocity $=c_\text{lat}$ (G2, G3)

**Fundamental speed (exact).** Reusing the F26/F105/F180 machinery, the on-axis dispersion is $\Omega(\mathbf k)=\lvert\mathbf k\rvert/\sqrt3$, so the signalling/group velocity is

$$\frac{d\Omega}{d\lvert k\rvert}\bigg|_{k\to0}=\frac{1}{\sqrt3}=c_\text{lat}\quad(\text{to }10^{-16}).$$

This is the QC-sector analogue of the F180 result $c_\text{grav}=c_\text{photon}=c_\text{lat}$: information in the substrate cannot propagate faster than the one light cone of the lattice.

**Strict causal cone (exact).** The register's gates are nearest-neighbour, so entanglement obeys a hard Lieb–Robinson cone. Evolving a Néel product $|0101\ldots\rangle$ under a brick-wall of native exchange gates, the connected correlation $C(r,t)=\langle Z_0Z_r\rangle-\langle Z_0\rangle\langle Z_r\rangle$ is **exactly zero** (machine precision) for $r>4t$ — each brick-wall tick spreads a single operator by 2 cells, and the two-point correlator (two Heisenberg-evolved operators) has cone $4t$. There is **no instantaneous propagation**: the substrate is causal, with a finite maximum entangling velocity bounded by $c_\text{lat}$. (The emergent super-exchange chain saturates a *smaller* velocity $v_\text{eff}\sim J<c_\text{lat}$ because super-exchange is a second-order/virtual process — always inside the light cone.)

## 3. Confrontation with collapse models and experiment (G4)

| Bound | Rate (s$^{-1}$) | vs model floor |
|---|---|---|
| Measured Sr-clock decoherence ($1/T_2^*$, $T_2^*=118$ s) | $8.5\times10^{-3}$ | conservative ceiling $1.5\times10^{-12}$ is **9.7 orders below** |
| Measured transmon decoherence ($1/T_2$, $1.06$ ms) | $9.4\times10^{2}$ | conservative ceiling **14.8 orders below** |
| CSL, GRW value | $10^{-16}$ | model rate $8.6\times10^{-40}$ is **23 orders below** |
| CSL, Adler value (X-ray-**excluded**) | $10^{-8}$ | model rate **31 orders below** |
| Diósi–Penrose $R_0\gtrsim4$ Å | — | model has **no DP collapse term** |

The model's intrinsic floor sits below **every** current bound. Crucially, the model is a **unitary theory with no objective-collapse term**: it does not contain CSL's stochastic per-nucleon localisation or the DP gravitational self-collapse (gravity here is the deterministic, unitary dielectric $K$ of F64/F178). So it *predicts* the continued null results of collapse-model searches. This distinguishes the model *in principle* from GRW/CSL/DP — but only as a null prediction, testable solely if collapse were ever detected; against all present data it is simply consistent. **Route 4 yields no near-term discriminating test.**

## 4. The one non-Planck channel — emergent doublon leakage (G5)

The prompt's caution is kept strictly: the model has exactly **one** native decoherence channel that is *not* Planck-suppressed — the **emergent doublon leakage** $d=(2t/U)^2$ of the field-native exchange gate (F220/F225), which reproduces the measured $0.13\%$ leakage of a GaAs exchange qubit at $U/t\approx55$. This is a **material-scale** ($\sim10^{-3}$ per gate) two-site-Hubbard effect of the *effective* model, present in any Hubbard system — **not** a fundamental discreteness floor. Per gate operation the two channels are separated by

$$\frac{d_\text{doublon}}{\Gamma_\text{intrinsic}\,\tau_\text{gate}}\sim10^{51}\quad(\sim52\ \text{orders}),$$

so "emergent material-scale leakage" and "fundamental Planckian floor" differ by $\sim50$ orders and must never be conflated: the former is a real, measured, device-level error (F225); the latter is unobservable.

## What this closes and what remains

**Closes:** the Route-4 yes/no question. Answer: **no observable intrinsic floor** — the effective-theory unitarity floor is exactly zero, the substrate residual is Planck-suppressed ($\lesssim10^{-40}\,\text{s}^{-1}$, two-power-suppressed per F130), the Lieb–Robinson velocity equals $c_\text{lat}=1/\sqrt3$ exactly, and the model is unitary with no objective collapse. It sits below all current bounds ⇒ **no near-term test from this route**.

**Open:** (i) a first-principles calculation of the LIV-induced non-unitarity *coefficient* (here bounded, not computed — the model's structural claim is that it vanishes in the IR); (ii) if any future experiment reaches the $10^{-12}\,\text{s}^{-1}$ conservative ceiling it would begin to probe the pessimistic single-power bound, though the F130 result argues the true rate is far below even that.
