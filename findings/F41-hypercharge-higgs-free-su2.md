# F41 — Hypercharge U(1)_Y is exactly compatible with the Higgs-free F27 chiral SU(2) mass model

**Date:** 2026-05-26 - 17:45
**Status:** Confirmed — 7/7 tests PASS
**Module:** `ca-simulation/forks/hypercharge_fork.py`
**Tests:** `model-tests/test_hypercharge_fork.py` (Y1–Y7)
**Results:** `test-results/hypercharge_fork.json`

---

## The question

After F27 (chiral SU(2) mass from β-gauging — no Higgs Yukawa) and F34b (W mass from Stueckelberg — no Higgs VEV), one role of the Standard Model Higgs remains untested: it carries hypercharge $Y_\Phi = +1$, balancing the mismatch $Y_L - Y_{e_R} = +1$ in the Yukawa term $\bar\Phi\,\bar\psi_L\,\psi_R$.

Concretely, the F27 mass step couples $\eta_L$ (with $Y_L = -1$) directly to $\chi_R$ (with $Y_R(e) = -2$ or $Y_R(\nu) = 0$). Under $U(1)_Y$ the bilinear $\eta^\dagger\chi$ picks up a phase $\alpha\,(Y_R - Y_L)/2 \neq 0$, so the *bare* F27 mass step is **NOT** $U(1)_Y$-invariant.

Does this kill $U(1)_Y$ in the Higgs-free model? Does the SU(2)_L lepton sector still work as before?

---

## Answer

$U(1)_Y$ is fully compatible — provided the pure-gauge field $U(x)$ inside the F27 mass step is extended to carry the Higgs-equivalent hypercharge:

$$U(x) \;\longrightarrow\; U(x)\,\cdot\,\mathrm{diag}\!\left(e^{+i\alpha(x)\,\Delta Y_\nu/2},\;e^{+i\alpha(x)\,\Delta Y_e/2}\right)$$

with $\Delta Y_e = Y_L - Y_{e_R} = +1$ (the SM Higgs hypercharge) and $\Delta Y_\nu = Y_L - Y_{\nu_R} = -1$ (the conjugate-Higgs hypercharge, played by $i\sigma_2\Phi^*$ in the SM). The diagonal factor sits *between* the SU(2)_L rotation $U$ and the right-handed isospin index, so:

- **SU(2)_L Ward identity (F27 T5) is preserved exactly** — the U(1)_Y phase commutes with the SU(2)_L rotation on the isospin index (both $\nu_L$ and $e_L$ share $Y_L = -1$, so the Y phase is *common* across the L-doublet and factors out of any SU(2) action).
- **U(1)_Y Ward identity is exact** — for both the e-branch and the ν-branch (the conjugate-Higgs sign convention is required).
- **Mass step unitarity is preserved** — $M = c_m I + i s_m A$ with $A^\dagger = A$ and $A^2 = I$ remains intact when the diagonal Y-phase is unitary.

In gauge-theoretic language, $U(x)$ is promoted from pure gauge in $\mathrm{SU}(2)_L$ to pure gauge in $\mathrm{SU}(2)_L \times U(1)_Y$. No physical scalar boson is introduced; the additional phase d.o.f. becomes the longitudinal mode of the $Z$ under the Stueckelberg mechanism (F34b).

---

## Implementation

`ca-simulation/forks/hypercharge_fork.py` provides:

| Function | Purpose |
|----------|---------|
| `mass_step_doublet_su2xu1y` | Extended F27 mass step with per-branch Higgs-equivalent phases |
| `apply_u1y_transform` | Applies $\psi \to e^{i\beta(x)Y_\psi/2}\psi$ to each Weyl field |
| `make_u1y_field` | Site-centred U(1)_Y angle $\alpha(x)$ (identity / random / plane) |
| `covariant_phase_per_chirality` | $(e^{i\beta Y_L/2}, e^{i\beta Y_{\nu_R}/2}, e^{i\beta Y_{e_R}/2})$ factors for kinetic steps |
| Constants `Y_LEPTON_L`, `Y_E_R`, `Y_NU_R`, `DELTA_Y_E`, `DELTA_Y_NU` | SM hypercharge assignments |

The mass step at each lattice cell is

$$M \;=\; c_m\,I \;+\; i s_m\,\begin{pmatrix} 0 & U \cdot D(\alpha) \\ D^\dagger(\alpha) \cdot U^\dagger & 0 \end{pmatrix},\qquad D(\alpha) = \mathrm{diag}(e^{+i\alpha\,\Delta Y_\nu/2},\, e^{+i\alpha\,\Delta Y_e/2}).$$

When $\alpha(x) \equiv 0$ this reduces *bit-for-bit* (residual $0.0$) to `ca_dirac.mass_step_doublet_su2`.

---

## Test results

| Test | Description | Residual | Target | Status |
|------|-------------|---------:|-------:|:------:|
| Y1 | U(1)_Y Ward identity, e-branch | $9.04\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y2 | U(1)_Y Ward identity, ν-branch (conjugate) | $9.16\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y3 | $\alpha\equiv 0$ reduces to F27 bit-for-bit | $0.0$ | $\leq 10^{-30}$ | PASS |
| Y4 | SU(2)_L Ward identity with random $\alpha$ | $9.16\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y5 | $U=I$ → no isospin leakage from U(1)_Y | $0.0$ | $\leq 10^{-12}$ | PASS |
| Y6 | Mass-step unitarity, 50 random $(U,\alpha)$ steps | $4.53\times 10^{-15}$ | $\leq 10^{-12}$ | PASS |
| Y7 | Gell-Mann–Nishijima algebra $Q = T_3 + Y/2$ | $0.0$ | $0$ | PASS |

