# F245 — Closed forms for the composite-photon curl-residual subleading coefficients (L1)

**Date:** 2026-07-15 - 19:10
**Status:** Confirmed — closes open-derivation **L1** (`open-derivations-prompts-v2.md` Part 3; exactness-inventory "not-yet-met" #5). Both "measured but no closed form" subleading coefficients of Finding 7's composite-photon curl residual are now derived in closed form and verified at mpmath precision (2D: 2.8×10⁻¹⁹; 3D: 9×10⁻¹⁵, Richardson-limited). The 2D on-axis value is additionally derived **algebraically**. Neither number is a new fundamental constant.
**Modules:** `ca-simulation/derive_curl_subleading.py` (new; cross-checked against `ca_maxwell_2d.py` and `ca_maxwell.py` to 10 digits — those modules used, not modified)
**Cross-references:** [[F01-F15-findings]] (Finding 7 — the curl residual and its leading constant $1/\sqrt{2d}$), and the F25/F26 exact real-rotation EM propagator (the $\Delta t\to0$ limit these coefficients are the discrete-time corrections to).

---

## What was open

Finding 7 established the pointwise composite-photon curl residual

$$\frac{\text{curl residual}}{\lVert k\rVert} = \frac{1}{\sqrt{2d}} + (\text{subleading}) + \dots,\qquad \frac{1}{\sqrt{2d}}=\frac{1}{\sqrt2}\,c_\text{lat},$$

with the leading constant $1/\sqrt{2d}$ derived exactly (dimensionality-driven, Tier-1). The **subleading** coefficients were measured numerically with no closed form (exactness-inventory not-yet-met #5):

- **2D square:** $\text{curl}/k = \tfrac12 + \alpha\,k^2 + \mathcal O(k^3)$, with $\alpha\approx-0.0104$ (quadratic — 2D dispersion correction starts at $k^2$).
- **3D BCC:** $\text{curl}/k = \tfrac1{\sqrt6} + \beta\,k + \mathcal O(k^2)$, with $\beta\approx+0.01883$ (linear — BCC has an $\mathcal O(k)$ dispersion correction along $(1,1,1)$).

The near-miss guesses on record were $-1/96$ (2D) and $1/54$ (3D). Both are now settled.

## Result

### 2D square — direction-resolved closed form (machine-precision exact)

For $k$ at angle $p$ from the $x$-axis,

$$\boxed{\;\alpha(p) = \frac{\cos 4p - 9}{768}\;}$$

verified against the exact eigenmode/bilinear construction to $2.8\times10^{-19}$ at eight angles. Consequences:

| direction | $\alpha$ | value |
|-----------|----------|-------|
| on-axis $p=0,\tfrac\pi2$ | $-\tfrac1{96}$ | $-0.0104166\ldots$ |
| $p=\tfrac\pi4$ (45°, max $\lvert\alpha\rvert$) | $-\tfrac{5}{384}$ | $-0.0130208\ldots$ |
| direction average $\langle\alpha\rangle$ | $-\tfrac{9}{768}=-\tfrac{3}{256}$ | $-0.0117187\ldots$ |

Finding 7's reported **$-0.0104$ is the on-axis value $-1/96$** — and because $\alpha<0$ everywhere (smaller $\lvert\alpha\rvert$ ⇒ larger $\text{curl}/k$ ⇒ larger residual), the on-axis direction is exactly the **max-residual** direction the random-direction sampler converges to. The near-miss $-1/96$ was correct.

**Algebraic derivation (on-axis).** Along $(0,1)$ the half-momentum unitary is the plane rotation $U=\begin{psmallmatrix}c&-s\\s&c\end{psmallmatrix}$ with $c=\cos\theta,\ s=\sin\theta,\ \theta=k/(2\sqrt2)$. The positive eigenmode is $\psi=(1,i)/\sqrt2$, giving the bilinear $G=(i,0,1)$, $\hat n=(0,1,0)$, so $G_T=(i,0,1)$ and $\lvert E_0\rvert=\lvert B_0\rvert=2s$. Evolving $G\to G\,e^{-2i\theta}$ and forming the normalised residual $r=\lVert\partial_t E - i(2\mathbf n)\times B\rVert/(\lvert E\rvert+\lvert B\rvert)$ collapses (the transverse/quadrature algebra) to

$$r = \sqrt2\,\lvert\sin\theta\rvert = \sqrt2\,\sin\!\frac{k}{2\sqrt2}\quad\Rightarrow\quad \frac{r}{k}=\frac12 - \frac{k^2}{96} + \mathcal O(k^4),$$

so $\alpha_\text{axis}=-1/96=(\cos4p-9)/768\big|_{p=\pi/2}$ exactly. The residual is purely the discrete-time ($\Delta t=1$) finite-rotation correction to the F25/F26 exact rotation law — a Planck-scale signature, not a model error.

### 3D BCC — direction-resolved closed form (machine-precision exact)

For a unit wavevector $\hat k=(\hat k_x,\hat k_y,\hat k_z)$,

$$\boxed{\;\beta(\hat k) = -\frac{\sqrt2}{12}\,\hat k_x\,\hat k_y\,\hat k_z\;}$$

verified across six independent rational directions to $9\times10^{-15}$ (3-point Richardson). Structure and consequences:

- **Vanishes on every coordinate plane** (any component zero ⇒ $\beta=0$). This is the lowest cubic ($O_h$) harmonic — the $T_{2}$/$xyz$ invariant — with the correct parity; the linear-in-$k$ curl correction is carried entirely by this single anisotropy channel.
- **Sign varies with direction**: $\beta<0$ toward the body diagonals, $\beta=0$ on axes/faces.
- **Extremum** at $\hat k=(1,1,1)/\sqrt3$: $\lvert\beta\rvert_\text{max}=\dfrac{\sqrt2}{12}\cdot\dfrac1{3\sqrt3}=\dfrac{\sqrt6}{108}=0.0226805$.

**Finding 7's "$0.01883$" is not a constant.** It is $\beta$ evaluated at the seed-0, 8-direction max-residual random direction $(0.7415,\,0.5385,\,-0.4002)$: $-\tfrac{\sqrt2}{12}(0.7415)(0.5385)(-0.4002)=+0.018833$, reproducing the reported digit exactly. The old near-miss $1/54=0.01852$ was chasing a random-seed artifact of a direction-dependent function. Averaging $\beta$ over the sphere gives $\langle\beta\rangle=0$ (odd in each component).

## Method / verification

`derive_curl_subleading.py` replicates the exact eigenmode → $\sigma$-bilinear → transverse $(E,B)$ → one-tick finite-difference → $i(2\mathbf n)\times B$ residual pipeline of `ca_maxwell_2d.py` (2D, $\phi=\psi_+$) and `ca_maxwell.py` (3D, $\phi=\psi_-$) in `mpmath` at 50 dps, using the closed-form eigenvector $(U_{12},\,e^{\mp i\omega}-U_{11})$. It agrees with the production numpy modules to 10 digits on the leading $1/\sqrt{2d}$ and reproduces the per-direction subleading coefficient, which is then matched to the boxed closed forms.

## Exactness tier

- 2D $\alpha(p)=(\cos4p-9)/768$: **Tier 1 (algebraic)** on-axis; **Tier 2 (machine-precision)** for the full angular form (residual $2.8\times10^{-19}$).
- 3D $\beta(\hat k)=-(\sqrt2/12)\hat k_x\hat k_y\hat k_z$: **Tier 2 (machine-precision)**, residual $9\times10^{-15}$ (Richardson-limited).

## What this does not close

- The 3D overall constant $\sqrt2/12$ and the 2D $1/768$ are pinned to machine precision by the numerics but not yet given a standalone algebraic derivation for the *full* angular form (only the 2D on-axis case is closed algebraically). The angular *shapes* ($\cos4p$; the $xyz$ cubic harmonic) are forced by square/cubic symmetry.
- This is the Finding-7 **bilinear-construction** curl residual. Its relationship to the F25/F26 exact-rotation-law curl (open item L2) is the natural next step.
