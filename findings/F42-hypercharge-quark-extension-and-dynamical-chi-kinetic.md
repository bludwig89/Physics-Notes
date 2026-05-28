# F42 — Hypercharge $U(1)_Y$ extended to the quark sector AND right-handed singlets promoted to dynamical $Y$-coupled fields in the kinetic step

**Date:** 2026-05-27 - 09:00
**Status:** Confirmed — 8/8 tests PASS
**Module:** `ca-simulation/ca_hypercharge.py` (extension; F41 surface unchanged)
**Tests:** `model-tests/test_hypercharge_extension.py` (Y8–Y15)
**Results:** `test-results/hypercharge_extension.json`
**Closes:** F41 §"Implications" point 4 (quark Y-coupling); first-generation-completeness review §3 item 3 (dynamical $e_R, u_R, d_R$ via kinetic-step $U(1)_Y$).

---

## The two questions

F41 ([F41-hypercharge-higgs-free-su2.md](F41-hypercharge-higgs-free-su2.md)) closed $U(1)_Y$ on the *lepton mass step* without re-introducing a Higgs scalar, by promoting the pure-gauge $U(x)$ to carry the Higgs-equivalent hypercharge $\Delta Y$. Two follow-ups remained:

1. **Quark mass step.** Does the same construction transfer to $(u_L, d_L) \leftrightarrow (u_R, d_R)$ with $\Delta Y_u = -1$, $\Delta Y_d = +1$?
2. **Dynamical $\chi$ kinetic step.** F41's `covariant_phase_per_chirality` returned site phases for $e_R$, $u_R$, $d_R$, but those were never wired into the kinetic step — the singlets remained passive spectators. Can they be promoted to genuinely $Y$-coupled fields under the spectral kinetic step?

---

## Answers

Both yes, at machine precision.

**(1) Quark mass step.** The SM hypercharge assignment gives
$$Y_{Q_L} = +\tfrac{1}{3},\quad Y_{u_R} = +\tfrac{4}{3},\quad Y_{d_R} = -\tfrac{2}{3},$$
so $\Delta Y_u \equiv Y_{Q_L} - Y_{u_R} = -1$ and $\Delta Y_d \equiv Y_{Q_L} - Y_{d_R} = +1$. These are **numerically identical** to the lepton values $(\Delta Y_\nu, \Delta Y_e)$. The Higgs-equivalent diagonal therefore transfers verbatim — exactly the prediction in F41 §"Implications" point 4. Concretely, the quark mass step uses
$$M_{\text{quark}} \;=\; c_m\,I \;+\; i s_m\,\begin{pmatrix} 0 & U \cdot D_q(\alpha) \\ D_q^\dagger(\alpha) \cdot U^\dagger & 0 \end{pmatrix},\qquad D_q(\alpha) = \mathrm{diag}\!\left(e^{+i\alpha\,\Delta Y_u/2},\, e^{+i\alpha\,\Delta Y_d/2}\right).$$

**(2) Dynamical $\chi$ kinetic step.** Each first-generation right-handed singlet $\chi \in \{e_R, u_R, d_R\}$ couples to $\alpha(x)$ through a site-centred Stueckelberg-form wrap of the exact-QCA Weyl spectral step:
$$\boxed{\;\chi(x) \xrightarrow{\,e^{-i\alpha(x)Y/2}\,} \tilde\chi(x) \xrightarrow{\;U_W(k,\,\tfrac{\Delta t}{2})\;} \tilde\chi'(x) \xrightarrow{\,e^{+i\alpha(x)Y/2}\,} \chi'(x).\;}$$

This satisfies the gauge transformation law **exactly** (not just to first order in $\alpha$):
$$S[\alpha+\beta]\bigl(e^{i\beta(x) Y/2}\,\chi\bigr) \;=\; e^{i\beta(x) Y/2}\,S[\alpha](\chi)\qquad\text{for any }\alpha(x),\beta(x).$$
At $\alpha(x) \equiv 0$ the step is bit-for-bit equal to `ca_dirac._weyl_half_step_2c`, so every existing F27/F41 test that does not switch on $\alpha$ still passes unchanged (regression guarantee, Y14).

