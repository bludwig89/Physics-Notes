# F109 — The F92 bridge executed as a dynamical construction: the pair-sum law is derived from the update rule ($U\otimes U$ rotates the symmetric two-quantum channel by exactly $2t$), the 45°/unitarity-cap point is the unique attractor of the rule-driven phase flow (repulsion rate at the origin exactly $4I_2$), and the flavor-resolved condensation experiment lands on the constrained point with the $(A_{1g},E_g)$ decomposition measured, not posited

**Date:** 2026-06-06 - 23:30
**Status:** Partial (closing C.4's simulation build; the honest residuals are explicit) — 5/5 checks PASS. **What is constructed (audit item C.4, the F92 §6 build):** (B1) the per-tick chirality allocation is **flavor-resolved in the model's own code** — three flavor axes each execute the unit 2-vector $(\cos t_a,\sin t_a)$, $t_a=m_a\,dt$, bit-level (`ca_dirac.mass_step_1flavor_u1`, extends F92-P1); (B2, **exact**) the two-constituent one-tick step $U(t)\otimes U(t)$, $U=e^{it\sigma_1}$, has spectrum $\{e^{2it},1,1,e^{-2it}\}$ with all four eigenpairs verified symbolically — the maximally-rotating channel is the **symmetric two-quantum combination** (exactly the state the Fock $\sqrt2$ of F92-P2 normalizes) and traverses $2t$ per tick, so $m_\text{comp}=\sin2t$ by F46: **L1, previously kinematic (F73), is derived from the update rule**; (B3) the relaxational flow of the constituent phase under the sea energy with L1 kinematics, $E(t)=f(\sin2t)$, has exactly two fixed points — $t=0$ **repulsive** with exact rate $4I_2$ (measured $0.8772$ vs $4\times0.21913=0.8765$ at $L=24$) and $t=45°$ the **attractor** whose stiffness diverges toward the wall (the F46 arccos cliff; measured $3.0\to10.5\to30.4$ as $\varepsilon\to0$): every seed in $(0°,90°)$ flows to $45°$ exactly, where $y=\sqrt2\sin t_*=1$ (budget filled), $m_\text{pair}=1$ (mass peak) and $c^2=2\cot t_*=2$ (Fock) — **F92's triple saturation and F101-A0's wall-pinning emerge as the dynamical endpoint of the flow**; (B4) the flavor-resolved pairing simulation: from 1000 random seeds the projected flow of the F108-completed gap functional condenses into the constrained channel with basin fractions **lepton 49.1%**, $(0,0,0)$ 41.1%, $(1,1,1)$ 0.1%, and the **measured** (common, differential) decomposition at the lepton basin: $Q=0.666661$, $\delta=12.733°$, $\cos3\delta=0.785874$, equipartition $e/(\sqrt3\bar y)=0.999991$ ($A=\sqrt2\,\bar y$), Fock readout $c^2=2.000018$ — the F92-P5 data pin reproduced by the dynamics. Honest comparisons: minimal couplings → $(0,0,0)$ 87.9% with the lepton basin metastable at 11.7% (F101-A2/F108 realized dynamically); wall-constrained flow ($y_\tau\equiv1$, the audit's "constrained to one point") → the light flavors condense at the data point in **91.8%** of seeds. See §5.
**Script:** `tests/findings/test_F109_f92_bridge_construction.py` (~3 s)
**Results:** `test-results/F109_f92_bridge_construction.json`
**Cross-references:** [[F92-per-constituent-phase-consistency]] (the §6 residual this builds; P1/P2/P4/P5 all reappear as dynamical statements), [[F108-democratic-no-go-global-stability]] (the completion that makes the lepton point the global attractor; the metastable minimal-coupling basins), [[F101b-one-heavy-branch-fit-W]] (A0 wall-pinning, here a flow endpoint), [[F95-B-derived-C-localized]] ($I_2$, the repulsion-rate constant), [[F96-second-shell-Eg-gap-saturation]] (the gap functional), [[F73-spin0-bound-pair-scalar]] (L1, now derived from the rule), [[F82-why-saturation-composite-mass-peak]] (the energetics grounding the flow direction), [[F46-pythagorean-lattice-mass]] ($m=\sin\Omega_\text{rest}$).

---

## 1. B1/B2 — the per-tick allocation and L1 from the rule

B1 extends F92-P1 to three flavor axes: each executes its own exact unit
allocation $(\cos t_a,\sin t_a)$ — the raw material of the bridge is in the
update rule itself, flavor-resolved.

B2 is the new exact theorem. With $U(t)=\cos t\,I+i\sin t\,\sigma_1$ (the
F46 $D_k$ block at $k=0$), the two-constituent step is
$U\otimes U=e^{it(\sigma_1\otimes I+I\otimes\sigma_1)}$ and the four exact
eigenpairs are the $|\pm\pm\rangle$ basis with phases $\{2t,0,0,-2t\}$:

$$U\otimes U\;\big|{+}{+}\big\rangle=e^{2it}\,\big|{+}{+}\big\rangle,\qquad
\big|{+}{+}\big\rangle=\tfrac12(1,1,1,1)^T\ \text{(symmetric, two-quantum)}.$$

The composite rest rotation is $2t$ per tick exactly, so $m_\text{comp}=\sin2t$
(F46). The pair-sum law L1 — input kinematics in F73 — is now an output of
the update rule, and the channel that carries it is precisely the symmetric
two-quantum state whose Fock normalization ($\sqrt2$, F92-P2) feeds L2.

## 2. B3 — the phase flow: 45° as the unique attractor

Relaxational descent of the constituent phase under the sea energy with the
L1 kinematics (the dissipative mean-field image of the per-tick update;
grounded in F82's mass-peak energetics):

$$\dot t=-\frac{d}{dt}f(\sin 2t)=-2f'(m)\cos 2t .$$

Exactly two fixed points on $[0°,90°]$:

- $t=0$ (empty): **repulsive**, with exact rate $4I_2$ from
  $f'(m)=-I_2m+O(m^3)$ — measured $0.8772$ vs $0.8765$ ($0.08\%$). A bare
  flavor axis cannot stay empty under the pure sea; the contacts are what
  stabilize emptiness (consistent with F96/F101).
- $t=45°$: the **attractor**, stiffness $\propto|f'(\sin2t)|\to\infty$
  toward the wall (the arccos cliff) — all 33 seeds across $(2°,88°)$
  converge to $45°$ to machine resolution, including from the over-wrap
  side ($t>45°$, the F73 bound acting dynamically).

At the endpoint the three saturations of F92-P4 hold *exactly* as outputs:
$y=\sqrt2\sin45°=1$, $m_\text{pair}=\sin90°=1$, $c^2=2\cot45°=2$. The
identification "generation angle = constituent rest phase at 45°" is no
longer only the unique consistency point of L1+L2 — it is **where the
rule-driven flow ends up from any initial phase**.

## 3. B4 — the flavor-resolved condensation (the audit's simulation)

Projected gradient flow of $y=(y_0,y_1,y_2)$ on $[0,1]^3$ under the
F96/F101 functional with the F108 completion ($v=-0.175$, $c=0.27$,
$W^*=1.46$, couplings refit closed-form), 1000 uniform seeds:

| functional | lepton basin | $(0,0,0)$ | $(1,1,1)$ | other |
|---|---|---|---|---|
| F108-completed | **49.1%** | 41.1% | 0.1% | 9.7% |
| minimal (no completion) | 11.7% (metastable) | 87.9% | 0 | 0.4% |
| wall-constrained ($y_\tau{\equiv}1$), minimal | **91.8%** | 0 | 0.1% | 8.1% |

Measured at the lepton basin (decomposition computed from the converged
field, not imposed): $\bar y=0.42027$, $e=0.727922$, $\delta=12.7328°$,
$\cos3\delta=0.785874$, $Q=0.666661$, equipartition ratio
$e/(\sqrt3\bar y)=0.999991$ (i.e. $A=\sqrt2\,\bar y$ — the F80/F92
equipartition emerges in the channel decomposition), and the Fock readout
$c^2=2\cot\phi=2.000018$ — the same $1.9\times10^{-5}$ pin F92-P5 obtained
from the PDG masses, now produced by the simulation's endpoint.

## 4. What this changes

F92 §6's residual was: *the bridge from the per-tick chirality allocation to
the collective flavor vector is constrained to one point but not built.* The
build now exists at the mean-field level: allocation (B1) → pair channel
rotating at $2t$, symmetric, Fock-normalized (B2, exact) → phase flow whose
only interior attractor is the 45°/cap point (B3) → flavor-resolved
condensation that lands on the constrained collective vector and reproduces
the measured decomposition (B4). The audit's C.4 "simulation build, not new
theory" is executed, and it ties C.3/C.4 together: the F108 completion is
what turns the constrained point from metastable into the dominant basin.

## 5. Honest residuals (read this)

1. **Relaxational dynamics:** B3/B4 use damped gradient flow as the
   dissipative image of the per-tick update; the QCA's true real-time
   condensation (unitary + bath/measurement structure) is not built here.
2. **The angle's value:** $\delta=12.73°$ at the endpoint traces to the
   fitted couplings ($\cos3\delta=0.7859$ remains the chain's one free
   number, F93/F95) — what is measured-not-posited is the *channel*
   (one wall-pinned + $E_g$ split, never democratic), the equipartition
   ratio, the $45°$ phase, and the basins.
3. **Global landing needs F108's $(v,c)$:** with minimal couplings the
   lepton basin is metastable (11.7%) — fully consistent with
   F101-A2/F108; the self-consistent $(W,v,c)$ derivation remains the
   open item it was after F108.

## 6. Test summary (`test_F109_f92_bridge_construction.py`, 2026-06-06 - 23:27)

| Check | Statement | Result | Status |
|---|---|---|---|
| B1 | three-flavor per-tick allocation $(\cos t_a,\sin t_a)$ unit, bit-level | $<10^{-15}$ | PASS |
| B2 | $U\otimes U$ spectrum $\{e^{\pm2it},1,1\}$, all four eigenpairs; rotating channel symmetric | sympy exact | PASS |
| B3 | fixed points $\{0,45°\}$; $t{=}0$ rate $=4I_2$; cliff stiffness; 33/33 seeds $\to45°$ | $0.8772$ vs $0.8765$; $0.0$ dev | PASS |
| B4 | condensation channel + measured decomposition + honest comparisons | $Q=0.666661$, $\delta=12.733°$, eq. $0.999991$, $c^2=2.000018$ | PASS |
| V | verdict + residuals recorded | — | PASS |

**Overall 5/5 PASS** (~3 s).

## 7. Provenance

- New content: the $U\otimes U$ pair-composition theorem (L1 from the rule);
  the phase-flow fixed-point/attractor structure with the exact $4I_2$
  repulsion rate; the flavor-resolved condensation experiment with measured
  $(A_{1g},E_g)$ decomposition and basin census; the wall-constrained
  variant.
- Machinery: `ca_dirac.mass_step_1flavor_u1` (F27), `ca_bcc.bcc_dispersion`
  + F46 sea tables (F101 convention), F108 completion couplings, sympy for
  the exact parts, pure numpy elsewhere (no scipy, per CLAUDE.md caution).
- Verification: `tests/findings/test_F109_f92_bridge_construction.py`
  (2026-06-06 - 23:27, 5/5 PASS), results
  `test-results/F109_f92_bridge_construction.json`.
- Masses: PDG charged leptons.
