# F63 — The cost of the torsion-free assumption: Einstein–Cartan spin-torsion is ≲0.3% at F62 densities, O(1) only above ~3 quanta per cell

**Date:** 2026-05-30 - 21:06
**Status:** Confirmed — 5/5 checks PASS (EC coefficient exact-rational; ratio and Cartan density real-arithmetic). This is a **bounded magnitude estimate**, not a dynamical torsion simulation (that is plan item D3b, open research).
**Module:** new `ca-simulation/forks/gr_fork_F63_spin_torsion_estimate.py` (self-contained; real arithmetic only, no scipy/chiral bilinear). **Tests:** `model-tests/test_F63_spin_torsion_estimate.py`; results `test-results/F63_spin_torsion_estimate.json`.
**Origin:** the reconciliation in `page34-eom-derivation.md` §2/§4 — page 34's first-order (Palatini) variation w.r.t. the independent connection $\Omega_\mu$ (EOM 3) would generate Einstein–Cartan torsion sourced by fermion spin, which the project (F50/F52/F62) drops by working torsion-free. This finding answers whether that omission costs anything.

## What was open

Page 34 of the notebook sets up a first-order action with $q^\mu,\Omega_\mu,\eta,\chi$ independent. Varying $\Omega_\mu$ gives the **Einstein–Cartan connection equation**: torsion is fixed *algebraically* by the spinor spin density, and eliminating it leaves the standard axial-axial four-fermion contact term

$$\mathcal{L}_{4f} = -\tfrac{3}{16}\,\kappa\,\big(\bar\psi\gamma_5\gamma^\mu\psi\big)\big(\bar\psi\gamma_5\gamma_\mu\psi\big),\qquad \kappa=\frac{8\pi G}{c^4}.$$

The project assumes the torsion-free branch (the source-free solution of EOM 3). The honest question: **at the fermion densities the lattice actually runs, is the dropped four-fermion term negligible, or is the assumption quietly throwing away real physics?**

## Method (why it is numpy-safe)

Energy-density bookkeeping in lattice/Planck units ($\hbar=c=1$, $G=\ell_P^2$), comparing the EC four-fermion density $u_{4f}$ to the Dirac density $u_\text{Dirac}$ of the same fermions. The chiral bilinear is **never contracted numerically** (that would route through the $\gamma_5\gamma^\mu$ matrices — the CLAUDE.md chiral caveat). Instead the *polarised upper bound* $|\bar\psi\gamma_5\gamma^\mu\psi|\le n$ (number density) is used, so a fully spin-polarised packet saturates it and the estimate is **conservative** — a "negligible" verdict is therefore robust. The cell size is F61's pinned $a = P_\text{pre}\,d^{1/4}\ell_P$, $P_\text{pre}=\sqrt{2\pi\eta g_*}$, $\eta_\text{Weyl}=1/12$, $g_*=16$.

With number density $n=f/a^3$ ($f$ = occupation, fermions per cell), the largest (cutoff-scale, $\omega\sim m\sim1/a$) ratio is the closed form

$$\boxed{\;r_\text{cutoff}(f)=\frac{u_{4f}}{u_\text{Dirac}}=\frac{3\pi}{2}\,f\,\Big(\frac{\ell_P}{a}\Big)^2=\frac{3\pi}{2}\,\frac{f}{2\pi\eta g_*\sqrt d}=\frac{3f}{4\,\eta g_*\sqrt d}.\;}$$

Torsion scales as $n^2$ while Dirac scales as $n$, so the ratio is **linear in occupation** $f$.

## Results

| Check | What it verifies | Result |
|---|---|---|
| EC coefficient | the $-\tfrac{3}{16}\kappa\,j_5^2$ prefactor | $3/16$ **exact (rational)** |
| F61 cell | $a/\ell_P$ at $g_*=16,d=3$ | $3.809$ (matches F61) |
| F62 densities | all 4 D2/D3a packet configs evaluated, not skipped | 4/4, worst $r=2.9\times10^{-3}$ |
| Cartan density | occupation $f^*$ where $r_\text{cutoff}=1$ | $f^*=3.08$ quanta/cell |

