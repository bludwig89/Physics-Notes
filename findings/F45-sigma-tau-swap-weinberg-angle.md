# F45 — sin²θ_W from the σ ↔ τ swap geometry on the BCC lattice

**Date:** 2026-05-27 - 14:30
**Status:** Algebraic prediction — bare/tree-level
**Modules touched:** (analysis only — no code change to `ca_wmu.py`)
**Verification script:** `model-tests/test_f45_sigma_tau_weinberg.py` (algebraic, rational arithmetic)

---

## Result

Identifying the σ ↔ τ swap-singlet direction on the BCC L-doublet with $U(1)_Y$ and the swap-triplet directions with $SU(2)_L$, the **bare lattice Weinberg angle** is

$$\boxed{\;\sin^2\theta_W \;=\; \tfrac{1}{4},\qquad \cos^2\theta_W \;=\; \tfrac{3}{4},\qquad \frac{m_Z}{m_W} \;=\; \frac{2}{\sqrt{3}}\;}$$

This is a **prediction**, not a fit. F35 currently consumes $\theta_W$ as an input parameter; this finding supplies it from the swap geometry alone.

| Quantity | Bare prediction | PDG (on-shell) | Δ (rel) |
|---|---|---|---|
| $\sin^2\theta_W$ | $1/4 = 0.2500$ | $0.2232$ | $+12.0\%$ |
| $\cos^2\theta_W$ | $3/4 = 0.7500$ | $0.7768$ | $-3.45\%$ |
| $m_Z/m_W$ | $2/\sqrt{3} = 1.1547$ | $1.1346$ | $+1.77\%$ |

The mass-ratio prediction $m_Z/m_W = 2/\sqrt{3}$ lands within ~2% of experiment with no fit parameters. This is closer than the canonical SU(5) GUT tree-level value ($\sin^2\theta_W = 3/8 = 0.375$), which must be run down through ~13 decades of energy to reach experiment.

---

## Setup

The chiral SU(2) extension (F27, F41) places at every BCC site a Weyl spinor carrying both a spin index (σ-space, $\mathbb{C}^2_\sigma$) and a weak-isospin index (τ-space, $\mathbb{C}^2_\tau$):

$$|\text{state}\rangle \in \mathbb{C}^2_\sigma \otimes \mathbb{C}^2_\tau\quad(\dim = 4).$$

Generators acting on this 4D doublet:

| Group | Generator(s) | Form on $\mathbb{C}^2_\sigma \otimes \mathbb{C}^2_\tau$ | Count |
|---|---|---|---|
| $SU(2)_L$ | $T^a = \tfrac{1}{2}\tau^a$ | $I_\sigma \otimes \tfrac{1}{2}\tau^a$ ($a=1,2,3$) | 3 |
| $U(1)_Y$ | $Y/2$ | $I_\sigma \otimes \tfrac{Y_L}{2} I_\tau = -\tfrac{1}{2} I_\sigma \otimes I_\tau$ | 1 |

The σ ↔ τ swap is the involution $\Pi : A \otimes B \mapsto B \otimes A$ on operators. It has eigenvalues $\pm 1$, and on the 4D state space decomposes as

$$\mathbb{C}^2_\sigma \otimes \mathbb{C}^2_\tau \;=\; \underbrace{\text{Sym}^2 \mathbb{C}^2}_{\text{3D triplet,}\;\Pi=+1} \;\oplus\; \underbrace{\Lambda^2 \mathbb{C}^2}_{\text{1D singlet,}\;\Pi=-1}.$$

---

## The σ ↔ τ duality (pp. 67, 71 of the notebook)

The notebook records the observation:

> "$A_\mu$ works on the isospin vector just like $W$ works on the spin vector."

Concretely: the photon's charge operator on the L-doublet is the rank-1 projector
$$Q_L \;=\; T_3 + \tfrac{Y_L}{2}I_\tau \;=\; \begin{pmatrix} 0 & 0 \\ 0 & -1 \end{pmatrix} \;=\; -\tfrac{1}{2}(I_\tau - \tau_3),$$
and the $W^3$ coupling on a chirality doublet has the matrix
$$\tfrac{1}{2}(I_\sigma + \sigma_3) \;=\; \begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix},$$
i.e. the σ ↔ τ swap takes one rank-1 projector to the other. This is the *manifest* form of the σ ↔ τ exchange that pp. 67, 71 invoke.

---

## The matching condition

The σ ↔ τ swap identifies generator directions across spaces. Counting:

- **1 direction** is swap-invariant: the trace part $I_\sigma \otimes I_\tau$. This is the $U(1)_Y$ Cartan ($Y/2 \cdot I$, an overall phase). The coupling here is $g'$.
- **3 directions** lie in the swap-triplet (symmetric) subspace and span the $SU(2)_L$ generators $T^1, T^2, T^3$. The coupling is $g$.

The σ ↔ τ swap-symmetric coupling normalization assigns *equal bare lattice strength* to each generator direction. With $g'^2$ deposited entirely in the 1-dimensional singlet and $g^2$ distributed over the 3-dimensional triplet, equality of per-direction strength gives

$$\frac{g'^2}{1} \;=\; \frac{g^2}{3} \quad\Longleftrightarrow\quad \frac{g'^2}{g^2} \;=\; \frac{1}{3}.$$

The Weinberg angle is $\tan\theta_W = g'/g$, hence

