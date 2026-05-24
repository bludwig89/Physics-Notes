# Finding 22 — QCA Velocity Addition: Exact Deformed Formula from the Arccos Dispersion

**Date:** 2026-05-22  
**Status:** Confirmed — Tier 1 algebraic (sympy bit-zero) + Tier 2 machine-precision numerical  
**Source:** `ca-simulation/derive_velocity_addition.py` (extension of Finding 15)

---

## Summary

Starting from the exact 2D-square QCA Dirac dispersion

$$\omega(k) = \arccos\!\bigl(\sqrt{1-m^2}\,\cos(k/\sqrt{2})\bigr), \quad c_\text{lat} = 1/\sqrt{2},$$

we derive algebraically that:

1. The **SR Lorentz boost acts exactly on the QCA 4-momentum** $(\omega, k)$.
2. The 4-momentum velocity $u_p = k c_\text{lat}^2/\omega = k/(2\omega)$ satisfies $u_p = \rho(m)\,u_g$ at $k \to 0$, where
$$\rho(m) = \frac{m}{\sqrt{1-m^2}\,\arcsin m} = 1 - 2\beta_\text{LV}(m).$$
3. This yields a **closed-form deformed velocity-addition formula**
$$u'_\text{QCA} = \frac{u_g + v_g}{1 + 2\rho^2(m)\,u_g v_g}$$
with deviation from SR
$$\delta u' = \frac{2(1-\rho^2)\,u\,v\,(u+v)}{(1+2\rho^2 u v)(1+2uv)} \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v).$$

Since $\beta_\text{LV}(m) < 0$ for all $m \in (0,1)$, the QCA **always predicts less velocity addition than SR at finite mass**, consistent with the time-dilation over-dilation in Finding 15.

---

## Derivation

### Step 1 — The ρ ratio

Expanding $\omega(K)$ with $K = k/\sqrt{2}$ at $K \to 0$:

$$\omega \approx \arcsin m + \frac{\sqrt{1-m^2}}{2m}\,K^2 + O(K^4)$$

The group velocity is $u_g = d\omega/dk = (1/\sqrt{2})\,d\omega/dK$; at $K \to 0$:

$$u_g \approx \frac{\sqrt{1-m^2}}{m}\,k/2 \quad (\text{leading term in }k)$$

The 4-momentum velocity is $u_p = k/(2\omega) \approx k/(2\arcsin m)$ at $k \to 0$.  Therefore

$$\rho \equiv \lim_{k\to 0}\frac{u_p}{u_g} = \frac{m/\arcsin m}{\sqrt{1-m^2}} = \frac{m}{\sqrt{1-m^2}\,\arcsin m}.$$

Confirmed symbolically via sympy with residual = **0** (bit-exact).

### Step 2 — Deformed velocity-addition formula

The SR Lorentz boost $(v_\text{frame})$ maps the 4-momentum as

$$k' = \gamma(k - 2v\,\omega), \quad \omega' = \gamma(\omega - v\,k), \quad \gamma = (1-2v^2)^{-1/2}.$$

Since $u_p = \rho\,u_g$, both $u_p$ and $v_p = \rho\,v_g$ obey SR velocity addition exactly:

$$u'_p = \frac{u_p + v_p}{1 + 2\,u_p\,v_p} = \frac{\rho(u+v)}{1 + 2\rho^2 uv}.$$

Converting back to group velocity via $u'_g = u'_p/\rho$ yields the deformed formula.

### Step 3 — LV deviation

$$\delta u' = u'_\text{QCA} - u'_\text{SR} = \frac{2(1-\rho^2)\,u\,v\,(u+v)}{(1+2\rho^2 uv)(1+2uv)}.$$

Confirmed symbolically (sympy residual = **0**). Leading-order expansion:

$$2(1-\rho^2) = 2(1-\rho)(1+\rho) \approx -4\beta_\text{LV}(m)\cdot 2 = 8\beta_\text{LV}(m) \quad (\rho \approx 1 \text{ at small }m)$$

