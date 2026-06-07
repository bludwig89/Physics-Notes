# F102 — Coupling several rotors: the Gaussian↔confinement crossover survives, plaquettes decouple at strong coupling, and coupling organises the crossover into a transition

**Date:** 2026-06-05 - 16:10
**Status:** Confirmed — 5/5 checks PASS. Exact diagonalisation of $\mathbb{Z}_3$ gauge theory (coupled rotors) on strips of $P=1,2,3$ plaquettes; M1 Lanczos validated vs dense ($2.7\times10^{-14}$) + Gauss-law trivial sector ($\langle A_s\rangle=1$); M2–M5 the crossover, decoupling, factorisation, log law, and transition precursor. **Answers the open question of F101 §7.**
**Script:** `model-tests/test_F102_coupled_rotors.py` (~29 s)
**Results:** `test-results/F102_coupled_rotors.json`
**Cross-references:** [[F101-strong-coupling-sigma-compact-rotor]] (the single rotor this couples; §7 open question), [[F100-gamma-from-transfer-operator]] / [[F99-sigma-as-centre-lagrange-multiplier]] (the $\mathbb{Z}_3$ centre theory), [[F70-gradient-flow-confinement-string-tension]] (the 2D independent-plaquette area law recovered at strong coupling), [[F94-lattice-gauge-mc-confinement-vs-F86]] (the full multi-mode SU(3) route this complements).

---

## 1. The question (F101 §7)

F101 solved a **single** compact rotor (one plaquette) exactly and found the Gaussian (weak) ↔ logarithmic-confinement (strong) crossover. But a single plaquette has no neighbours; in 2+1D plaquettes **share links** and are genuinely coupled. F101 §7 flagged the honest open question: *does the crossover survive the coupling?* This finding answers it by exactly diagonalising the genuinely-coupled theory.

## 2. The coupled theory — $\mathbb{Z}_3$ gauge theory by exact diagonalisation

The physical centre is $\mathbb{Z}_3$, so "coupling several rotors" is precisely $\mathbb{Z}_3$ lattice gauge theory in 2+1D (Hamiltonian form), on an open strip of $P$ plaquettes:

$$H=-\Gamma\sum_{\text{links}}\big(X_l+X_l^\dagger\big)-\lambda\sum_{\text{plaq}}\big(B_p+B_p^\dagger\big),\qquad B_p=\!\!\prod_{l\in p}Z_l^{\pm1},$$

with $X$ the clock shift, $Z$ the clock, $\mathbb{Z}_3$ operators **exact** (no truncation artifacts). Strong coupling $=$ small $\lambda$ (electric term dominates → confined); weak $=$ large $\lambda$ (magnetic → deconfined). The confinement order parameter is $\langle B_p\rangle$ — exactly F101's $s_1$, now in the **coupled** theory. Solved by matvec Lanczos with full reorthogonalisation (validated against dense ED to $3\times10^{-14}$, ground state confirmed in the trivial Gauss sector $\langle A_s\rangle=1$). Adjacent plaquettes share a link ($p_0$ carries $v_1^{+1}$, $p_1$ carries $v_1^{-1}$) — a genuine coupling.

## 3. What survives, and what coupling adds

**M2 — the crossover survives.** $\langle B_p\rangle(\lambda)$ runs the full $0\to1$ for $P=1,2,3$. At **strong coupling the curves are identical across $P$** (spread $2\times10^{-6}$): coupled plaquettes **decouple** when the electric term dominates, so the single-rotor result is exact there. The strong-coupling log law persists, $\langle B_p\rangle\propto\lambda$ (ratio $\langle B_p\rangle(0.3)/\langle B_p\rangle(0.1)=3.07\approx3$), i.e. $\sigma=-\ln\langle B_p\rangle\sim-\ln\lambda$.

