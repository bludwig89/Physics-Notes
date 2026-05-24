# F26 — BCC Spin Axis n̂(k) and Scalar Contamination |ψᵀψ|² = 1 − n̂_y²

**Date:** 2026-05-23  
**File:** `ca-simulation/ca_bcc.py` — `bcc_spin_axis`  
**File:** `ca-simulation/ca_maxwell.py` — `psi_scalar_bilinear_analytic`, `weyl_spin_axis_scalar_contamination`  
**Test tag:** C9  
**Track A residual:** 2.84 × 10⁻¹⁴ (formula algebraic identity)  
**Track B residual:** 6.20 × 10⁻¹⁴ (vs. np.linalg.eig eigenmode)

---

## Motivation

Finding F24 identified that the (1,0) bilinear scalar contamination $\psi^T\psi$ is
"non-zero for generic BCC eigenmodes (typical $|\psi^T\psi| \approx 0.67$)."
That value is NOT arbitrary — it is fully determined by the wavevector $\hat{k}$
through the BCC spin axis $\hat{n}(\hat{k})$.  This finding locks it down in closed form.

---

## The BCC Spin Axis

The BCC Weyl walk (Paper 1 Eq. 15, sign-corrected) has the matrix

$$U(\mathbf{k}) = u\,I_2 - i\,(\mathbf{n}\cdot\boldsymbol\sigma), \qquad u^2 + |\mathbf{n}|^2 = 1$$

with (sign = '+', $c_i = \cos(k_i/\sqrt{3})$, $s_i = \sin(k_i/\sqrt{3})$):

$$u = c_xc_yc_z + s_xs_ys_z$$

$$n_x = s_xc_yc_z - c_xs_ys_z, \quad
  n_y = -c_xs_yc_z + s_xc_ys_z, \quad
  n_z = c_xc_ys_z + s_xs_yc_z$$

The **BCC spin axis** is $\hat{n} = \mathbf{n}/\sin\omega$ where $\omega = \arccos(u)$, $\sin\omega = |\mathbf{n}|$.

The positive-helicity eigenmode $\psi_+$ satisfies $(\hat{n}\cdot\boldsymbol\sigma)\psi_+ = +\psi_+$, i.e.
$\hat{n}$ is the Bloch vector of $\psi_+$.

### Continuum limit

As $|k| \to 0$ (using $c_i \to 1$, $s_i \to k_i/\sqrt{3}$):

$$\hat{n} \;\to\; \frac{1}{|k|}(k_x,\,-k_y,\,k_z)$$

The sign flip on $k_y$ is an intrinsic chirality convention of the Bisio BCC walk.
The spin–momentum locking $|(\hat{n}\cdot\boldsymbol\sigma)\psi_+ = +\psi_+|$ is exact
at all $k$.

---

## Closed-Form |ψᵀψ| (Phase-Invariant)

Writing $\psi_+ = (\cos\frac{\Theta}{2},\, \sin\frac{\Theta}{2}\,e^{i\Phi})^T$ in the
standard Bloch basis ($\hat{n}_z = \cos\Theta$, $\hat{n}_x = \sin\Theta\cos\Phi$,
$\hat{n}_y = \sin\Theta\sin\Phi$):

$$\psi^T\psi = \cos^2\!\tfrac{\Theta}{2} + \sin^2\!\tfrac{\Theta}{2}\,e^{2i\Phi}$$

**Magnitude (phase-convention-independent):**

$$\boxed{|\psi^T\psi|^2 = 1 - \hat{n}_y^2}$$

**Proof:**

$$|\psi^T\psi|^2 = 1 - 4\cos^2\!\tfrac{\Theta}{2}\sin^2\!\tfrac{\Theta}{2}\sin^2\Phi
= 1 - \sin^2\!\Theta\,\sin^2\!\Phi = 1 - \hat{n}_y^2 \qquad \checkmark$$

**Full complex form** (Bloch-angle convention, standard phase):

$$\psi^T\psi = 1 - \frac{\hat{n}_y(\hat{n}_y - i\hat{n}_x)}{1+\hat{n}_z}
\qquad (\hat{n}_z \neq -1)$$

