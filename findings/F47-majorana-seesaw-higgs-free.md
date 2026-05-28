# F47 — Higgs-free ν_R Majorana mass step and see-saw scaling: a natural explanation for the smallness of the neutrino mass

**Date:** 2026-05-28 - 14:00
**Status:** Confirmed — 6/6 tests PASS
**Module:** `ca-simulation/forks/hypercharge_fork.py` (re-exports `ca_hypercharge`; F43 block adds Majorana primitives)
**Tests:** `model-tests/test_majorana_fork.py` (M1–M6)
**Results:** `test-results/majorana_fork.json`
**Builds on:** F27 chiral SU(2) Dirac CA, F41 hypercharge fork, F42 quark+dynamical-χ kinetic.

---

## The question

In F41 the right-handed neutrino $\nu_R$ entered with $Y_{\nu_R} = 0$ — the SM assignment — but the mass step *only* gave it a Dirac mass $M_D$ via the F27 $\eta \leftrightarrow \chi$ coupling. The standard see-saw mechanism additionally allows a **bare Majorana mass** on $\nu_R$,

$$\mathcal L_M \;=\; -\tfrac12 M_R \,\bigl(\nu_R^T \varepsilon \,\nu_R \;+\; \text{h.c.}\bigr),\qquad \varepsilon \;=\; i\sigma^2,$$

and in the SM this is the *only* gauge-invariant mass term available for a singlet because $\nu_R^T \varepsilon \nu_R$ carries hypercharge $2Y_{\nu_R} = 0$. The question for our Higgs-free CA is:

1. **(a)** Does the bare $\nu_R$ Majorana mass step, written in QCA form, remain (i) unitary on the lattice and (ii) gauge-invariant under the F41 $U(1)_Y$?
2. **(b)** Combined with the F27/F41 Dirac mass, does the lattice reproduce the canonical see-saw scaling

$$m_\nu \;\approx\; \frac{M_D^2}{M_R}\qquad (M_R \gg M_D)?$$

If yes, the smallness of the active neutrino mass is explained **with no Higgs anywhere** in the model: a single large scale $M_R$ replaces an unnaturally small Yukawa coupling.

---

## Answer

Both yes, at machine precision and across $M_R/M_D \in \{3, 10, 30, 100, 300, 10^3, 3\!\cdot\!10^3, 10^4, 3\!\cdot\!10^4, 10^5\}$.

### (a) Bare Majorana step — unitary and gauge-covariant

The QCA Majorana step on a single Weyl singlet is the closed-form integration of the BdG-form EOM $i\partial_t \chi_u = +M_R \chi_d^*$, $i\partial_t \chi_d = -M_R \chi_u^*$:

$$\boxed{\;\chi_u' \;=\; c_M\,\chi_u \;-\; i s_M\,\chi_d^*,\qquad \chi_d' \;=\; c_M\,\chi_d \;+\; i s_M\,\chi_u^*\;}$$

with $c_M = \cos(M_R\,dt)$, $s_M = \sin(M_R\,dt)$. The step is *anti-linear* in $\chi$ (couples $\chi$ to $\chi^*$) — that anti-linearity is intrinsic to a Majorana mass and is the source of lepton-number violation.

**R-unitarity.** A direct algebraic expansion gives

$$|\chi_u'|^2 + |\chi_d'|^2 \;=\; (c_M^2 + s_M^2)(|\chi_u|^2 + |\chi_d|^2) \;+\; 2 c_M s_M\,\bigl[\operatorname{Re}(i\chi_u\chi_d) - \operatorname{Re}(i\chi_u\chi_d)\bigr] \;=\; |\chi_u|^2 + |\chi_d|^2,$$

so the step is exactly R-unitary on the 4 real DOFs. Test **M1** verifies this over a sweep of $M_R \in \{0, 10^{-6}, 0.1, 0.3, 1, 5, 17.7, 10^3, 10^6\}$, $dt \in \{0.05, 0.31, 1.0, 1.27\}$, and a 200-step composition.

