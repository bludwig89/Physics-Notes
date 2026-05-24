# F24 — Weyl SL(2,ℂ) Boost: Lorentz 4-Current Covariance

**Date:** 2026-05-23  
**File:** `ca-simulation/ca_maxwell.py` — `sl2c_boost`, `weyl_sl2c_4current_covariance`  
**Test tag:** C7  
**Residual:** 3.71 × 10⁻¹⁶ (machine precision)

---

## Statement

The SL(2,ℂ) pure-boost matrix

$$A = \exp\!\left(-\tfrac{\zeta}{2}\,\boldsymbol\sigma\cdot\hat{v}\right)
    = \cosh\tfrac{\zeta}{2}\,I_2 - \sinh\tfrac{\zeta}{2}\,(\boldsymbol\sigma\cdot\hat{v})$$

correctly induces the defining SL(2,ℂ) → SO(1,3) homomorphism on the
Weyl 4-current.  For any Weyl spinor $\psi$ and boost $({\hat v},\zeta)$:

$$j'^\mu \;\equiv\; (A\psi)^\dagger\,\bar\sigma^\mu\,(A\psi)
  \;=\; \Lambda^\mu{}_\nu\,j^\nu, \qquad
  j^\mu = \psi^\dagger\bar\sigma^\mu\psi$$

where $\bar\sigma^0 = I_2$, $\bar\sigma^i = \sigma^i$, and $\Lambda$ is the 4×4
Lorentz boost matrix with rapidity $\zeta$ along $\hat{v}$.

Verified across 12 random $(\hat k, \hat v)$ pairs at $|k|=0.3$, $v/c=0.6$ using
BCC eigenmodes; max relative residual $|j' - \Lambda j|/|\Lambda j| = 3.71\times 10^{-16}$.

---

## Representation-theory context

The bilinear $G^i = \psi^T\sigma^i\psi$ of Paper 1 Eq. 33 uses a **transpose**,
not a dagger.  Under $\psi\to A\psi$ it transforms as

$$G'^i = \psi^T A^T\sigma^i A\,\psi
  \;=\; \Lambda_{(1,0)}^{ij}\,G^j - \sinh\zeta\,\hat v^i\,(\psi^T\psi)$$

The second term is a **(0,0) scalar contamination** pointing along $\hat v$.
It is non-zero for generic BCC eigenmodes (typical $|\psi^T\psi|\approx 0.67$)
and survives transverse projection onto $\hat k'$ whenever $\hat v\not\perp\hat k'$.

Therefore $G^i = \psi^T\sigma^i\psi$ lies in the **self-dual (1,0)** Lorentz
irrep — distinct from the **(½,½)** Maxwell-field irrep on which Mohr's V6
boost operates.  Direct comparison of the (1,0) bilinear to the V6 result is
ill-posed in general.

The correct (½,½) object at the spinor level is the Weyl 4-current
$j^\mu = (\psi^\dagger\psi,\,\psi^\dagger\boldsymbol\sigma\psi)$,
which IS directly comparable to V6 through the 4-vector boost $\Lambda$,
and is verified here to machine precision.

---

## Key identity (verified)

For a z-boost $A = \operatorname{diag}(e^{-\zeta/2}, e^{\zeta/2})$:

$$A^\dagger\,\sigma_z\,A = \cosh\zeta\;\sigma_z - \sinh\zeta\;I_2$$

Contracting with $\psi^\dagger(\cdots)\psi$:

$$j'^z = \cosh\zeta\;j^z - \sinh\zeta\;j^0 \qquad \checkmark$$

which is exactly the $z$-component of a Lorentz 4-vector boost.

---

## Implementation

```python
def sl2c_boost(v_hat_c, zeta):
    v = np.asarray(v_hat_c, dtype=float)
    sigma_v = v[0]*_S_X + v[1]*_S_Y + v[2]*_S_Z
    ch = np.cosh(float(zeta)/2); sh = np.sinh(float(zeta)/2)
    return ch*np.eye(2, dtype=complex) - sh*sigma_v

def weyl_sl2c_4current_covariance(k_mag=0.3, v_mag=0.6, n_dirs=12, seed=7):
    # For each (k̂, v̂): compute j = (ψ†ψ, ψ†σψ), boost with Λ,
    # compare to j' = ((Aψ)†(Aψ), (Aψ)†σ(Aψ)).
    # Returns max |j' - Λj| / |Λj|.
```

---

## Significance

This closes the Lorentz-covariance loop at the spinor level: the 2×2 SL(2,ℂ)
boost matrix $A$ is the exact double-cover of the 4×4 Lorentz boost $\Lambda$.
The residual of $3.71\times 10^{-16}$ is at the IEEE-754 double-precision floor,
confirming no implementation errors in `sl2c_boost`.

The (1,0) bilinear structure of the composite photon is a separate open question:
the correct Lorentz covariance of $G = \psi^T\sigma\psi$ under boosts involves
the (1,0) representation and its scalar contamination term, which is the subject
of future study.
