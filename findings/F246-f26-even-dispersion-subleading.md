# F246 — Subleading coefficients of the F26 even-rotation curl law: closed form + exact even-power vanishing (L2)

**Date:** 2026-07-15 - 19:40
**Status:** Confirmed — closes open-derivation **L2** (`open-derivations-prompts-v2.md` Part 3; exactness-inventory "not-yet-met" #3 reframed / Tier-3 #5). The subleading coefficient of the F26 exact real-rotation EM propagator (`ca_wmu._f26_rotation_step`) is derived in closed form and verified to $4\times10^{-19}$. A stronger structural result comes for free: **all even-power dispersion corrections vanish identically**, so the leading Lorentz-violation signature is the CPT-even cubic $\lvert k\rvert^3$ term. Positive result, not a no-go.
**Modules:** `ca-simulation/derive_f26_dispersion.py` (new; uses the `ca_wmu._f26_rotation_step` / `ca_bcc._bcc_uvec` dispersion, not modified)
**Cross-references:** [[F245-curl-subleading-closed-forms]] (L1 — the *bilinear-construction* curl residual, whose leading $1/\sqrt6=c_\text{lat}/\sqrt2$ and single-chirality subleading are a distinct, larger discretisation artifact), and Finding 25/F26 (the exact real-rotation law, Tier-1 #51, that this expands).

---

## What was open

The F26 propagator advances the real $(\mathbf E,\mathbf B)$ pair by a rigid rotation of angle

$$\Omega_\text{even}(k)=\omega_+(k/2)+\omega_-(k/2),\qquad \omega_s=\arccos u_s,\quad u_s(q)=c_xc_yc_z+s\,s_xs_ys_z$$

(arguments $q_i/\sqrt3$; $s=\pm1$; the **even** dispersion required for real gauge fields, F26). Its $\Delta t\to0$ limit is the free-Maxwell curl with light speed $c_\text{lat}=1/\sqrt3$ (Tier-1). The leading discrete-time curl-residual coefficient $c_\text{lat}/\sqrt2$ is confirmed (Tier-1 #51); whether the **subleading** coefficients have a closed form was open.

## Result

Expanding $\Omega_\text{even}$ order-by-order in $\lvert k\rvert$ against the linear free-Maxwell reference gives

$$\frac{\Omega_\text{even}(k)}{\lvert k\rvert}=c_\text{lat}+c_3(\hat k)\,\lvert k\rvert^{2}+c_5(\hat k)\,\lvert k\rvert^{4}+\dots,\qquad c_\text{lat}=\frac1{\sqrt3}.$$

### 1. Structural — even-power terms vanish exactly (algebraic)

The BCC chiral constraint gives $u_+(-q)=u_-(q)$, hence $\omega_-(q)=\omega_+(-q)$ and

$$\Omega_\text{even}(k)=\omega_+(\tfrac{k}{2}\hat d)+\omega_+(-\tfrac{k}{2}\hat d)=\Omega_\text{even}(-k),$$

an **even** function of the scalar $k$. An even function with the $c_\text{lat}\lvert k\rvert$ leading non-analyticity can contain **only odd powers of $\lvert k\rvert$** ($\lvert k\rvert,\lvert k\rvert^3,\lvert k\rvert^5,\dots$): a $k^2$ or $k^4$ term would be $\lvert k\rvert\times(\text{odd power of }k)$, which is odd in $k$ and forbidden. Therefore

$$\boxed{\;\text{all even-order dispersion corrections }(k^2,k^4,\dots)\text{ vanish identically}\;}$$

The single-chirality law $\Omega=2\omega_+(k/2)$ keeps a nonzero $k^2$ term (numerically $-\sqrt3/54$ along $\langle111\rangle$, $-\sqrt6/108$ along $\langle211\rangle$); the even symmetrisation removes it. **Physical content:** the F26 photon carries **no CPT-odd ($k^2$) Lorentz violation** — its leading vacuum-dispersion signature is the **CPT-even cubic $\lvert k\rvert^3$** term, which is exactly the form the GRB/AGN vacuum-dispersion bounds constrain, and it is helicity-symmetric (non-birefringent) by construction.

### 2. Leading subleading coefficient — closed form (machine-precision exact)

$$\boxed{\;c_3(\hat k)=-\frac{\sqrt3}{216}\,\bigl(p+3q\bigr)\;}\qquad
\begin{aligned}p&=\hat k_x^2\hat k_y^2+\hat k_y^2\hat k_z^2+\hat k_z^2\hat k_x^2\\ q&=\hat k_x^2\hat k_y^2\hat k_z^2\end{aligned}$$

the two cubic ($O_h$) invariants of the unit wavevector. Equivalently $c_3=-\tfrac{\sqrt3}{216}p-\tfrac{\sqrt3}{72}q$. Verified against the exact dispersion to $4.5\times10^{-19}$ across ten independent rational directions. Consequences:

| direction | $p,\ q$ | $c_3$ |
|-----------|---------|-------|
| $\langle100\rangle$ axis | $0,\ 0$ | $0$ — **exactly luminal & dispersionless** |
| $\langle110\rangle$ | $\tfrac14,\ 0$ | $-\tfrac{\sqrt3}{864}=-0.00200469$ |
| $\langle111\rangle$ (extremum) | $\tfrac13,\ \tfrac1{27}$ | $-\tfrac{\sqrt3}{486}=-0.00356389$ |

$c_3$ is **identical for the even and single-chirality laws** (the odd $\lvert k\rvert$ powers survive both); only the even-power $k^2$ term distinguishes them.

## Method / verification

`derive_f26_dispersion.py` evaluates the exact $\Omega_\text{even}$ at 60-digit precision, fits the even-power series $\Omega/\lvert k\rvert = c_\text{lat}+c_3k^2+c_5k^4$, and matches $c_3$ to the boxed closed form (worst residual $4.5\times10^{-19}$). It also exhibits the $c_2,c_4$ vanishing for the even law against the nonzero single-chirality values.

## Exactness tier

- Even-power vanishing: **Tier 1 (algebraic)** — forced by $\Omega_\text{even}(k)=\Omega_\text{even}(-k)$.
- $c_\text{lat}=1/\sqrt3$: **Tier 1** (pre-existing).
- $c_3(\hat k)=-(\sqrt3/216)(p+3q)$: **Tier 2 (machine-precision)**, residual $4.5\times10^{-19}$; the $p,q$ cubic-harmonic *structure* is forced by $O_h$ symmetry + the axis-vanishing.

## What this does not close

- The next coefficient $c_5(\hat k)$ (the $\lvert k\rvert^5$ term) is direction-dependent and computable by the same fit; its closed form (a degree-6 cubic harmonic) is not extracted here.
- The overall rational $\sqrt3/216$ is pinned to machine precision but not given a standalone algebraic derivation of the full angular form (the $c_3(111)=-\sqrt3/486$ point is the cleanest anchor).
- This is the F26 field-propagator **dispersion** signature. The larger $c_\text{lat}/\sqrt2=1/\sqrt6$ **bilinear-construction** curl residual is a separate object, closed in [[F245-curl-subleading-closed-forms]] (L1).