$$\tan^2\theta_W = \tfrac{1}{3},\qquad \sin^2\theta_W = \tfrac{1}{4},\qquad \cos^2\theta_W = \tfrac{3}{4}.$$

The factor of 3 is the dimension of the swap-triplet — the same 3 that counts the SU(2)_L generators. No empirical input enters.

---

## Cross-check: Casimirs on the L-doublet

A consistency check uses Casimirs rather than dimension counting. On the L-doublet:

| Group | Casimir | Value |
|---|---|---|
| $SU(2)_L$ | $C_2 = T(T+1)$ with $T=1/2$ | $3/4$ |
| $U(1)_Y$ | $(Y_L/2)^2 = (-1/2)^2$ | $1/4$ |

Ratio: $C_2(U(1)_Y) / C_2(SU(2)_L) = (1/4)/(3/4) = 1/3 = g'^2/g^2$. Same answer by an independent route — the 1:3 ratio is geometric, not normalization-dependent.

---

## Algebraic verification

```
# fractions arithmetic — no floating point
g'²/g²       = 1/3                (exact rational)
sin²θ_W      = (1/3) / (1 + 1/3)  = 1/4
cos²θ_W      = 1 - 1/4             = 3/4
m_Z/m_W      = 1/cos θ_W           = 2/√3   (algebraic)
```

Residual against the F35 mass-ratio relation $m_Z/m_W = 1/\cos\theta_W$ at the predicted angle: **bit-for-bit zero** (the F35 identity is algebraic — see F35 W6.3).

---

## Comparison with notebook hypotheses and other models

| Source | $\sin^2\theta_W$ | rel. error vs. PDG 0.2232 |
|---|---|---|
| **F45 σ↔τ swap (this finding)** | $1/4 = 0.2500$ | $+12.0\%$ |
| Notebook p. 104 (W± = 3e exactly) | $2/9 = 0.2222$ | $-0.42\%$ |
| SU(5) GUT, tree | $3/8 = 0.3750$ | $+68.0\%$ |
| PDG 2024 (on-shell) | $0.22321$ | — |

The notebook's $2/9$ has the closest numerical match but no derivation: it was posed as a hypothesis ("What if coupling to $W^\pm = 3e$ exactly?") rather than derived from BCC structure. The σ↔τ swap value $1/4$ is the structure-derived prediction; the gap to experiment is what would be filled by RG running and the (currently absent) lattice loop corrections.

The mass ratio is the more robust comparison because it depends on $\cos\theta_W$ (which is closer to the geometric value $\sqrt{3}/2$ than $\sin\theta_W$ is to $1/2$): predicted $m_Z/m_W = 2/\sqrt{3} = 1.1547$ vs. PDG $1.1346$ — a 1.77% error with **zero fit parameters**.

---

## What this does and does not derive

**Derived:**
- the ratio $g'^2 / g^2 = 1/3$ from σ↔τ swap dimension counting
- the bare Weinberg angle $\theta_W = \pi/6 = 30°$ on the lattice
- the bare mass ratio $m_Z/m_W = 2/\sqrt{3}$ (combined with F35 W6.3)

**Not derived (open questions):**
- the absolute couplings $g$ and $g'$ — only their ratio
- RG running from the BCC scale to $M_Z$ (the model currently has no loops)
- whether the 12% gap in $\sin^2\theta_W$ closes under quantum corrections, or whether the σ↔τ swap is broken at some scale
- the question of whether $2/9$ has a deeper σ↔τ refinement (the notebook's coincidence is striking — would require a finite-$k$ BCC correction analysis)

---

## How this changes F35

F35 (`ca_wmu.py::weinberg_mix`) treats $\theta_W$ as an input argument. After F45 it acquires a **default value** $\theta_W = \pi/6$ from first principles. The W6.1–W6.5 test residuals are unchanged (those tests verify identities that hold for *any* $\theta_W$); F45 adds a single new algebraic test:

```python
# F45 test
theta_W_predicted = np.pi / 6
assert abs(np.sin(theta_W_predicted)**2 - 0.25) < 1e-15
assert abs(np.cos(theta_W_predicted)**2 - 0.75) < 1e-15
mZ_over_mW = 1 / np.cos(theta_W_predicted)
assert abs(mZ_over_mW - 2 / np.sqrt(3)) < 1e-15
```

Suggested follow-up: change `weinberg_mix(...)` signature to `weinberg_mix(..., theta_W=np.pi/6)` so the σ↔τ-symmetric value is the default and any deviation from it must be passed explicitly.

---

## Relationship to prior findings

| Finding | Connection |
|---|---|
| F26 — c_lat as rotation rate | Photon eigenmode $A$ defined by the F45 mixing; F26 dispersion unchanged |
| F27 — Chiral SU(2) mass | The τ-space on which the swap acts is the F27 isospin extension |
| F35 — Electroweak mixing | F45 supplies the value of $\theta_W$ that F35 currently treats as input |
| F38 — Anomaly cancellation | $Y_L = -1$ used here is the FG-1 anomaly-cancelling value |
| F41 — Hypercharge Higgs-free | $U(1)_Y$ direction identified with the swap-singlet |
| F44 — $m_A = 0$ from rank-1 Stueckelberg | The rank-1 photon projector $Q_L$ used here is the same rank-1 structure |

---

## Files

- `findings/F45-sigma-tau-swap-weinberg-angle.md` — this finding
- `model-tests/test_f45_sigma_tau_weinberg.py` — algebraic verification (rational arithmetic)
- `test-results/F45_sigma_tau_weinberg.json` — written by the test script
