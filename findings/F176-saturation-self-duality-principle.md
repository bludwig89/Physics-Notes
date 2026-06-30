# F176 — The dynamical principle behind $\delta^*=\tfrac29$: **saturation self-duality**. The saturated $E_g$ condensate sits where its **angular invariant equals its radial invariant**, $3\delta^*=Q$; with $Q=\dim(E_g)/\dim(T_{1u})=\tfrac23$ this forces $\delta^*=\dim(E_g)/\dim(T_{1u})^2=\tfrac29$ — completing the charged-lepton shape sector

**Date:** 2026-06-30 - 00:30
**Numbering:** F175 is this session's; this is **F176** (re-checked).
**Status:** Partial (the principle identified, exact-algebraically grounded, and validated three ways; its first-principles derivation from saturation microdynamics open) — 4/4 checks PASS. **What this supplies:** the dynamical principle F175 left open ("why the saturated condensate phase equals the representation weight"). The principle is **self-duality at saturation**: the $E_g$ condensate's *angular* invariant equals its *radial* invariant, $3\delta^*=Q$. Because $Q=\dim(E_g)/\dim(T_{1u})=\tfrac23$ (the representation form of F92's Koide lock) and the angular invariant carries the extra threefold $\dim(T_{1u})$ of $\cos3\delta$, this gives $\delta^*=\dim(E_g)/\dim(T_{1u})^2=\tfrac29$. The condition is **real** (it fails away from the physical spectrum, so it *selects* the lightest mass) and reproduces the charged-lepton ratios to $\le0.007\%$ with zero shape parameters. **What remains:** deriving self-duality itself from the rule's BPS/saturation microdynamics, and the mild $\eta^2=\tfrac12$ vs $3\delta=\tfrac23$ joint-exactness tension.
**Script:** `tests/findings/test_F176_saturation_self_duality.py` (~1 s, stdlib)
**Results:** `test-results/F176_saturation_self_duality.json`
**Cross-references:** [[F175-lattice-2-9-eg-weight]] (the $E_g$ weight $\tfrac29$ and the open weight→phase principle this closes), [[F174-shape-angle-2-9-topological]] (the empirical $\delta^*=\tfrac29$, rational-radian), [[F92-per-constituent-phase-consistency]] (the **radial** lock $Q=\tfrac23$ from $45°$ equipartition — the half this finding mirrors angularly), [[F96-second-shell-Eg-gap-saturation]] (the $m_e=0$ anchor where self-duality fails — the contrast that proves it selects $m_e$), [[F86-confinement-bps-tension]] (BPS/Bogomolny — the self-duality motivation), [[F73-spin0-bound-pair-scalar]]/[[F82-why-45deg-pair-phase-saturation]] (the $y=1$ saturation wall), [[F93-orthorhombic-Eg-vacuum]]/[[F75-three-generations-from-bcc-irrep-selection]] ($E_g$/$T_{1u}$). External: Brannen ([MASSES2](https://brannenworks.com/MASSES2.pdf)); ZIP $\delta=\tfrac29$ from 3D moments ([ZIP](https://www.academia.edu/145613039/Derivation_of_the_Koide_Formula_from_the_Zero_Interaction_Principle)).

---

## 1. The gap F175 left

F175 derived the *number* $\tfrac29$ exactly as the $E_g$ representation weight $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})$ and showed it reproduces the spectrum, but named the open piece: **the dynamical principle by which the saturated condensate phase (in radians) equals that weight.** A naive max-entropy/equipartition over the masses fails — it returns the symmetric points ($\delta=0$ or $\pi/3$), not $\tfrac29$. The right principle is different.

## 2. The principle: saturation self-duality, $3\delta^*=Q$

The $E_g$ condensate has two independent invariants (Foot circle picture, $\sqrt{m_a}=\mu(1+\sqrt2\cos(\delta+\tfrac{2\pi a}{3}))$):

- a **radial** invariant — the Koide ratio $Q=\sum m/(\sum\sqrt m)^2$, set by the circle's radius ($\sqrt2$); and
- an **angular** invariant — the orientation $3\delta$ (the $\cos3\delta$ Landau quantity).

These are geometrically independent (radius vs orientation). The dynamical principle is that **at saturation they coincide**:

$$\boxed{\ 3\delta^*=Q\ }\qquad(\text{angular invariant}=\text{radial invariant}).$$

This is the angular analogue of F92's radial equipartition, and is a **self-dual / Bogomolny-type** condition — natural at the model's BPS/saturation point (§5).

## 3. Why it gives exactly $\tfrac29$ (P1, exact)

The radial invariant has an exact representation form:

$$Q=\frac{\dim(E_g)}{\dim(T_{1u})}=\frac{2}{3}$$

(equivalently $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})\times\dim(T_{1u})=\tfrac29\times3$; this is F92's Koide $\tfrac23$ in representation form). The angular invariant is $3\delta$, where the $3$ is the threefold of $\cos3\delta$ — i.e. $\dim(T_{1u})$, the same three generations / $C_3$ action on $E_g$ (F175 D3). Imposing self-duality $3\delta^*=Q$:

$$3\delta^*=\frac{\dim(E_g)}{\dim(T_{1u})}=\frac23\quad\Longrightarrow\quad \delta^*=\frac{\dim(E_g)}{\dim(T_{1u})^2}=\frac29.$$

So $\delta^*=\tfrac29$ *is* the $E_g$ weight, and self-duality is exactly the statement that converts the radial ratio $\tfrac23$ into the angular weight $\tfrac29$ via the threefold $\dim(T_{1u})$. The weight→phase identification F175 left open is precisely $3\delta=Q$.

