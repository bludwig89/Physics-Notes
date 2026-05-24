# Finding 25 — Real-rotation formula holds to machine precision; Maxwell curl holds only to O(k)

**Date:** 2026-05-23  
**Status:** Confirmed — machine precision (real-rotation), O(k) coefficient exact (Maxwell gap)  
**Source:** `ca-simulation/ca_maxwell.py::real_rotation_vs_maxwell_curl` and `real_rotation_k_scan`

---

## Context

Finding 23 established that the composite-photon curl residual is π/2 phase-locked and algebraically exact at coefficient $c_\text{lat}/\sqrt{2}$.  The root cause: the bilinear evolution is a **discrete real rotation** of the $(E_G, B_G)$ field pair, while the Maxwell curl equation is the **continuous-time imaginary-driven limit** of that rotation.

This finding directly tests the proposed hypothesis:
> *Assume the Maxwell curl equation is incorrect theory and $c_\text{lat}$ is correct — what is the impact?*

---

## The two predictions under test

**Real-rotation prediction** (derived from bilinear $G_T(t) = e^{-i\Omega t} G_T(0)$, writing $G_T = A + iC$, $E = 2|n|A$, $B = 2|n|C$):

$$\mathbf{E}(t+1) = \cos\Omega\;\mathbf{E}(t) + \sin\Omega\;\mathbf{B}(t)$$
$$\mathbf{B}(t+1) = -\sin\Omega\;\mathbf{E}(t) + \cos\Omega\;\mathbf{B}(t)$$

with $\Omega = 2\omega(k/2)$ the composite-photon phase per tick.

**Maxwell curl prediction** (continuous-time, $\Delta t = 1$ approximation):

$$\mathbf{E}(t+1) \approx \mathbf{E}(t) + i\,(2\mathbf{n}_{k/2}) \times \mathbf{B}(t)$$
$$\mathbf{B}(t+1) \approx \mathbf{B}(t) - i\,(2\mathbf{n}_{k/2}) \times \mathbf{E}(t)$$

---

## Results

**Single k = 0.05 test (12 random BCC directions):**

| Prediction | E residual | B residual |
|---|---|---|
| Real-rotation (cos/sin) | $2.0 \times 10^{-16}$ | $3.3 \times 10^{-16}$ |
| Maxwell curl | $2.0 \times 10^{-2}$ | $2.0 \times 10^{-2}$ |

Real-rotation holds at **machine precision**. Maxwell curl deviates by **5 orders of magnitude** more.

**k-scan (curl/k and rot/k across a decade):**

| $k$ | curl\_E/k | rot\_E/k | $c_\text{lat}/\sqrt{2}$ |
|---|---|---|---|
| 0.001 | 0.408256 | $1.2 \times 10^{-13}$ | 0.408248 |
| 0.002 | 0.408264 | $2.1 \times 10^{-13}$ | 0.408248 |
| 0.005 | 0.408286 | $2.9 \times 10^{-14}$ | 0.408248 |
| 0.010 | 0.408324 | $1.0 \times 10^{-14}$ | 0.408248 |
| 0.020 | 0.408398 | $1.0 \times 10^{-14}$ | 0.408248 |
| 0.050 | 0.408611 | $4.4 \times 10^{-15}$ | 0.408248 |
| 0.100 | 0.408938 | $1.2 \times 10^{-15}$ | 0.408248 |

- **curl\_E/k** → $c_\text{lat}/\sqrt{2} = 1/\sqrt{6} \approx 0.408248$ (flat, confirming F23).
- **rot\_E/k** → 0 at all $k$ (numerical noise only, no systematic growth).

---

## Derivation of the real-rotation formula

Starting from $G_T(t) = e^{-i\Omega t} G_T(0)$ and writing $G_T(0) = A + iC$ with $A, C \in \mathbb{R}^3$:

$$E(t) = 2|n|\,\mathrm{Re}(G_T(t)) = 2|n|(A\cos\Omega t + C\sin\Omega t)$$
$$B(t) = 2|n|\,\mathrm{Im}(G_T(t)) = 2|n|(-A\sin\Omega t + C\cos\Omega t)$$

