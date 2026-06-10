# F81 — Why 45°: the charged-lepton equipartition is the phase saturation of a two-constituent pair, and Q reads off N = 2

**Date:** 2026-06-02 - 12:15
**Status:** Partial — 4/4 checks PASS + 1 recorded residual. **This answers the "why 45°" of F80 at the level of the *value*:** a two-constituent (Cooper) pair shares the $\pi/2$ stable phase budget equally, $\pi/4=45°$ per member, giving $Q=2/3$ exactly; and the observed lepton $Q$ **reads off the constituent number $N=2$**. The residual is now a single sharper question — *why the pair sits at its phase saturation* — not the value itself.
**Script:** `tests/findings/test_F81_45deg_pair_saturation.py` (<1 s)
**Results:** `test-results/F81_45deg_pair_saturation.json`
**Cross-references:** [[F80-one-45deg-em-saturation-koide]] (the open question this closes; the $Q(\phi)=1/(3\cos^2\phi)$ map), [[F69-paired-spinor-photon]] (the pair-phase-sum rule), [[F73-spin0-bound-pair-scalar]] (the $\pi/2$ stability saturation; the spin-0 singlet), [[F74-two-constituent-bound-state-binding]] / [[F77-njl-gap-rpa-selfconsistent]] (the criticality / threshold-state language), [[F78-koide-amplitude-from-cooper-pair]] ($\sqrt m$ as the constituent amplitude), [[F82-why-saturation-composite-mass-peak]] (answers the 'why at saturation' residual below: the composite mass peaks at $45°$, so any binding lands there).

---

## 1. The question

F80 reduced the charged-lepton hierarchy to one number — the amplitude
$\sqrt m$ sits at $\phi=45°$ to the democratic axis ($Q=2/3$) — but could not say
*why 45°*. The rotation is a full $45°$ from democracy, and perturbative
electromagnetism ($\alpha/\pi\approx0.13°$) is ~$340\times$ too weak to drive it
(F80-D5). This finding derives the *value* $45°$ from the model's own
pair-phase rules.

---

## 2. The derivation

Each step is a rule already established in the project:

| step | statement | source |
|---|---|---|
| (a) | the charged lepton is a bound **pair** of constituents | F73 |
| (b) | the generation angle $\phi$ (the angle of $\sqrt m$ off the democratic axis, F80) is a **per-constituent rotation** | *new identification* |
| (c) | a bound pair's total phase is the **sum** of the constituent phases: total $=N\phi$ for $N$ constituents | F69 |
| (d) | a stable composite requires total phase $\le\pi/2$ (beyond it the composite mass $\sin(\text{phase})$ turns over → over-wrap instability) | F73 |
| (e) | the physical state sits at **saturation** (maximal stable binding / criticality) ⟹ $N\phi=\pi/2$ ⟹ $\phi=\dfrac{\pi}{2N}$ | F74-style |
| (f) | $Q(\phi)=\dfrac{1}{3\cos^2\phi}$ | F80 |

Combining (e)+(f):

$$\boxed{\;Q_N=\dfrac{1}{3\cos^2\!\big(\tfrac{\pi}{2N}\big)}\;}$$

For the **pair, $N=2$**: $\phi=\pi/4=45°$ *exactly*, and $Q=\dfrac{1}{3\cos^2 45°}=\dfrac{1}{3\cdot\frac12}=\dfrac23$ *exactly*.

**Why 45° in one line:** the pair *halves* the $\pi/2$ stable-phase budget — each
of the two constituents carries $\pi/4=45°$.

---

## 3. Q reads off the constituent number (E1, E2)

$Q_N$ is a strictly decreasing function of $N$:

| $N$ | $\phi=\pi/2N$ | $Q_N$ | |
|---|---|---|---|
| 1 | $90°$ | $\infty$ | (no pair; no stable saturation) |
| **2** | $\mathbf{45°}$ | $\mathbf{2/3=0.66667}$ | **observed: $0.66666$** |
| 3 | $30°$ | $4/9=0.44444$ | |
| 4 | $22.5°$ | $0.39052$ | |
| $\infty$ | $0°$ | $1/3$ | (democratic limit) |

The integer $N$ that matches the measured $Q_\text{lepton}=0.666661$ is **uniquely
$N=2$** (residual $6\times10^{-6}$; $N=3$ misses by $0.22$). So **$Q=2/3$ is the
signature of the two-constituent (Cooper-pair) structure** — the pairing premise
of F73 is now *read directly off the charged-lepton mass ratios*, with no extra
input. A three-body bound state would sit at $Q=4/9$; a single particle has no
such equipartition. The data say "two."