- **At F62's actual packet densities the torsion term is ≲0.3%.** F62's tests release one quantum spread over a Gaussian of width $\sigma\in\{6,7,16\}$, giving peak occupation $f_\text{peak}=1/(\pi\sigma^2)\approx1.2\times10^{-3}$–$8.8\times10^{-3}$. The resulting $r_\text{cutoff}$ ranges $4\times10^{-4}$ (Rindler) to $2.9\times10^{-3}$ (deflection / backreaction). The rest-mass ratio $r_\text{rest}=r_\text{cutoff}/m$ peaks at $1.4\times10^{-2}$ for the $m=0$ deflection packet (where the "rest" floor is set to $m=0.2$). **The torsion-free assumption costs F62 nothing measurable** — well below its 1–25% quantitative tolerances.
- **Torsion becomes O(1) only at $f^*\approx3$ quanta per cell.** With a cell of $\sim3.8\,\ell_P$, that is essentially Planck-scale density (several fermions packed into one near-Planck cell). Below it, the assumption is safe; the lattice would have to be driven to super-dense, near-Planck occupancy before Einstein–Cartan torsion competes with the Dirac dynamics.

## Interpretation

The reconciliation document flagged EOM 3 as the *one* place page 34's first-order variation exposes genuinely new content (the spin-torsion four-fermion term) absent from the project's torsion-free emergent gravity. F63 quantifies it: that content is a contact term suppressed by $f(\ell_P/a)^2$, so it is **parametrically negligible in the entire sparse-fermion regime** the model operates in, and reaches O(1) only at the Cartan (near-Planck) density $f^*\approx3$/cell. This is consistent with the continuum Einstein–Cartan result (torsion matters only near $\rho_\text{Cartan}$, far above nuclear density) and *vindicates* the project's choice to drop torsion — it is not an approximation that costs accuracy at any density F62/F52 tests, only a statement that the model is not resolving trans-Planckian fermion packing.

## What is derived vs posited

- **Derived/exact:** the EC four-fermion prefactor $3/16$ (rational); the closed-form ratio $r_\text{cutoff}=\tfrac{3f}{4\eta g_*\sqrt d}$; the Cartan occupation $f^*=\tfrac{2}{3\pi}(a/\ell_P)^2$.
- **Posited (conservative inputs):** the polarised bound $j_5\le n$ (upper bound, makes the estimate worst-case); $\omega\sim1/a$ for the cutoff ratio (largest); F61's $a$, $\eta=1/12$, $g_*=16$.
- **Not done (open, D3b):** an actual dynamical torsion field co-evolved with the Dirac CA. F63 is the *pre-check* that says such a simulation would see ≲0.3% effects at current densities — i.e. D3b's torsion sector is safely ignorable until the model is pushed to near-Planck occupancy.

## Limitations / honest caveats

- This is dimensional/energy-density bookkeeping, not a measured lattice observable. The factor of $3\pi/2$ and the polarised bound are order-unity; the robust content is the **scaling** ($r\propto f(\ell_P/a)^2$) and the **two-orders-of-magnitude margin** at F62 densities, not the third significant figure.
- The Dirac "rest floor" $\omega\ge m$ understates $u_\text{Dirac}$ for relativistic packets (which would make $r$ *smaller*), so using it is again conservative.
- $g_*=16$ is the fermionic one-generation count (F61); the gauge sector does not carry spin-1/2 torsion, so it does not enter $j_5$.

## Relation to other findings

Follows directly from `page34-eom-derivation.md` (the page-34 EOM reconciliation). Uses **F61** (pinned cell size $a$, $\eta$, $g_*$) and checks against **F62** (the dynamical curved-background Dirac CA whose densities it evaluates). Sits upstream of plan item **D3b** (full nonlinear backreaction / torsion), which it pre-screens as negligible at current densities. Links: [[F62-dirac-gravity-dynamical-fork]], [[F61-weyl-eta-and-gstar-prefactor]], [[F52-gravity-from-rest-leg-backreaction]].