Runtime: 0.014 s on $L=24$, $m=0.3$.

---

## Y3 / Y5 — The SU(2) lepton field is NOT affected

These two results jointly confirm that the user's first concern — *will it still work with the chiral SU(2) mass model?* — is answered yes:

- **Y3** (bit-for-bit reduction): turning the U(1)_Y field off ($\alpha\equiv 0$) gives exactly the F27 mass step; no algebraic drift was introduced. Every F27 test (T1–T9 in [F27](F27-complex-mass-chiral-su2.md)) therefore still passes against `mass_step_doublet_su2xu1y(\alpha=0)`.
- **Y5** (no isospin leakage): with $U(x) = I$, U(1)_Y does NOT rotate ν into e or vice-versa. Starting from pure $\chi_\nu$ initial data, no $\eta_e$ output appears (residual $0.0$), and symmetrically for $\chi_e$. The Higgs-equivalent diagonal $D(\alpha)$ stays diagonal because both Δ-charges sit on the diagonal — U(1)_Y is *strictly* an Abelian phase on the isospin eigenstates, not a rotation between them.

The SU(2)_L Ward identity (Y4) is the formal statement that the F27 chiral-SU(2)_L symmetry survives the Y-extension intact.

---

## Physics interpretation

The SM Higgs hypercharge $Y_\Phi = +1$ has a clean re-interpretation in the Higgs-free CA:

> $Y_\Phi$ is **not** a property of any physical scalar field — it is the hypercharge that the F27 pure-gauge field $U(x)$ must carry in order for the chiral mass step to commute with $U(1)_Y$.

The conjugate-Higgs structure $i\sigma_2\Phi^*$ that the SM uses to give up-type quarks mass is recovered automatically as the $\Delta Y_\nu = -1$ branch of the diagonal $D(\alpha)$. So the SM's "two different Higgs operators for up vs. down" arises here as a *single* extended $U(x)$ field with two diagonal phase eigenvalues — one fewer free object in the theory.

---

## Implications for the model

1. **Charge conservation is exact at the mass-step level** (Y1, Y2) — the previously-noted Yukawa-style Y mismatch in F27 is resolved without re-introducing the Higgs.
2. **F35's algebraic $Q = T_3 + Y/2$ table** now has a dynamical companion: the per-fermion phase under a $U(1)_Y$ rotation is consistent with the Gell-Mann–Nishijima assignment (Y7 verified algebraically; Y1/Y2 verified at the mass step).
3. **The Stueckelberg path (F34b) is unchanged** — extending $U(x)$ to carry one extra U(1)_Y phase costs one additional Goldstone d.o.f., exactly what Stueckelberg eats to give $Z$ its longitudinal mode. **Rank-1 mass-matrix consequence (F44):** because $U(x)$ is a *single* field carrying both the $\mathrm{SU}(2)_L$ direction and the $U(1)_Y$ phase, the covariant Stueckelberg kinetic $(f^2/2)\,\mathrm{tr}|D_\mu U|^2$ evaluated at $U = I$ produces a $(W^3, B)$ mass block $f^2\binom{g}{-g'}\binom{g\ -g'}$ — a *rank-1 outer product*, with $\det = 0$ and exactly one non-zero eigenvalue $m_Z^2 = f^2(g^2+g'^2)$. The photon's masslessness ($m_A = 0$) is therefore a *structural consequence* of the single-$U$ construction, not an extra constraint. The notebook's "anomalous" $W^3 B$ cross term flagged in `physics-notes-complete-review.md` §3.1 is the off-diagonal of this rank-1 block, absorbed by the W6.1 rotation into $\mathrm{diag}(0, m_Z^2)$. Confirmed at machine precision by `test_wmu_phase6_rank1.py` (W6.6–W6.8), residuals $\le 1.5\times 10^{-15}$. See [F44](F44-higgs-free-mA-zero-from-rank1-stueckelberg.md).
4. **Quark sector (F40 / FG-2 / FG-3)** receives a follow-up task: the up- and down-type quarks have $Y_L = +1/3$ vs. $Y_R(u) = +4/3$ and $Y_R(d) = -2/3$, so $\Delta Y_u = -1$ and $\Delta Y_d = +1$ — the *same* pair of values as $(\Delta Y_\nu,\Delta Y_e)$ in the lepton sector. The hypercharge fork should transfer verbatim to the quark mass step, modulo the universal Y_L assignment.

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| F27 chiral SU(2) | $U(x)$ is the pure-gauge field whose Y-extension this fork constructs |
| F34b Stueckelberg W mass | The extra U(1)_Y phase becomes the Z longitudinal mode |
| F35 electroweak mixing | Algebraic $Q = T_3 + Y/2$ now has dynamical confirmation |
| F38 anomaly cancellation | Y values used here are exactly the FG-1 anomaly-cancelling set |
| F40 quark electroweak | Hypercharge fork extends to quark mass step (next task) |

---

## Files

- `ca-simulation/forks/hypercharge_fork.py` — fork module (does not modify any existing file)
- `model-tests/test_hypercharge_fork.py` — Y1–Y7 test suite
- `test-results/hypercharge_fork.json` — numerical results
