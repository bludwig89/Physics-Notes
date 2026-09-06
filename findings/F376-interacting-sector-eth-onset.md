# F376 — G10 residual: the free sector's GGE breaks down toward genuine (ETH) thermalisation once an integrability-breaking interaction is turned on, but *not* from a nearest-neighbour interaction alone

**Date:** 2026-09-06 - 01:30
**Status:** **Confirmed — 7/7 PASS**, one declared control verified red. Rubric row **G10** (PARTIAL) gets its first interacting-sector result: F300 sec4.1 and F309 sec7.2 both name "thermalisation on F110's link Hamiltonian" as the open next step, and until this finding no interacting sector had been attempted at all. Three legs are exact/machine-precision (the fermionic-sign construction check, the reflection-parity block-diagonalisation, the declared control), four are quantitative (the level-spacing-ratio separation and its finite-size flow, the entanglement-plateau/ceiling-fraction ordering, the ETH eigenstate-fluctuation trend).
**Module:** `src/casim/engine/interactions/thermodynamics_interacting.py`
**Test record:** `F376-interacting-sector-eth-onset` (gate tier)
**Results:** `test-results/F376_interacting_sector_eth_onset.json`
**Claim card:** `docs/claims/CL305-interacting-sector-eth-onset.md`
**Reviewed:** 2026-09-06 — **CONFIRMED** ([independent review](../docs/reviews/F376-review-2026-09-06.md))

**Cross-references:** [[F300-lattice-native-thermodynamics]] (sec4.1 — the 2N conserved branch occupations, the GGE result, and the named next step this finding executes), [[F309-gstar-from-model-content]] (sec7.2 — "nothing here shows the fermionic sector thermalises either", reaffirming the same caveat), [[F110-realtime-link-hamiltonian-confinement]] (the real-time link Hamiltonian named as the next step, and sec5's own statement that dynamical matter is not yet coupled to it — why this finding does not attempt that coupling directly), [[F294-c7-chi-map-ncolour-audit]] (the deferred SU(N) ladder F300/F309 both point to as the eventual gauge-side partner of this question).

---

## 1. What was open, and what this closes

F300 built lattice-native thermodynamics for the model's free (quadratic) photon sector and proved, exactly, that the branch occupations $n_\pm(\mathbf k)$ are conserved charges — $2N$ of them for an $N$-site lattice — so the free sector's stationary state is a **generalised Gibbs ensemble (GGE)**, never a Gibbs state (F300 sec4.1). F309 extended the equilibrium side of the same machinery to the fermionic content and closed with the identical caveat: *"nothing here shows the fermionic sector thermalises either"* (F309 sec7.2). Both findings name the same next step, verbatim: **thermalisation on F110's link Hamiltonian.**

F110's link Hamiltonian, read literally, is not that step. It is a pure Kogut–Susskind gauge construction on **static** charges, and F110 sec5 says so without qualification: *"Dynamical (quark) matter is not yet coupled; that coupling is the next leg of the P2 chain."* Coupling F110's gauge degrees of freedom to F300/F309's Gaussian fermion machinery is a real, separate, and larger engineering project — building a lattice gauge theory with dynamical matter — and is not attempted here. What this finding does instead is ask the question F300/F309 actually left open (*does the free sector's GGE give way to genuine thermalisation once an interaction is turned on*) using the smallest interacting extension of the free-fermion lattice machinery that is both (a) inherited from the same conserved-charge structure F300/F309 already established and (b) small enough to diagonalise exactly, with no truncation.

**The result has two tiers, and the second tier is the informative one.** A nearest-neighbour density–density interaction alone is *not* enough — it trades one integrable model for another (Sec. 2). A second, next-nearest-neighbour term breaks integrability genuinely, and three independent, standard diagnostics agree that the GGE gives way to eigenstate thermalisation (Sec. 4–6). Turning on "an interaction" is not sufficient; turning on an interaction that generically breaks the conserved-charge structure is.

---

## 2. The minimal extension, and why it needs two terms and not one

F300/F309's structural result — an extensive tower of exactly conserved single-particle-mode occupations, giving a GGE rather than a Gibbs state — is not particular to the 3D BCC two-branch dispersion. It is the generic feature of **any** quadratic fermion lattice Hamiltonian: a quadratic $H$ is diagonalised by some set of single-particle modes, and their occupations are then exactly conserved operators. So the smallest faithful reproduction of the question doesn't need the full 3D BCC walk — it needs a quadratic fermion lattice with the same conserved-charge structure, small enough to exactly diagonalise, plus the minimal term that breaks it.

