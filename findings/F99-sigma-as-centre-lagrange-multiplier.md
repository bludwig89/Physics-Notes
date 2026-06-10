# F99 — The string tension σ derived from the QCA rule as the centre-twist Lagrange multiplier of $\mathbb{Z}_N$ non-closure

**Date:** 2026-06-05 - 14:40
**Status:** Confirmed — 5/5 checks PASS. D1/D2/D4 algebraically exact (sympy, symbolic $\mathbb{Z}_N$ weights), D3 machine precision (real SU(3) links), D5 reconciliation (F70 numeric to its published table; F86 small-σ algebraic). **Closes the bridge** flagged open in F97 §8 and F98 §4.
**Script:** `tests/findings/test_F99_sigma_from_qca_rule.py` (<0.5 s)
**Results:** `test-results/F99_sigma_from_qca_rule.json`
**Cross-references:** [[F98-enforcer-is-binder]] (the price *structure* this now derives), [[F97-baryon-phase-closure-no-go]] (§8 open bridge), [[F70-gradient-flow-confinement-string-tension]] (2D-exact area law $\sigma=-\ln w$, the SU(3) anchor reconciled here), [[F86-colour-dielectric-dual-superconductor]] ($\sigma=2\pi v^2 n$, the small-σ limit), [[F94-lattice-gauge-mc-confinement-vs-F86]] (real SU(3) links used for the centre-covariance test), [[F43-dynamical-gluons]] (the gluon rotation update rule).

---

## 1. What was open, and what this closes

F98 established the *price structure* of confinement — $\sigma=0$ when the centre-phase budget closes (N-ality 0), $\sigma R\to\infty$ when it does not — but **took $\sigma$ as an input** from F86 ($2\pi v^2 n$) and F94 (gauge-MC). F98 §4 named the gap explicitly: *“the Lagrange statement is structural … not yet a derivation of $\sigma$ as the multiplier inside the QCA update rule.”* F97 §8 had named the same target. This finding **derives** $\sigma$ from the rule's own centre statistics, and shows it *is* the Lagrange multiplier conjugate to the centre-closure constraint.

## 2. The derivation in four moves

**Move 1 — the rule is centre-covariant (D3, on the real SU(3) links).** A $\mathbb{Z}_N$ centre transform $U\to zU$ ($z=e^{2\pi i/N}$) applied to all temporal links of one time-slice sends every Polyakov loop $P\to zP$ while leaving every contractible Wilson loop invariant (verified to $5\times10^{-16}$ / $0.0$ on `lgt_fork_A_mc`). So the rule's observables organise by **centre charge (N-ality)** — the budget whose closure F97/F98 identified with stability. The centre symmetry is exact in the update rule, not imposed.

**Move 2 — track the centre content; the 2D area law gives $\sigma_k=-\ln s_k$ (D1, exact).** Project the plaquette holonomy the rule produces onto its centre sector: a class weight $p(n)$, $n\in\mathbb{Z}_N$. In the 2D testbed (F70: axial gauge ⇒ independent plaquettes) a Wilson loop of centre charge $k$ over area $A$ obeys **exactly**

$$\langle W_k\rangle=s_k^{\,A},\qquad s_k=\frac{z(2\pi k/N)}{z(0)},\qquad z(\theta)=\sum_{n\in\mathbb{Z}_N}p(n)\,e^{in\theta},$$

so $\boxed{\sigma_k=-\ln s_k}$. This is the $\mathbb{Z}_N$ analogue of F70's SU(3) $\sigma=-\ln w$. Proven (symbolic $p_0,p_1,p_2$): $s_0=1$ identically ⇒ $\sigma_0=0$; $s_{k+N}=s_k$ (centre-periodic); $s_k=s_{N-k}$ for a centre-symmetric weight ($k\leftrightarrow N-k$ string degeneracy); $0<s_k<1$ off closure ⇒ $\sigma_k>0$. **This re-derives F98's E3/E5 from the rule instead of assuming them.**

**Move 3 — $\sigma$ *is* the Lagrange multiplier (D2, exact).** A source of N-ality $k$ is equivalent to a ’t Hooft centre **twist** $\theta_k=2\pi k/N$. The constrained free-energy density is $\sigma_k=f(\theta_k)$, $f(\theta)=-\ln[z(\theta)/z(0)]$. The twist angle is the multiplier conjugate to the centre-closure constraint: stationarity of the Lagrangian $\mathcal L(\theta)=\ln z(\theta)-i\theta c$ gives