One-step advance:

$$E(t+1) = 2|n|(A\cos\Omega(t+1) + C\sin\Omega(t+1))$$
$$= \cos\Omega\cdot 2|n|(A\cos\Omega t + C\sin\Omega t) + \sin\Omega\cdot 2|n|(-A\sin\Omega t + C\cos\Omega t)$$

Wait — we need $+\sin\Omega\cdot B(t)$, not $-\sin\Omega\cdot\text{something}$. Let me expand carefully:

$$A\cos\Omega(t+1) + C\sin\Omega(t+1)$$
$$= A(\cos\Omega t\cos\Omega - \sin\Omega t\sin\Omega) + C(\sin\Omega t\cos\Omega + \cos\Omega t\sin\Omega)$$
$$= \cos\Omega(A\cos\Omega t + C\sin\Omega t) + \sin\Omega(-A\sin\Omega t + C\cos\Omega t)$$
$$= \cos\Omega\cdot\frac{E(t)}{2|n|} + \sin\Omega\cdot\frac{B(t)}{2|n|}$$

Therefore:
$$\boxed{E(t+1) = \cos\Omega\;E(t) + \sin\Omega\;B(t)}$$

This is an exact identity — no small-$k$ approximation required. It holds for any $\Omega$ and any initial $G_T(0)$.

---

## Physical interpretation

**If the Maxwell curl equation is wrong theory at the Planck scale:**

1. The real-rotation formula is the correct discrete-time electromagnetic law.  The bilinear evolution is a rigid rotation of the $(E, B)$ pair at rate $\Omega = 2\omega(k/2) \approx c_\text{lat}|k|$ per tick.

2. **$c_\text{lat}$ is preserved** — it sets the rotation rate $\Omega = c_\text{lat}|k|$ (at small $k$), which is exactly the Maxwell wave speed.

3. **Maxwell is the $\Delta t \to 0$ limit** — as the tick rate increases:
   $$\frac{E(t+\Delta t) - E(t)}{\Delta t} \to \frac{d E}{d t} = \Omega\; B = c_\text{lat}|k|\;B$$
   which in position space is $\partial_t E = c_\text{lat}\,\nabla \times B$ — the Maxwell curl equation.

4. **The O(k) curl residual is a prediction, not a failure.** Its coefficient $c_\text{lat}/\sqrt{2}$ (exact, F23) is the leading Planck-scale signature of the discrete real rotation.

5. **Falsifiable:** at Planck-scale frequencies $\Omega \sim \pi/2$, the real-rotation and Maxwell curl predictions differ by:
$$\Delta E = (\cos\Omega - 1)E + (\sin\Omega - \Omega)B \approx -\frac{\Omega^2}{2}E + \mathcal{O}(\Omega^3)$$
This is a quadratic-in-frequency correction to the curl law.

---

## What is not changed by this assumption

| Property | Status |
|---|---|
| $c_\text{lat} = 1/\sqrt{d}$ | ✓ unchanged — sets rotation rate |
| Transversality $k\cdot E = k\cdot B = 0$ | ✓ exact (F21) |
| Energy conservation $\|E\|^2 + c^2\|B\|^2$ | ✓ machine precision (F17) |
| Maxwell equations in continuum limit | ✓ recovered as $\Delta t \to 0$ |
| Paper 1 bilinear construction | ✓ fully valid — it generates the real rotation |

---

## Test function

`ca_maxwell.py::real_rotation_vs_maxwell_curl(k_mag, n_dirs, seed)`  
`ca_maxwell.py::real_rotation_k_scan(k_values, n_dirs, seed)`

Added to Exactness Inventory Tier 1 #51 (real-rotation) and Tier 2 #15 (k-scan slope).

---

## Cross-references

- [[F23-smearing-ruled-out-curl-residual-is-phase-locked]]: established the π/2 phase lock
- [[F21-curl-residual-geometry-independence]]: coefficient is $c_\text{lat}/\sqrt{2}$
- [[F17-poynting-energy-conservation]]: energy conservation exact under bilinear propagation
- Exactness Inventory #49 ($c_\text{lat}/\sqrt{2}$ coefficient), #51 (this result)