---

## Implementation

`ca-simulation/ca_hypercharge.py` (F42 block; F41 surface left intact):

| Function / constant | Purpose |
|---|---|
| `Y_QUARK_L = +1/3`, `Y_U_R = +4/3`, `Y_D_R = -2/3` | SM quark hypercharges. |
| `DELTA_Y_U = -1`, `DELTA_Y_D = +1` | Higgs-equivalent $\Delta Y$ absorbed into $U(x)$ on the quark side. |
| `mass_step_quark_doublet_su2xu1y` | F41 mass step ported to the $(u, d)$ quark doublet; same algebraic form, swap $(\Delta Y_\nu, \Delta Y_e) \to (\Delta Y_u, \Delta Y_d)$. |
| `apply_u1y_transform_quark` | Apply $\psi \to e^{i\beta(x)Y_\psi/2}\psi$ to each Weyl quark field. |
| `kinetic_half_step_chi_u1y` | Dynamical $U(1)_Y$-covariant kinetic half-step for one $\chi$ singlet, parameterised by $Y$. |
| `kinetic_half_step_chi_singlets_all` | One-shot helper that runs the kinetic step on $e_R$, $u_R$, $d_R$ with their canonical $Y$ values. |
| `apply_u1y_transform_chi` | Apply $\chi \to e^{i\beta(x)Y/2}\chi$ to a single singlet. |