$$\frac{\partial\mathcal L}{\partial\theta}=0\iff c=-\,i\,\frac{z'(\theta)}{z(\theta)}=\langle n\rangle_\theta,$$

i.e. the multiplier $\theta$ is exactly what fixes the centre charge to $c$ — and at a centre value $c=k$, $\theta_k=2\pi k/N$ and the price is $f(\theta_k)=-\ln s_k=\sigma_k$, with $f(\theta_0)=0$ (no price on closure). So $\sigma$ is not merely *like* a multiplier — it is the value of the constrained free energy whose multiplier is the centre twist. **This is the F97 §8 / F98 §4 statement, now an identity.**

**Move 4 — $p(n)$ comes from the rule's disorder (D4, exact).** The centre projection of a heat-kernel / Wilson plaquette weight is the $\mathbb{Z}_N$ clock weight $p(n)\propto e^{\gamma\cos(2\pi n/N)}$, with $\gamma$ set by the rotation-rule disorder (the accumulated holonomy / rotation angle $\Omega$). Limits, both exact: ordered rule $\gamma\to\infty$ ⇒ $s_1\to1$, $\sigma_1\to0$ (deconfined); maximally disordered $\gamma\to0$ ⇒ $p$ uniform, $z(2\pi/N)=0$, $s_1\to0$, $\sigma_1\to\infty$. $\sigma_1(\gamma)$ is monotone decreasing in order. Confinement is the disordered phase of the rule's centre variable — consistent with F70 CF7 (cooling dissolves $\sigma$).

## 3. Reconciliation (D5)

- **F70.** $\sigma_k=-\ln s_k$ is the same law as F70's $\sigma(\beta)=-\ln w(\beta)$ — tension $=-\ln$ of a normalised plaquette weight. F70's SU(3) values are reproduced from `ca_confinement` and are positive, monotone-decreasing in $\beta$, $\to0$ as $\beta\to\infty$: $\sigma(0.5{,}1{,}2{,}4{,}8{,}20)=3.543,2.811,2.051,1.274,0.624,0.219$ — matching the F70 table. F70 is the full fundamental (N-ality 1); $-\ln s_1$ is its centre projection; they share the leading strong-coupling behaviour.
- **F86.** In the small-$\sigma$ / Abelian-BPS limit $s_k=1-\varepsilon_k$, $\sigma_k=-\ln(1-\varepsilon_k)\simeq\varepsilon_k$; when only the unit centre charge is excited $\varepsilon_k\propto k$, so $\sigma_k=k\,\sigma_1$. Identifying $2\pi v^2:=\sigma_1$ gives $\sigma_k=2\pi v^2 k$ — exactly F86's $\sigma=2\pi v^2 n$, with $\sigma_0=0$.

## 4. Check summary (5/5)

| Check | Statement | Tier | Residual |
|---|---|---|---|
| D1 | centre projection $\sigma_k=-\ln s_k$, $s_k=z(2\pi k/N)/z(0)$; $s_0=1$ ($\sigma_0=0$) exact, periodic mod $N$, $k\leftrightarrow N-k$ degenerate, $0<s_k<1$ off closure | 1 (sympy) | 0 |
| D2 | Lagrange/twist: $\theta_k=2\pi k/N$ is the multiplier conjugate to centre charge (stationarity $c=-i\,z'/z$); $\sigma_k=f(\theta_k)=-\ln s_k$; $f(\theta_0)=0$ | 1 (sympy) | 0 |
| D3 | real SU(3) rule centre-covariant: slice twist $zI$ ⇒ Polyakov $\to z$·Polyakov, contractible Wilson loops invariant | 2 | poly $5.0\times10^{-16}$, wilson $0.0$ |
| D4 | rule→weight $p(n)\propto e^{\gamma\cos(2\pi n/N)}$; $\sigma_1(\gamma\to\infty)=0$, $\sigma_1(\gamma\to0)=\infty$, monotone | 1 (sympy) | 0 |
| D5 | reconciliation: F70 $-\ln w(\beta)$ same law (table reproduced); F86 $2\pi v^2 k$ the small-σ Abelian-BPS limit | 1 + numeric | F70 table matched |

## 5. Honest scope

- **2D-exact, strong-coupling beyond.** The area-law step (Move 2) is exact in 2D (independent plaquettes, F70's mechanism) and strong-coupling/centre-projected in higher $D$; the full non-Abelian 3+1D $\sigma$ still needs the gauge-MC (F94, Option A). The **centre-Lagrange-multiplier identity itself (Moves 1, 3) is rep-independent and $D$-independent** — it is the $\mathbb{Z}_N$ centre algebra of the rule.
- **$p(n)$ from the rule.** Move 4 uses the centre projection of the standard plaquette weight with disorder parameter $\gamma(\Omega)$; the *exact* functional map $\gamma(\Omega)$ from the unitary rotation tick to the Euclidean centre weight (via the rule's transfer operator) is characterised by its limits and monotonicity here, not yet in closed form — the remaining quantitative thread.
- **A-vs-C $k$-dependence persists.** The Abelian-BPS limit gives $\sigma_2=2\sigma_1$ (F86); the full centre weight with non-negligible $p(2)$ gives the Casimir-type $\sigma_2=\sigma_1$ (F94). Same caveat as F98 §4 / F94 CMP3 — they agree on $\sigma_0=0$, $\sigma_{k\ne0}>0$, all the closure principle needs.

## 6. Provenance

- New content: the centre-twist Lagrange-multiplier derivation of $\sigma$ (Moves 1–4, §2), and its reconciliation to F70/F86 (§3).
- Reused: F70 2D area law and `ca_confinement.string_tension`; F94 `lgt_fork_A_mc` links; F86 $2\pi v^2 n$; F97/F98 closure principle.
- Verification: `tests/findings/test_F99_sigma_from_qca_rule.py` (2026-06-05, 5/5 PASS), results `test-results/F99_sigma_from_qca_rule.json`.