$$H = -t\sum_{i=0}^{L-2}\bigl(c_i^\dagger c_{i+1} + \text{h.c.}\bigr) \;+\; V_1\sum_{i=0}^{L-2} n_i n_{i+1} \;+\; V_2\sum_{i=0}^{L-3} n_i n_{i+2}$$

— an open (OBC) spinless-fermion chain, half filling $N=L/2$, $t=1$. This is not an arbitrary reduction: the free term ($V_1=V_2=0$) is exactly the quadratic structure F300/F309 studied, reduced to one band; and the **nearest-neighbour-only** interacting case ($V_1\neq0,\,V_2=0$) is the textbook $t$–$V$ model, which is exactly Jordan–Wigner-dual to the XXZ spin chain and remains **Bethe-ansatz integrable for every value of $V_1$**. So "the smallest interacting extension" in the naive sense turns on an interaction without generically breaking integrability — it swaps one exactly solvable model for another. Reaching a generic, non-integrable point requires a second term; adding a next-nearest-neighbour interaction $V_2$ is the standard, minimal choice in the eigenstate-thermalisation-hypothesis (ETH) literature for leaving the integrable manifold (Santos & Rigol, *Onset of quantum chaos in one-dimensional bosonic and fermionic systems and its relation to thermalization*, Phys. Rev. E **81**, 036206 (2010), arXiv:0910.2985 — that paper studies exactly this $t$–$V$–$V'$ family and reports the crossover from integrable to chaotic level statistics as the next-nearest-neighbour term is turned on).

Three regimes are run side by side at matched $L$, $t=1$:

| tag | $V_1$ | $V_2$ | character |
|---|---|---|---|
| `free` | 0 | 0 | quadratic; every single-particle mode occupation exactly conserved (F300/F309's own structural feature) |
| `integrable_V1` | 0.5 | 0 | interacting, but Jordan-Wigner-integrable (XXZ) |
| `generic_V1V2` | 0.5 | 0.5 | generic, expected non-integrable |

---

## 3. Construction, and how the fermionic sign convention was validated

Basis: fixed-particle-number occupation states, $\dim=\binom{L}{N}$ (no truncation). Fermionic sign convention: $c_k|n\rangle = (-1)^{P(n,k)}|n\text{ with bit }k\text{ cleared}\rangle$ where $P(n,k)$ is the parity of the number of occupied sites with index $<k$ (standard second-quantised convention). This was validated two independent ways before any physics was measured:

* **C0 — exact free-fermion spectrum.** At $V_1=V_2=0$ the many-body ground-state energy must equal the sum of the $N$ lowest single-particle OBC tight-binding energies, $-2t\cos(k\pi/(L+1))$, $k=1,\dots,L$. Checked at $L=6,8,10,12,14$: worst residual $7.1\times10^{-15}$.
* **Independent full-Fock-space cross-check (not a gate-tier check, reported here for completeness).** The combinatorial-basis Hamiltonian was compared, elementwise, against an entirely independent construction built from $2^L$-dimensional Jordan–Wigner Pauli-matrix operators ($\sigma^\pm$ with a $\sigma^z$ string for the hopping term, plain diagonal projectors for the interaction/potential terms — the two constructions share no code), for $L=6$, all three regimes together (hopping + $V_1$ + $V_2$ + a symmetry-breaking test potential). Elementwise agreement: $1.1\times10^{-16}$.

**C1 — reflection-parity block-diagonalisation.** OBC already breaks translation invariance; the one discrete symmetry left is the reflection $i\to L-1-i$, which every one of hopping/$V_1$/$V_2$ respects. The parity-adapted change of basis is built explicitly (symmetric/antisymmetric combinations of a state and its mirror image) and verified, for every regime and every $L\in\{10,12,14\}$, to (a) be orthonormal and (b) genuinely block-diagonalise $H$ — worst off-block element $2.5\times10^{-16}$. This mattered in practice: an earlier version of this module built the parity transform with interleaved even/odd columns rather than grouped ones, which silently produces a *bogus* block split (off-block element $\mathcal O(1)$, not small) even though the transform itself is still orthonormal — a defect that would have contaminated every downstream level-statistics number without C1 as a standing construction check. Fixed before any of the numbers below were taken as final; C1 is now a permanent gate-tier check specifically because this failure mode is silent otherwise.

---

## 4. Diagnostic 1 — the level-spacing ratio $\langle r\rangle$

The mean ratio of consecutive level spacings, $r_n=\min(s_n,s_{n-1})/\max(s_n,s_{n-1})$ (Oganesyan & Huse, Phys. Rev. B **75**, 155111 (2007)), computed within the reflection-even sector (trimming 5% at each spectral edge), distinguishes integrable (Poisson) from quantum-chaotic (GOE) spectra without unfolding. The two reference constants, $\langle r\rangle_\text{Poisson}=0.3863$ and $\langle r\rangle_\text{GOE}=0.5307$, are quoted directly from the literature (Atas, Bogomolny, Giraud & Roux, Phys. Rev. Lett. **110**, 084101 (2013), who derived the full ratio distribution and its mean for both ensembles; the same two numbers are the standard reference pair throughout the ETH/MBL literature, e.g. the review lecture notes at arXiv:1904.00091 sec. III).

| $L$ | dim | `integrable_V1` $\langle r\rangle$ | `generic_V1V2` $\langle r\rangle$ |
|---|---|---|---|
| 10 | 252 | $0.4168\pm0.0258$ | $0.4725\pm0.0254$ |
| 12 | 924 | $0.3875\pm0.0133$ | $0.5141\pm0.0123$ |
| 14 | 3432 | $0.3797\pm0.0072$ | $0.5224\pm0.0066$ |

At $L=14$: `integrable_V1` sits $0.9\sigma$ from Poisson (0.3863) and `generic_V1V2` sits $20.6\sigma$ **above** Poisson and only $1.3\sigma$ below GOE (0.5307). The finite-size flow is monotone and in the expected direction for **both** regimes: `integrable_V1`'s $\langle r\rangle$ falls toward 0.3863 as $L$ grows ($0.4168\to0.3875\to0.3797$) while `generic_V1V2`'s rises toward 0.5307 ($0.4725\to0.5141\to0.5224$) — the two regimes visibly separate as the system grows, which a finite-size coincidence would not do.

**The `free` regime is reported for context and is flagged, not used as evidence** (sec 7.1): its own $\langle r\rangle$ does not track Poisson cleanly across $L$ (0.5706, 0.4382, 0.6133 at $L=10,12,14$) — the free point carries an extra chiral/particle-hole symmetry beyond the reflection this finding resolves, giving extra exact degeneracies that bias the ratio statistic. This is a known property of the exactly free point and does not touch the `integrable_V1`-vs-`generic_V1V2` comparison, which is the finding's actual claim.

---

## 5. Diagnostic 2 — the entanglement-entropy plateau of a domain-wall quench

Initial state: a domain wall (leftmost $N$ sites filled, rightmost $N$ empty). Evolution is **exact** — the full many-body spectrum and eigenvectors are computed once (no Trotterisation, no truncation) and $|\psi(t)\rangle=\sum_n e^{-iE_nt}\langle n|\psi_0\rangle|n\rangle$ is evaluated directly. The half-chain ($L_A=L/2$) entanglement entropy $S_A(t)$ is computed by direct SVD of the bipartite amplitude tensor (exact; the fixed site-ordered occupation basis needs no extra fermionic sign across a contiguous cut, since all of $A$'s creation operators already precede all of $B$'s in the canonical ordering). The long-time plateau (mean of the second half of 30 sampled times out to $t=40/t$) is reported as a fraction of the absolute volume-law ceiling $L_A\ln2$:

| $L$ | `free` frac. | `integrable_V1` frac. | `generic_V1V2` frac. | gap (generic $-$ integrable) |
|---|---|---|---|---|
| 10 | 0.5831 | 0.7302 | 0.7375 | 0.0073 |
| 12 | 0.6073 | 0.6932 | 0.7617 | 0.0685 |
| 14 | 0.5221 | 0.6487 | 0.7456 | 0.0969 |

`generic_V1V2`'s fraction is essentially $L$-independent ($0.738\to0.762\to0.746$), consistent with a genuine, size-extensive entanglement density — the expected signature of real (ETH) thermalisation. `integrable_V1`'s fraction **falls** as $L$ grows ($0.730\to0.693\to0.649$), and the gap between the two regimes **widens**, not closes, from $L=10$ to $L=14$. This is the qualitative signature a surviving GGE-style constraint predicts: the extra conserved (quasi-local) charges of the Jordan-Wigner-integrable point suppress the entanglement density below the genuinely thermalising value, and — because the constraint is extensive — the suppression does not wash out as the system grows.

(An attempt was made to also compare against a plain energy-only canonical/Gibbs prediction for $S_A$, built as a Boltzmann-weighted average of individual eigenstates' entanglement entropies. That comparison is **not reported as a result**: by concavity of the von Neumann entropy, $\sum_n p_n S(\rho_A^{(n)}) \le S(\sum_n p_n \rho_A^{(n)})$, so an eigenstate-averaged quantity of this kind necessarily under-estimates the true entropy of the physically correct dephased/mixed ensemble for *any* system, integrable or not — the naive canonical comparison came out lower than the measured plateau in **every** regime including `generic_V1V2`, which is the concavity gap, not evidence about thermalisation. The correct thermal reference for the Jordan-Wigner-integrable regime is in any case the full GGE built from the entire tower of quasi-local charges, not a plain energy-only canonical ensemble; that GGE is not constructed here. This is recorded so a later session does not re-introduce the same mis-comparison.)

---

## 6. Diagnostic 3 — eigenstate-to-eigenstate fluctuation (the ETH signature)

For each regime and $L$, the 60 eigenstates nearest in energy to the domain-wall quench's mean energy $E_0=\langle\psi_0|H|\psi_0\rangle$ are selected, and the standard deviation of the half-chain entanglement entropy across a 30-state subset of that window is measured (D'Alessio, Kafri, Polkovnikov & Rigol, *From quantum chaos and eigenstate thermalization to statistical mechanics and thermodynamics*, Adv. Phys. **65**, 239 (2016)). ETH predicts this eigenstate-to-eigenstate spread **shrinks** with system size (nearby-energy eigenstates converge to the same, smooth function of energy); a non-ergodic system shows no such shrinkage.

| $L$ | `integrable_V1` std | `generic_V1V2` std |
|---|---|---|
| 10 | 0.2998 | 0.2835 |
| 12 | 0.2875 | 0.1624 |
| 14 | 0.3175 | 0.1478 |

`generic_V1V2`'s spread falls by nearly half from $L=10$ to $L=14$ (0.284 → 0.148); `integrable_V1`'s does not shrink at all (0.300 → 0.318, if anything mildly rising). This is the sharpest of the three diagnostics and the cleanest confirmation that `generic_V1V2` alone is developing the ETH signature.

**A secondary, more local observable behaves differently, and this is itself informative rather than a contradiction.** The same window's fluctuation in the *local* centre-site density $n_{L/2}$ shrinks with $L$ for **both** interacting regimes (`integrable_V1`: 0.0565→0.0477→0.0420; `generic_V1V2`: 0.0442→0.0345→0.0205) — reported in the results JSON but not used as a gate check. This matches the established distinction in the GGE literature (e.g. Vidmar & Rigol's GGE review): a GGE correctly reproduces the expectation values of *simple local* observables even though it is not a Gibbs state, while the *entanglement entropy* — a genuinely global, extensive quantity — is exactly where GGE and Gibbs predictions are known to diverge. Seeing that divergence show up in $S_A$ but not (as clearly) in $n_{L/2}$ is consistent with, not contrary to, that literature.

---

## 7. Checks

| # | Check | Result | Class |
|---|---|---|---|
| C0 | free many-body GS == sum of $N$ lowest single-particle OBC levels (validates the fermionic sign convention) | $7.1\times10^{-15}$ | exact |
| C1 | reflection-parity transform block-diagonalises $H$ for every regime and $L\in\{10,12,14\}$ | $2.5\times10^{-16}$ | machine |
| C2 | `integrable_V1` $\langle r\rangle$ consistent with Poisson (0.3863) at $L=14$ | $0.3797\pm0.0072$ ($0.9\sigma$) | quantitative |
| C3 | `generic_V1V2` $\langle r\rangle$ separated from Poisson by $>10\sigma$ and closer to GOE than Poisson at $L=14$ | $20.6\sigma$; $0.5224$ vs GOE $0.5307$ | quantitative |
| C4 | finite-size flow: `generic_V1V2` $\langle r\rangle$ rises toward GOE, `integrable_V1` $\langle r\rangle$ falls toward Poisson, $L=10\to14$ | monotone both ways | quantitative |
| C5 | entanglement-plateau ceiling-fraction: `generic_V1V2` $>$ `integrable_V1` at every $L$, gap non-closing | $0.0073\to0.0969$ | quantitative |
| C6 | ETH signature: eigenstate-to-eigenstate $S_A$ fluctuation shrinks with $L$ for `generic_V1V2`, does not for `integrable_V1` | $0.2835\to0.1478$ vs $0.2998\to0.3175$ | quantitative |

**7/7 PASS.** Declared control, verified red: forcing $V_2\to0$ inside the `generic_V1V2` regime (i.e. making it identical to `integrable_V1`) turns **C3, C4, C5, C6** red — the regime-separation checks — while leaving **C0–C2** untouched, exactly as it should (`check_f375(v2_control=True)`: 3/7 pass).

---

## 8. Scope limits, and what is *not* claimed

1. **This is not F110's link Hamiltonian coupled to matter.** That coupling (real gauge degrees of freedom driving dynamical fermions) is F300/F309's literal named next step and remains fully open; see sec1 and sec9.
2. **$t$, $V_1$, $V_2$ are toy couplings on a 1D single-band reduction**, not values derived from the BCC dispersion's own expansion coefficients (F300 sec2.1, F309 sec2). No claim is made that any specific interaction strength the model's own gauge sector would generate corresponds to $V_1=V_2=0.5$.
3. **Finite $L\in\{10,12,14\}$.** The level-statistics and ETH-fluctuation trends are measured to move in the expected direction across three sizes; this is evidence of a trend, not a thermodynamic-limit proof.
4. **The `free` regime's own $\langle r\rangle$ is not a clean Poisson signal** (sec4) — flagged as a known feature of the exactly free point (extra chiral/particle-hole degeneracy beyond the resolved reflection symmetry), not hidden, and not load-bearing for the finding's actual (integrable-vs-generic) comparison.
5. **The naive canonical/Gibbs comparison for $S_A$ was attempted and explicitly discarded** (sec5) as a concavity artefact rather than a thermalisation diagnostic — recorded so it is not silently redone.
6. **No claim of exactness for $V_1,V_2$ integrability/non-integrability beyond level statistics and quench dynamics.** The $t$–$V$ model's Bethe-ansatz integrability for all $V_1$ is standard (Jordan–Wigner duality to XXZ); this finding does not re-derive that duality, only uses its consequence (Poisson statistics) as the null hypothesis `integrable_V1` is checked against.

**Falsifier.** A re-run at larger $L$ (16–20, feasible with a sparse/Lanczos rebuild of this same module rather than the dense `numpy.linalg.eigh` used here — sec9) that shows `integrable_V1`'s $\langle r\rangle$ *not* continuing to converge toward 0.3863, or `generic_V1V2`'s ETH fluctuation *not* continuing to shrink, would directly contradict this finding's central claim (that the two-tier structure — interaction alone insufficient, integrability-breaking interaction sufficient — is real and not a finite-size coincidence at $L\le14$).

---

## 9. Next steps, in order of value

1. **Extend to $L=16$–$20$** using a sparse Hamiltonian + Lanczos/shift-invert eigensolver (this module currently uses dense `numpy.linalg.eigh`, which was fast enough at $L\le14$ but does not scale further on the available hardware) to firm up the finite-size trend beyond three points.
2. **F110's actual named next step**: couple dynamical fermionic matter to the real-time link Hamiltonian (F110 sec5's own "next leg of the P2 chain") — the gauge-sector interacting theory this finding explicitly does not attempt, still open.
3. **Construct the full quasi-local-charge GGE** for the `integrable_V1` (XXZ) point, so the entanglement-entropy comparison in sec5 can be made against the *correct* thermal reference (the GGE, not a naive canonical ensemble) rather than only the qualitative ceiling-fraction argument used here.
4. **Thread the model's own BCC dispersion coefficients** (F300 sec2.1 / F309 sec2's closed-form $A(\hat n)$, $b(\hat n)$) into $V_1,V_2$ in place of the toy values 0.5/0.5, if a natural lattice-native interaction channel is identified.