$$\Rightarrow \delta u' \approx 8\beta_\text{LV}(m)\cdot u\cdot v\cdot(u+v), \quad \beta_\text{LV}(m) \approx -\frac{m^2}{6} \text{ for small }m.$$

---

## Key results

| Result | Status |
|---|---|
| $\rho(m) = m/(\sqrt{1-m^2}\arcsin m) = 1-2\beta_\text{LV}(m)$ — sympy zero | **Tier 1 exact** |
| $\delta u'$ closed form — sympy zero residual | **Tier 1 exact** |
| Massless limit $m\to 0$ ($\rho\to 1$): $\delta u' = 0$ — SR recovered | **Tier 1 exact** |
| $\rho$ formula vs numerical $u_p/u_g$ at $k=10^{-6}$, max residual $3.4\times 10^{-14}$ across $m \in [0.05,0.90]$ | **Tier 2 machine precision** |
| $8\beta_\text{LV} \approx -4m^2/3$ (leading small-$m$ approximation) | **Tier 1 exact (symbolic)** |

---

## Numerical summary

**Step 2 — Deformed formula scan (algebraic):**

| $m$ | $u$ | $v$ | $u'_\text{QCA}$ | $u'_\text{SR}$ | $\delta u'$ | rel(lead) |
|---|---|---|---|---|---|---|
| 0.10 | 0.01 | 0.01 | 0.0199960 | 0.0199960 | $-2.69\times 10^{-8}$ | 1.3e-3 |
| 0.10 | 0.10 | 0.05 | 0.1485050 | 0.1485149 | $-9.89\times 10^{-6}$ | 1.8e-2 |
| 0.50 | 0.10 | 0.10 | 0.1952520 | 0.1960784 | $-8.26\times 10^{-4}$ | 6.2e-3 |

**Step 3 — Continuum-limit ρ check:**

| $m$ | $\rho_\text{analytic}$ | $u_p/u_g$ (num.) | residual |
|---|---|---|---|
| 0.05 | 1.0008348643 | 1.0008348643 | 2.2e-16 |
| 0.50 | 1.1026577908 | 1.1026577908 | 6.6e-15 |
| 0.90 | 1.8438987463 | 1.8438987463 | 3.4e-14 |

**Step 4 — Group-velocity boost structure at finite k:**

At fixed $v_2 = 0.001$ and $m = 0.10$, the total deviation of the lattice QCA boost from SR is:

$$d_\text{qca} = v_g^\text{boost} - u'_\text{SR} \approx v_2\!\left(1 - \frac{1}{\rho(m)}\right) \approx v_2\cdot(-2\beta_\text{LV}) = 3.35\times 10^{-6}$$

This is **k-independent at small k** — it is not a finite-k effect but the fundamental LV mismatch between the lattice group velocity and the SR-transformed group velocity. The correct SR-compatible kinematic observable is the 4-momentum velocity $u_p$, not the group velocity $u_g$.

---

## Physical interpretation

The group velocity $u_g = d\omega/dk$ does not transform as a relativistic velocity under Lorentz boosts of the 4-momentum. The lattice 4-momentum velocity $u_p = k c_\text{lat}^2/\omega$ does. Their ratio $\rho(m) \ne 1$ for $m > 0$ is the same coefficient that produces the SR-2 time-dilation LV term (Finding 15).

This is not a failure of the QCA's Lorentz structure — it is a consequence of the massive dispersion being nonlinear. In the massless limit ($m \to 0$, $\rho \to 1$) SR is recovered exactly. At finite mass, the deformed formula $u'_\text{QCA} = (u+v)/(1+2\rho^2 uv)$ is the lattice-exact analogue of SR velocity addition for group velocities.

---

## Connections

- **Finding 15**: $\beta_\text{LV}(m) = \tfrac12(1-\rho(m))$ — same coefficient appears in SR-2 time-dilation gap and here in velocity addition.
- **Small-$m$ expansion**: $8\beta_\text{LV} \approx -4m^2/3$; velocity-addition LV coefficient $= -4m^2/3$ to leading order.
- **Script**: `ca-simulation/derive_velocity_addition.py` — Steps 1–5 all pass, run in < 30 s.