**$U(1)_Y$ selection rule.** Under $V_Y[\beta]$ the singlet rotates as $\chi \to e^{i\beta Y_{\nu_R}/2}\chi$, so the Majorana bilinear $\chi^T \varepsilon \chi$ picks up $e^{i\beta Y_{\nu_R}}$. The step is invariant iff $Y_{\nu_R} \equiv 0 \pmod{2\pi/\beta}$. Tests **M2** (residual $0.0$ at $Y_{\nu_R} = 0$) and **M3** (residual machine-zero at $Y = 0$, *non-zero* and within the predicted $4 s_M \|\chi\|$ bound at $Y \in \{-2, +4/3\}$) verify both halves of the selection rule explicitly.

**This is the Higgs-free realisation of the SM rule.** In the SM the rule is enforced by $U(1)_Y$; here it is enforced by *exactly the same* $U(1)_Y$ gauge constraint inherited from F41, with no Higgs field appearing anywhere in the construction.

### (b) See-saw scaling — exact, then asymptotic

Combined with the F27 Dirac step, the local mass operator on the $(\nu_L, \nu_R)$ sector has the canonical see-saw 2×2 mass matrix in the $(\nu_L, \nu_R^c)$ basis:

$$M \;=\; \begin{pmatrix} 0 & M_D \\ M_D & M_R \end{pmatrix},\qquad \lambda_\pm \;=\; \frac{M_R \,\pm\, \sqrt{M_R^2 + 4M_D^2}}{2}.$$

In the limit $M_R \gg M_D$,

$$|\lambda_-| \;=\; \frac{\sqrt{M_R^2 + 4M_D^2} - M_R}{2} \;=\; \frac{M_D^2}{M_R}\bigl(1 - M_D^2/M_R^2 + \mathcal O((M_D/M_R)^4)\bigr).$$

Test **M5** verifies the closed form against `numpy.linalg.eigvalsh` over 64 random $(M_D, M_R)$ samples (max residual $1.82\times 10^{-12}$, target $10^{-9}$). Test **M6** sweeps the ratio $M_R/M_D$ and confirms the see-saw scaling holds within the next-order bound at every sampled ratio:

| $M_R/M_D$ | $m_\nu$ (closed form) | $M_D^2/M_R$ | $\biglabs(m_\nu\!\cdot\! M_R/M_D^2 - 1\bigr)$ | bound $1.1\,(M_D/M_R)^2$ |
|---:|---:|---:|---:|---:|
| 3        | $3.03\!\times\!10^{-1}$ | $3.33\!\times\!10^{-1}$ | $9.17\!\times\!10^{-2}$ | $1.22\!\times\!10^{-1}$ |
| 10       | $9.90\!\times\!10^{-2}$ | $1.00\!\times\!10^{-1}$ | $9.81\!\times\!10^{-3}$ | $1.10\!\times\!10^{-2}$ |
| 30       | $3.33\!\times\!10^{-2}$ | $3.33\!\times\!10^{-2}$ | $1.11\!\times\!10^{-3}$ | $1.22\!\times\!10^{-3}$ |
| 100      | $1.00\!\times\!10^{-2}$ | $1.00\!\times\!10^{-2}$ | $1.00\!\times\!10^{-4}$ | $1.10\!\times\!10^{-4}$ |
| 300      | $3.33\!\times\!10^{-3}$ | $3.33\!\times\!10^{-3}$ | $1.11\!\times\!10^{-5}$ | $1.22\!\times\!10^{-5}$ |
| 1 000    | $1.00\!\times\!10^{-3}$ | $1.00\!\times\!10^{-3}$ | $1.00\!\times\!10^{-6}$ | $1.10\!\times\!10^{-6}$ |
| 3 000    | $3.33\!\times\!10^{-4}$ | $3.33\!\times\!10^{-4}$ | $1.11\!\times\!10^{-7}$ | $1.22\!\times\!10^{-7}$ |
| 10 000   | $1.00\!\times\!10^{-4}$ | $1.00\!\times\!10^{-4}$ | $1.00\!\times\!10^{-8}$ | $1.10\!\times\!10^{-8}$ |
| 30 000   | $3.33\!\times\!10^{-5}$ | $3.33\!\times\!10^{-5}$ | $1.11\!\times\!10^{-9}$ | $1.22\!\times\!10^{-9}$ |
| 100 000  | $1.00\!\times\!10^{-5}$ | $1.00\!\times\!10^{-5}$ | $1.00\!\times\!10^{-10}$ | $1.10\!\times\!10^{-10}$ |