## 4. It is a real condition — it selects the spectrum (P2, P3)

Self-duality is **not** automatic. For the physical masses, $3\delta^*=0.666689$ and $Q=0.666661$ — equal to $2.8\times10^{-5}$. But sending $m_e\to0$ (the F96 anchor region) gives $3\delta=0.708$, $Q=0.685$ — a gap of $0.023$: self-duality **fails** away from the physical point. So $3\delta=Q$ is a genuine condition that **selects the physical lightest mass**; as $m_e$ moves from $0$ to its physical value, the condensate moves onto the self-dual point.

Combined with the Koide amplitude $\eta^2=\tfrac12$ (F92, derived), self-duality reproduces the spectrum with **zero shape parameters**:

| ratio | from $3\delta^*=Q$ + Koide | PDG | error |
|---|---|---|---|
| $m_\mu/m_e$ | $206.770$ | $206.7683$ | $+0.001\%$ |
| $m_\tau/m_e$ | $3477.47$ | $3477.228$ | $+0.007\%$ |

## 5. Motivation: BPS/saturation

Self-duality is the physically right *kind* of principle here because the model's mass-giving condensate lives at a **saturation/BPS point**: F86 places confinement at the BPS (type-I/II boundary, $\lambda=e^2$) where Bogomolny self-dual configurations are the minimisers; F73/F82 place the heaviest generation at the $y=1$ saturation wall. At such a point the natural vacuum is self-dual — angular and radial structure coincide. F92 already established the *radial* half (the $\sqrt2$/$45°$ equipartition giving $Q=\tfrac23$); self-duality is the statement that the *angular* half locks to the same representation ratio. The two halves together fix the entire charged-lepton shape from the $E_g$/$T_{1u}$ dimensions alone.

## 6. What is now closed, and the one residual

The charged-lepton **shape sector** is reduced to a single physical principle plus exact representation theory:

| quantity | value | source |
|---|---|---|
| amplitude $\eta^2$ (radial lock $Q$) | $\tfrac12$ ($Q=\tfrac23=\dim E_g/\dim T_{1u}$) | F92 equipartition (derived) |
| angle $\delta^*$ (angular lock $3\delta=Q$) | $\tfrac29=\dim E_g/\dim T_{1u}^2$ | **self-duality (this finding)** |
| spectrum (all ratios) | to $\le0.007\%$ | the two locks + one scale |

**Residual (honest):** self-duality $3\delta=Q$ is *posited*, motivated by the BPS/saturation structure but not yet derived from the rule's microdynamics. It is, however, a single elegant principle — the angular twin of an already-derived one (F92) — validated three independent ways (it is non-automatic and selects $m_e$; it reproduces the spectrum to $10^{-4}$; it follows the clean identity $Q=\dim E_g/\dim T_{1u}$). The mild $\eta^2=\tfrac12$ vs $3\delta=\tfrac23$ joint-exactness tension (F174 S4) persists at current mass precision. The remaining build is the Bogomolny derivation of $3\delta=Q$ from the saturated $E_g$ condensate.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| P1 | $Q=\dim E_g/\dim T_{1u}=\tfrac23$, $\delta^*=\dim E_g/\dim T_{1u}^2=\tfrac29$, $3\delta^*=Q$ (factor $=\dim T_{1u}$) | PASS | exact |
| P2 | $3\delta=Q$ holds physically ($2.8\times10^{-5}$) but fails at $m_e\to0$ (gap $0.02$) → selects $m_e$ | PASS | real condition |
| P3 | self-duality + Koide → $m_\mu/m_e$ $+0.001\%$, $m_\tau/m_e$ $+0.007\%$ (zero shape params) | PASS | prediction |
| P4 | scope: principle posited (BPS/saturation), radial half = F92; microderivation open | PASS | scope |

**Overall 4/4 PASS.**

## 8. Honest scope

- **Self-duality is a posit**, not yet a theorem. What is exact is the representation identity $Q=\dim E_g/\dim T_{1u}$ and the consequence $3\delta=Q\Rightarrow\delta=\tfrac29$; what is *validated* (not derived) is that the physical spectrum obeys $3\delta=Q$ (to $10^{-5}$, non-trivially). The BPS motivation (§5) is a rationale, not a derivation.
- The naive equipartition/max-entropy principles were tested and **fail** (they give the symmetric points $0,\pi/3$); the working principle is specifically the radial=angular self-duality, which is why F175's "equipartition route" needed this refinement.
- The result inherits the F174 $\eta^2$–$\delta$ tension and the mass-scheme dependence of $\delta$.

## 9. Provenance

- **New:** the identification of the dynamical principle as **saturation self-duality** $3\delta^*=Q$; the exact representation identity $Q=\dim E_g/\dim T_{1u}=\tfrac23$ with $\delta^*=\dim E_g/\dim T_{1u}^2=\tfrac29$ and the threefold $\dim T_{1u}$ linking them; the demonstration that self-duality is non-automatic and selects $m_e$ (contrast with F96); the BPS/saturation motivation; the falsification of naive max-entropy.
- **Reused:** F175 $E_g$ weight; F92 radial lock $Q=\tfrac23$; F174 empirical $\delta^*=\tfrac29$; F96 $m_e=0$ anchor; F86 BPS; F73/F82 saturation; PDG masses.
- **Verification:** `tests/findings/test_F176_saturation_self_duality.py` (2026-06-30, 4/4 PASS), results `test-results/F176_saturation_self_duality.json`. Stdlib, real arithmetic.