This rational form has subtractive cancellation near the south pole ($\hat{n}_z \approx -1$);
the implementation uses the Bloch-angle form (arccos + arctan2) for numerical stability.

---

## Continuum Limit

In the $|k| \to 0$ limit, $\hat{n}_y \to -\hat{k}_y$, so:

$$|\psi^T\psi| \;\to\; \sqrt{1-\hat{k}_y^2}$$

This is the magnitude of the projection of $\hat{k}$ onto the $xz$-plane.

| $\hat{k}$ direction | $|\psi^T\psi|$ (continuum) |
|---|---|
| Along $y$-axis | 0 (no contamination) |
| Along $x$ or $z$ | 1 (maximum contamination) |
| Random uniform average | $\langle\sqrt{1-\hat{k}_y^2}\rangle = \pi/4 \approx 0.785$ |

The BCC value of $\approx 0.69$ at $k=0.3$ is a finite-$k$ lattice correction to this limit.

---

## Scalar Contamination of the (1,0) Bilinear

The full contamination term from F24 is now completely locked down:

$$G'^i - \Lambda_{(1,0)}^{ij}G^j = -\sinh\zeta\,\hat{v}^i\,(\psi^T\psi)$$

where:
- $|\psi^T\psi| = \sqrt{1-\hat{n}_y(\hat{k})^2}$ is fully determined by $\hat{k}$
- $\hat{n}_y(\hat{k})$ is the $y$-component of `bcc_spin_axis(k/2)` — no free parameters

---

## Implementation

```python
# ca_bcc.py
def bcc_spin_axis(kx, ky, kz, sign='+'):
    """n̂(k) = n(k) / sin ω(k)  — Bloch vector of the positive-helicity eigenmode."""
    u, nx, ny, nz = _bcc_uvec(kx, ky, kz, sign=sign)
    sin_omega = np.sqrt(np.clip(1.0 - u**2, 0.0, None))
    safe = sin_omega > 0.0
    nh_x = np.where(safe, nx / np.where(safe, sin_omega, 1.0), 0.0)
    nh_y = np.where(safe, ny / np.where(safe, sin_omega, 1.0), 0.0)
    nh_z = np.where(safe, nz / np.where(safe, sin_omega, 1.0), 1.0)
    return np.stack([nh_x, nh_y, nh_z], axis=0)

# ca_maxwell.py
def psi_scalar_bilinear_analytic(kx, ky, kz, sign='+'):
    """ψ^T ψ = cos²(Θ/2) + sin²(Θ/2) e^{2iΦ}  where Θ, Φ from n̂."""
    n_hat = bcc.bcc_spin_axis(kx, ky, kz, sign=sign)
    Theta = float(np.arccos(np.clip(float(n_hat[2]), -1.0, 1.0)))
    Phi   = float(np.arctan2(float(n_hat[1]), float(n_hat[0])))
    c2 = np.cos(Theta / 2) ** 2
    s2 = np.sin(Theta / 2) ** 2
    return complex(c2 + s2 * np.exp(2j * Phi))
```

---

## Verification (C9)

| Track | Method | Residual |
|---|---|---|
| A | $\|f\|^2 + \hat{n}_y^2 - 1$, analytical formula | 2.84 × 10⁻¹⁴ |
| B | $\|\,\|f\|_{num} - \sqrt{1-\hat{n}_y^2}\,\|$, vs np.linalg.eig | 6.20 × 10⁻¹⁴ |

12 random $(\hat{k},k=0.3)$ directions; `bcc_spin_axis` evaluated at $k/2$.

---

## Significance

The scalar contamination of the (1,0) bilinear under Lorentz boosts is now fully derived:
**no free parameters** remain.  Given $(\hat{k}, \hat{v}, \zeta)$, the contamination
magnitude is $|\sinh\zeta|\cdot\sqrt{1-\hat{n}_y(\hat{k})^2}$, where $\hat{n}(\hat{k})$
is the exact BCC spin axis from `bcc_spin_axis`.

The "≈ 0.67" figure from F24 is the mean of $\sqrt{1-\hat{n}_y^2}$ over the 12 specific
random directions used in that test at $k=0.3$ — a finite-$k$ lattice value with exact
formula, not an empirical approximation.