The quark mass step acts on a single colour at a time; it is exactly the primitive that `ca_strong.quark_doublet_mass_step_su2` already loops over `COLOURS` for (F40's wrapper) — so the F42 step plugs in as a drop-in replacement when $\alpha(x)$ is needed.

---

## Test results — Y8–Y15

| Test | Description | Residual | Target | Status |
|------|-------------|---------:|-------:|:------:|
| Y8  | Quark $U(1)_Y$ Ward identity, d-branch (Higgs) | $8.89\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y9  | Quark $U(1)_Y$ Ward identity, u-branch (conjugate-Higgs) | $8.95\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y10 | $\alpha\equiv 0$ reduces to `ca_dirac.mass_step_doublet_su2` bit-for-bit | $0.0$ | $\leq 10^{-30}$ | PASS |
| Y11 | F27 SU(2)$_L$ Ward identity preserved with nontrivial $\alpha(x)$ | $9.93\times 10^{-16}$ | $\leq 10^{-12}$ | PASS |
| Y12 | Quark mass-step unitarity over 50 random $(U,\alpha)$ steps | $4.43\times 10^{-15}$ | $\leq 10^{-12}$ | PASS |
| Y13 | $\chi$ kinetic-step gauge covariance for $e_R$, $u_R$, $d_R$ + constant-$\alpha$ sanity | $1.78\times 10^{-15}$ | $\leq 10^{-10}$ | PASS |
| Y14 | $\alpha\equiv 0$ → $\chi$ kinetic step bit-for-bit equals `_weyl_half_step_2c` | $0.0$ | $\leq 10^{-30}$ | PASS |
| Y15 | Gell-Mann–Nishijima algebra on the quark side | $5.55\times 10^{-17}$ | $\leq 10^{-15}$ | PASS |

Runtime: $0.033$ s on $L=24$, $m=0.3$. F41 (Y1–Y7) re-run after the extension: still 7/7 PASS unchanged.

---

## What Y13 actually verifies

The exact gauge-covariance identity
$$S[\alpha+\beta](\,e^{i\beta(x)Y/2}\,\chi\,) \;=\; e^{i\beta(x)Y/2}\,S[\alpha](\chi)$$
is checked at machine precision for **each** of the three first-generation right-handed singlets ($Y_{e_R}=-2$, $Y_{u_R}=+4/3$, $Y_{d_R}=-2/3$) with random $\alpha(x), \beta(x)$, plus a constant-$\alpha$ sub-check confirming that a global $U(1)_Y$ phase is physically unobservable on a single field (the spectral step commutes with it and the wrap cancels). All four sub-residuals sit at the FFT round-off floor.

This is the rigorous statement that $\chi$ is **dynamically $Y$-coupled** — the kinetic step is no longer the bare free Weyl propagator, it is the covariantised propagator that transforms correctly under arbitrary local $U(1)_Y$. The Stueckelberg wrap is the spectral-kinetic analog of F31/F34's link-based $W_\mu$ covariantisation: $\tilde\chi(x) = e^{-i\alpha(x)Y/2}\chi(x)$ is the gauge-invariant scalar that propagates freely, and $\alpha(x)$ enters dynamically through the wrap-around phases (the spectral analog of a Wilson line).

---

## Why the lepton ΔY pair re-appears verbatim in the quark sector

$\Delta Y$ depends only on $Y_L - Y_R$, not on $Y_L$ itself. The SM has
$$Y_L - Y_{R,\text{up-type}} = -1,\qquad Y_L - Y_{R,\text{down-type}} = +1,$$
holding for **both** generations of each chirality pair: $(\nu_L, \nu_R)$ and $(u_L, u_R)$ are "up-type" (ΔY = −1); $(e_L, e_R)$ and $(d_L, d_R)$ are "down-type" (ΔY = +1). In the SM this is exactly the fact that the same Higgs field $\Phi$ gives mass to down-type fermions via $\bar\psi_L\,\Phi\,\psi_R$ and to up-type fermions via $\bar\psi_L\,i\sigma_2\Phi^*\,\psi_R$. In the Higgs-free CA it is the fact that **one** extended $U(x)$ field with two diagonal phase eigenvalues $(\Delta Y_u, \Delta Y_d) = (\Delta Y_\nu, \Delta Y_e) = (-1, +1)$ services *both* lepton and quark mass steps — there is no separate "quark Higgs" because there is no Higgs.

---

## Implications for the model

1. **First-generation closure — item 3 of the completeness review is now closed.** The right-handed singlets are no longer spectators: under any local $U(1)_Y$ rotation $\beta(x)$, each $\chi$ field rotates by $e^{i\beta(x)Y/2}$ and the kinetic step transforms covariantly to machine precision.
2. **Quark side now matches lepton side at every algebraic level.** Mass step (F40 + F42), SU(2)$_L$ Ward identity (F40/Q9 + F42/Y11), $U(1)_Y$ Ward identity (F42/Y8, Y9), Gell-Mann–Nishijima algebra (F42/Y15) all hold at machine ε on both sides.
3. **No Higgs boson is required anywhere in the first-generation electroweak sector.** F27 (mass), F34b (W mass via Stueckelberg), F41 (lepton $Y$), F42 (quark $Y$ + dynamical $\chi$) collectively replace all three SM Higgs roles for the first generation.
4. **Next item — dynamical $Z$ coupled to the neutral current.** F35 fixed the algebraic Weinberg mixing; F42's gauge-covariant $\chi$ kinetic step is the prerequisite for that wiring because $Z$ couples to $\chi$ through its $Y$-component.

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| F27 chiral SU(2) mass | F42's quark mass step is F27 + Y-extension; reduces to F27 bit-for-bit at $\alpha=0$ (Y10). |
| F34 / F34b W vertex + Stueckelberg mass | The $\chi$ kinetic Stueckelberg wrap is the Abelian analog of F34's link-based isospin covariantisation. |
| F35 electroweak mixing | F42 supplies the dynamical Y on $\chi$ that F35's algebraic mixing requires. |
| F40 quark electroweak | F40 left $\chi_u, \chi_d$ as spectators with identity isospin; F42 promotes them to dynamical $Y$-coupled fields. |
| F41 lepton hypercharge | F42 is the verbatim port to the quark sector + the kinetic-step promotion F41 deferred. |

---

## Files added / modified

- `ca-simulation/ca_hypercharge.py` — appended ~150 lines: F42 quark constants, `mass_step_quark_doublet_su2xu1y`, `apply_u1y_transform_quark`, `kinetic_half_step_chi_u1y`, `kinetic_half_step_chi_singlets_all`, `apply_u1y_transform_chi`. F41 surface unchanged.
- `model-tests/test_hypercharge_extension.py` (new) — Y8–Y15 (8 tests).
- `test-results/hypercharge_extension.json` (new) — 8/8 PASS at machine ε.
