# F36 — Yang-Mills Back-Reaction and Massive W Dispersion (Proca)

**2026-05-24 - 00:00**

## Summary

Phase 7 of the WMU roadmap implements and verifies two coupled results:

1. **Fermion-to-gauge-field back-reaction** via the linearized Yang-Mills source term $D_\mu F^{a,\mu\nu} = g J^{a,\nu}$, where $J^a$ is the left-handed isospin current of the $(ν, e)$ doublet.
2. **Massive W (Proca) propagation**, replacing the massless BCC dispersion $\Omega_\text{even}(k)$ with the full Proca dispersion $\omega_\text{eff}(k) = \sqrt{m_W^2 + \Omega_\text{even}^2(k)}$.

Both results are verified to machine precision on a $16^3$ BCC lattice.

---

## Finding WB-J: Fermion Isospin Current

The left-handed SU(2)$_L$ isospin current density is:

$$J^a(x) = \psi_L^\dagger(x)\,\frac{\tau^a}{2}\,\psi_L(x)$$

For the $(f_\nu, f_e)$ upper Weyl components (lower components $g$ are right-handed and do not couple — confirmed in F34):

$$J^1(x) = \mathrm{Re}(f_\nu^*(x)\,f_e(x))$$
$$J^2(x) = \mathrm{Im}(f_\nu^*(x)\,f_e(x))$$
$$J^3(x) = \tfrac{1}{2}\bigl(|f_\nu(x)|^2 - |f_e(x)|^2\bigr)$$

**Algebraic exactness:**

| State | Expected | Residual |
|-------|----------|---------|
| Pure $\nu$: $f_e = 0$ | $J^1=J^2=0$, $J^3=|f_\nu|^2/2$ | $0.0$ (exact) |
| Equal mix $f_\nu = f_e = \psi/\sqrt{2}$ | $J^1=|\psi|^2/2$, $J^2=J^3=0$ | $\leq 1.8\times10^{-15}$ |

The pure-$\nu$ case is exact because $f_e = 0$ forces $J^1 = J^2 = 0$ and $J^3 = |f_\nu|^2/2$ by definition with no floating-point operations.

---

## Finding WB-R: Linearized Back-Reaction

The Yang-Mills equation with source, linearized around a background, reads:

$$\partial_t \hat{E}^a(k) = \Omega(k)\,\hat{B}^a(k) + g\,\hat{J}^a(k)$$

The implementation splits this as:

1. **Free rotation** (one tick of F26): $(E^a, B^a) \to R_{\Omega}(k)\cdot(E^a, B^a)$
2. **Source kick** (real-space): $E^a \mathrel{+}= g\,J^a\,dt$

**Diagonal coupling structure:** Since $\tau^a$ are diagonal in isospin index $a$, the current $J^3$ drives only $W^3$, and $J^1, J^2$ drive only $W^1, W^2$ respectively.

**Verification (WB.3):**

- Starting from $E_W = B_W = 0$, one sourced step with pure $J^3$ source:  
  $\delta E_W^3 = g\,J^3\,dt$ **exactly** (residual $= 0.0$, algebraic)
- After 10 steps: $W^1 = W^2 = 0$ **exactly** (no cross-isospin leakage, residual $= 0.0$)
- $W^3 \neq 0$ (source has driven it non-zero ✓)

---

## Finding WB-M: Massive W (Proca) Dispersion

The BCC lattice Proca dispersion relation for a massive gauge boson is:

$$\omega^2(k) = m_W^2 + \Omega_\text{even}^2(k)$$

where $\Omega_\text{even}(k) = \omega_+(k/2) + \omega_-(k/2)$ is the symmetrized BCC dispersion from F26.

**Continuum limit** ($k \to 0$, $\Omega_\text{even} \to 2c_\text{lat}|k|$):

$$\omega^2 \to m_W^2 + 4c_\text{lat}^2\,|k|^2$$

This is the Klein-Gordon / Proca dispersion. The factor of 4 vs. the standard $c^2|k|^2$ arises from the double-BCC-hop structure of the F26 rotation; it rescales the lattice speed of light $c_\text{lat}$ by 2.

**Implementation:** The massive propagation step replaces $\Omega_\text{even}(k) \to \omega_\text{eff}(k)$ in the rotation matrix:

$$\begin{pmatrix} E^a(k,t+dt) \\ B^a(k,t+dt) \end{pmatrix} = \begin{pmatrix} \cos(\omega_\text{eff} dt) & \sin(\omega_\text{eff} dt) \\ -\sin(\omega_\text{eff} dt) & \cos(\omega_\text{eff} dt) \end{pmatrix} \begin{pmatrix} E^a(k,t) \\ B^a(k,t) \end{pmatrix}$$

**Verification against closed-form prediction** $C_n(k) = C_0(k)\,e^{-i\,\omega_\text{eff}(k)\,n}$ where $C = \hat{E}_k + i\,\hat{B}_k$:

| $m_W$ | Max relative error | Pass |
|-------|-------------------|------|
| 0.1 | $1.4\times10^{-13}$ | ✓ |
| 0.3 | $8.9\times10^{-14}$ | ✓ |
| 0.8 | $8.2\times10^{-14}$ | ✓ |

All residuals are at machine-precision round-off level for double arithmetic.

**Massless limit (WB.5):** At $m_W = 0$, $dt = 1$, the massive step reduces **exactly** to the free F26 step:

$$E_\text{err} = 0.0,\quad B_\text{err} = 0.0 \quad\text{(algebraic exact)}$$

---

## Test Results

| Test | Description | Residual | Result |
|------|-------------|---------|--------|
| WB.1 | Current pure-$\nu$ state | $0.0$ | PASS |
| WB.2 | Current equal-mix state | $\leq 1.8\times10^{-15}$ | PASS |
| WB.3 | Back-reaction diagonal coupling | $0.0$ | PASS |
| WB.4 | Massive Proca dispersion (3 masses) | $\leq 1.4\times10^{-13}$ | PASS |
| WB.5 | Massless limit exactness | $0.0$ | PASS |

**5/5 PASS** — all residuals at or below double-precision round-off.

---

## Physical Significance

- The back-reaction closes the loop between the fermionic and bosonic sectors of the BCC lattice QFT. The fermion current sourcing the W field is the CA analogue of the Yang-Mills covariant current conservation law.
- The Proca dispersion on the BCC lattice confirms that mass modifies only the $k=0$ gap, not the high-$k$ structure — consistent with the CA interpretation that lattice geometry sets UV behaviour and mass sets IR behaviour.
- The massless limit being exactly zero (not just small) is a non-trivial check: it confirms the massive implementation is a strict generalization of the massless one, with no spurious offset or rounding in the $m_W \to 0$ limit.