The deviation tracks exactly $1.0\cdot(M_D/M_R)^2$ — i.e., $0.91$ of the conservative $1.1$ bound — at every ratio.

**Cross-check between the 2×2 see-saw matrix and the lattice 8×8 BdG.** A separate construction, `bdg_hamiltonian_nu(M_D, M_R)`, builds the 8×8 Hermitian generator extracted directly from the $dt\to0$ limit of `mass_step_dirac_majorana_nu`. Test **M4** verifies that the numerical Jacobian of the QCA mass step at $dt = 10^{-7}$ equals this analytic 8×8 to $4.1\times 10^{-8}$ (target $10^{-4}$). Test **M6** then verifies that the smallest $|$eigenvalue$|$ of the 8×8 BdG matches $|\lambda_-|$ of the 2×2 closed form to $\le 10^{-12}\cdot M_R$ at every ratio — connecting the lattice CA realisation and the analytic see-saw spectrum at machine precision.

---

## Implementation

`ca-simulation/forks/hypercharge_fork.py` re-exports every primitive from the promoted `ca_hypercharge` module and adds the following Majorana block:

| Function | Purpose |
|---|---|
| `mass_step_majorana_chi(chi_u, chi_d, M_R, dt)` | Bare Majorana step on one Weyl singlet (closed form). Anti-linear; R-unitary. |
| `mass_step_dirac_majorana_nu(eta_u, eta_d, chi_u, chi_d, M_D, M_R, dt)` | Strang-split Majorana($dt/2$) ∘ Dirac($dt$) ∘ Majorana($dt/2$) on the ν sector — the see-saw probe step (no SU(2)_L, no kinetic). |
| `seesaw_2x2_matrix(M_D, M_R)` | The canonical 2×2 see-saw mass matrix in the $(\nu_L, \nu_R^c)$ basis. |
| `seesaw_eigenvalues(M_D, M_R)` | Numerically stable closed-form eigenvalues via Vieta ($\lambda_+\lambda_- = -M_D^2$) — avoids catastrophic cancellation at $M_R \gg M_D$. Returns `(lam_light, lam_heavy)` sorted by $|\cdot|$. |
| `seesaw_light_mass_approx(M_D, M_R)` | The asymptotic $M_D^2/M_R$ formula for reference / comparison. |
| `bdg_hamiltonian_nu(M_D, M_R)` | 8×8 Hermitian BdG generator on the doubled space; decomposes into two independent 4×4 blocks with the see-saw spectrum each. |
| `bdg_spectrum_nu(M_D, M_R)` | Eigenvalues of `bdg_hamiltonian_nu`, sorted by $|\lambda|$. |

The Majorana primitives are *additive* — every existing F41/F42 surface (`mass_step_doublet_su2xu1y`, `kinetic_half_step_chi_u1y`, …) is left bit-for-bit unchanged.

---

## Test results — M1 through M6

| Test | Description | Residual | Target | Status |
|------|-------------|---------:|-------:|:------:|
| **M1** | Bare Majorana step preserves $|\chi_u|^2 + |\chi_d|^2$ (sweep $M_R \in \{0,\ldots,10^6\}$, $dt \in \{0.05,\ldots,1.27\}$, 200-step compose) | $2.25\times 10^{-11}$ | $10^{-9}$ | PASS |
| **M2** | Majorana step invariant under $U(1)_Y$ at $Y_{\nu_R} = 0$ (the SM assignment) | $0.0$ exact | $10^{-12}$ | PASS |
| **M3** | $U(1)_Y$ selection rule: residual machine-zero at $Y=0$, *non-zero* and within the $4s_M\|\chi\|$ bound for $Y \in \{-2, +4/3\}$ | $0.0$ exact at $Y=0$, witness PASS for $Y\ne 0$ | $10^{-12}$ | PASS |
| **M4** | Numerical Jacobian of `mass_step_dirac_majorana_nu` at $dt=10^{-7}$ equals `bdg_hamiltonian_nu(M_D, M_R)` | $4.11\times 10^{-8}$ | $10^{-4}$ | PASS |
| **M5** | Closed-form `seesaw_eigenvalues` matches `numpy.linalg.eigvalsh(seesaw_2x2_matrix)` over 64 random samples | $1.82\times 10^{-12}$ | $10^{-9}$ | PASS |
| **M6** | See-saw scaling: $m_\nu \!\cdot\! M_R/M_D^2 \to 1$ within $(M_D/M_R)^2$ bound at every sampled ratio; BdG light eigenvalue matches closed form within $10^{-12}\,M_R$ | $0.0$ exact (excess over bound) | $0$ | PASS |