**M3 — area-law factorisation (F70 recovered).** The $P$-plaquette Wilson loop factorises, $\langle W_P\rangle=C_P\,\langle B_p\rangle^{P}$, with $C_P=O(1)$ at strong coupling ($C_2=1.17$, $C_3=1.38$ — the finite shared-link prefactor) and $C_P\to1$ toward deconfinement ($1.005,1.008$). So F70's independent-plaquette product structure is the strong-coupling limit of the coupled theory; the coupling enters only as an $O(1)$ prefactor on the otherwise-intact area law.

**M4 — confinement survives.** $\sigma=-\ln\langle B_p\rangle$ stays positive with the universal strong-coupling log slope $d\sigma/d\ln\lambda=-1.02,-1.02,-1.03$ for $P=1,2,3$ — the same $-\ln(\text{coupling})$ law of F101/F70, unaffected by coupling.

**M5 — coupling organises the crossover into a transition.** The new effect of coupling: weak-coupling order **increases with $P$** ($\langle B_p\rangle(\lambda{=}10)=0.938,0.959,0.975$ for $P=1,2,3$). More coupled rotors order more strongly — the finite-size precursor of the genuine deconfinement transition. Coupling does not wash the crossover out; it sharpens it.

## 4. Verdict

The crossover survives coupling. Concretely: at strong coupling the coupled plaquettes **decouple**, so F101's single-rotor result and F70's area law are exact; the $\sigma\sim-\ln(\text{coupling})$ confinement law holds for every $P$; and the only thing coupling adds is (i) a finite $O(1)$ Wilson-loop prefactor and (ii) a $P$-growing ordering at weak coupling that is the precursor of the deconfinement transition. The single-rotor picture (F101) is the strong-coupling limit of the true coupled theory — confirmed non-perturbatively by exact diagonalisation.

## 5. Check summary (5/5)

| Check | Statement | Residual |
|---|---|---|
| M1 | Lanczos = dense ED; trivial Gauss sector $\langle A_s\rangle=1$ | $2.7\times10^{-14}$; $1.000000$ |
| M2 | crossover survives $P{=}1,2,3$; decouple at strong coupling; $\langle B_p\rangle\propto\lambda$ | spread $2.3\times10^{-6}$; ratio $3.07$ |
| M3 | $\langle W_P\rangle=C_P\langle B_p\rangle^P$, $C_P{=}O(1)$ strong $\to1$ weak (F70) | $C_3$: $1.38\to1.008$ |
| M4 | $\sigma=-\ln\langle B_p\rangle$ log slope $-1$ all $P$ | $-1.02,-1.02,-1.03$ |
| M5 | weak-coupling order increases with $P$ (transition precursor) | $0.938,0.959,0.975$ |

## 6. Honest scope

- **Small lattices, open strips ($P\le3$).** Exact-ED reach; the qualitative crossover, decoupling, factorisation and ordering trend are robust, but the sharp deconfinement transition and continuum $\sigma$ need larger lattices (Lanczos scales, or F94's gauge-MC for full SU(3) 3+1D).
- **$\mathbb{Z}_3$ centre, 2+1D.** The coupled theory is the $\mathbb{Z}_3$ centre gauge theory (the physically relevant one for confinement, F99); the full non-Abelian SU(3) and 3+1D dynamics remain F94's domain. The A-vs-C $k$-dependence caveat (F98–F101) is unchanged.
- **Strong-coupling prefactor $C_P$.** The shared-link correction to the pure area law is computed here ($C_2=1.17$, $C_3=1.38$) but not given a closed form.

## 7. Provenance

- New content: the coupled $\mathbb{Z}_3$ gauge ED (matvec Lanczos, §2); the survival/decoupling/factorisation/log-law/transition-precursor results (§3–4).
- Reused: F101 single rotor and $\sigma=-\ln s_1$; F70 area-law product; F99 $\mathbb{Z}_3$ centre.
- Verification: `model-tests/test_F102_coupled_rotors.py` (2026-06-05, 5/5 PASS), results `test-results/F102_coupled_rotors.json`.