---

## 4. The three 45°'s are one (E3, E4)

At $N=2$ each pair member sits at $(\cos45°,\sin45°)=(1/\sqrt2,1/\sqrt2)$. This is
simultaneously:

- the **F73 rest-mass cap** $\arcsin(1/\sqrt2)=45°$ (the constituent's
  rest-rotation at the stability edge, where rest $=$ kinetic),
- the **Koide/generation equipartition** $\phi=45°$ (common $=$ differential, F80),
- the **spin-singlet weight** $1/\sqrt2$ of the Cooper pair $(\!\uparrow\downarrow-\downarrow\uparrow)/\sqrt2$.

They coincide because all three are *the per-constituent half of a $\pi/2$ pair
phase*: $N\phi_N=\pi/2$ with the budget split equally among the $N$ members
(verified for all $N$, E4), and for the pair that half is $45°$. F80's "two
45°'s are the same SO(2) rotation" now has its mechanism: **the pair halves the
$\pi/2$ budget, and 45° is that half.** The Cooper-pair singlet's own $1/\sqrt2$
(F80's conjecture) is the same statement — the singlet is the two-member
equal split.

---

## 5. Honest residual (E5)

**Answered (the value):** *why 45°* — a two-constituent pair shares the $\pi/2$
stable phase budget equally, $\pi/4$ each. The number $2/3$ is now derived, and
the constituent count $N=2$ is read off the data.

**Two load-bearing inputs remain:**

1. **The identification (b)** — that the generation-space angle $\phi$ is a
   per-constituent rotation obeying the F69 pair-phase-sum rule. This is a
   structural hypothesis, but it is strongly supported: it predicts $Q_N$ as a
   one-integer family and the data land on $N=2$ to $10^{-5}$.
2. **Sitting at saturation (e)** — that the lepton occupies the critical edge
   ($N\phi=\pi/2$) rather than a sub-saturated angle. Perturbative EM does not
   force this (F80-D5: $340\times$ too weak); it is a genuine *criticality*
   assumption. The selection of *which sector* is at criticality is still the
   EM/charge rule of F80 (only charged leptons; quarks QCD-dominated, neutrinos
   neutral).

**Net:** the open problem has shrunk from "why does the angle equal $45°$?" to
"why does the charged-lepton pair sit at its phase-saturation edge?" — a single
criticality question. The $45°$, the factor $2/3$, the constituent number
$N=2$, and the unification of the three $45°$'s are all now derived/observed
consequences of the two-constituent structure.

---

## 6. A falsifiable corollary

$Q_N=1/(3\cos^2(\pi/2N))$ ties a sector's **constituent number** to its Koide
ratio at saturation. Charged leptons: $Q=2/3\Rightarrow N=2$. This predicts that
any other sector that is a *clean two-body bound pair at saturation* must also
sit at $2/3$, and that sectors which are not (quarks: colour-confined,
QCD-dominated, $Q_\text{up}=0.85$, $Q_\text{down}=0.73$; neutrinos: neutral,
Majorana/seesaw, unpinned) need not. The relation is sharp enough to be wrong —
which is the point.

---

## 7. Test summary (`test_F81_45deg_pair_saturation.py`, 2026-06-02 - 12:15)

| Check | Statement | Result | Status |
|---|---|---|---|
| E1 | $Q_N=1/(3\cos^2(\pi/2N))$; $N{=}2\to2/3$, $N{\to}\infty\to1/3$ | exact | PASS |
| E2 | data select $N=2$ | best $N=2$, residual $6\times10^{-6}$ ($N{=}3$ off $0.22$) | PASS |
| E3 | pair member $=(1/\sqrt2,1/\sqrt2)=$ singlet $=$ F73 cap | identical $45°$ | PASS |
| E4 | phase-budget equipartition $N\phi_N=\pi/2$ | holds $\forall N$ | PASS |
| E5 | honest residual (recorded) | "why at saturation" remains | (info) |

**Overall 4/4 PASS** (+ recorded residual).

---

## 8. Provenance

- Closes the value-level part of the open question stated at the end of F80;
  the per-constituent identification (b), the $Q_N$ family, and the $N=2$
  readout are new.
- Verification: `tests/findings/test_F81_45deg_pair_saturation.py`
  (2026-06-02 - 12:15, 4/4 PASS + residual), results
  `test-results/F81_45deg_pair_saturation.json`.