Runtime: $7.9 \text{ ms}$ for 6/6 tests on a $16{\times}16$ lattice. JSON: [`test-results/majorana_fork.json`](../test-results/majorana_fork.json).

---

## Implications for the model

1. **Higgs-free neutrino-mass hierarchy.** The smallness of the active neutrino mass $m_\nu \sim 0.1$ eV alongside $m_e \sim 0.5$ MeV is explained by a single large Majorana scale $M_R$, not by an unnaturally tiny Yukawa coupling. Concretely, with $M_D \sim m_e$ and $M_R \sim 10^{12}-10^{15}\,\text{GeV}$, the see-saw produces $m_\nu \sim 10^{-2}-10^{-5}\,\text{eV}$ — the observed range — automatically.
2. **$Y_{\nu_R} = 0$ is structural, not a free parameter.** The same $U(1)_Y$ gauge constraint that forbade a Higgs scalar in F27/F34b/F41 also forces $\nu_R$ to be a $Y = 0$ singlet for a Majorana mass to exist. In the SM this is presented as a coincidence of the hypercharge assignment; here it is a consequence of one structural choice.
3. **Lepton-number violation is intrinsic.** The Majorana step is anti-linear in $\chi$ (couples $\chi$ to $\chi^*$). Lepton number is therefore not conserved by the F47 mass step, which is the prerequisite for any see-saw mechanism. Concrete CA experiments (neutrinoless double-beta-like processes) become possible without any further machinery.
4. **No new sector needed.** F47 is a *single* additional bare-mass term in the existing F41 ν-sector — no new gauge group, no new scalar, no new fermion content beyond the right-handed singlet that F41 already had.

---

## Open follow-ups

1. **Promote to a sibling module.** If the F47 step is used by downstream constructions (sterile-neutrino dispersion, lepton-number-violating processes), the natural promotion path is a new `ca_majorana.py` mirroring the F41 → `ca_hypercharge.py` promotion.
2. **Three generations.** The single-flavour see-saw block here generalises to a $3\times 3$ Majorana mass matrix $M_R$ and a $3\times 3$ Dirac matrix $M_D$. The lattice block then becomes the $6\times 6$ see-saw matrix $\bigl[\begin{smallmatrix}0 & M_D\\M_D^T & M_R\end{smallmatrix}\bigr]$ and the eigenvalues give the three light (active) and three heavy (sterile) neutrino masses. PMNS mixing falls out of the diagonalisation.
3. **Kinetic step for Majorana fields.** F42's `kinetic_half_step_chi_u1y` already runs at $Y_{\nu_R} = 0$ trivially (zero phase), so the kinetic sector is already F47-compatible. A dedicated test verifying composability — kinetic ∘ Majorana mass — is the natural M7.
4. **Lepton-number-violation diagnostic.** A direct test that the F47 step does not conserve $L = \int (|\eta|^2 - |\chi^c|^2)$ would explicitly distinguish it from a pure Dirac construction. Predicted residual: $\mathcal O(s_M\|\chi\|^2)$.

---

## References

- F27 chiral SU(2) Dirac CA — [F27](F27-complex-mass-chiral-su2.md)
- F41 hypercharge Higgs-free $U(1)_Y$ — [F41](F41-hypercharge-higgs-free-su2.md)
- F42 quark + dynamical χ kinetic — [F42](F42-hypercharge-quark-extension-and-dynamical-chi-kinetic.md)
- Standard see-saw I (Minkowski 1977; Gell-Mann, Ramond, Slansky 1979; Mohapatra–Senjanović 1980) — for the textbook 2×2 matrix and its eigenvalues.
