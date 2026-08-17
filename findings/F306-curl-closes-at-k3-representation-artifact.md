# Finding 306 — The composite-photon curl equation closes at $O(k^3)$; the reported $O(k)$ failure was a representation artifact

**Date:** 2026-08-04 - 15:45
**Status:** Confirmed — quantitative closed form, gate-tested
**Supersedes the interpretation of:** [[F21-curl-residual-geometry-independence]] (REFUTED), [[F23-smearing-ruled-out-curl-residual-is-phase-locked]] (OVERSTATED), [[F25-real-rotation-exact-discrete-time-maxwell]] (OVERSTATED). Ledger `S18-curl-residual-representation-artifact`.
**Source:** `casim.engine.gauge.bilinear` — `maxwell_curl_residual_analytic`, `check_curl_closes_at_k3`. Record: `F306-curl-closes-at-k3` (gate). Result: `test-results/F306_curl_closes_at_k3.json`.
**Origin:** the independent reviews of F21, F23 and F25 (`docs/reviews/`, 2026-08-04), authorised by Ben as "supersede + successor".

---

## Summary

For four findings and roughly three months, this project has recorded that the
Paper 1 composite-photon bilinear satisfies the free Maxwell curl equation only to
$O(k)$, with a "geometry- and dimension-independent" coefficient
$c_\text{lat}/\sqrt2$. Two research sessions were then spent hunting the cause —
first geometry (F21), then Paper 1's smearing function (F23) — and a third
reinterpreted the residual as a Planck-scale prediction (F25).

**There was nothing to hunt.** The residual is an artifact of how it was defined.

`EM_bilinears` returns

$$E_G = \lvert n\rvert(G_T + G_T^*), \qquad B_G = i\lvert n\rvert(G_T^* - G_T),$$

which are **real** 3-vectors — the time-quadrature pair of a single circularly
polarised amplitude, not a Maxwell electric/magnetic pair. The residual then
differences them against $i\,2\tilde n\times B_G$, which is **pure imaginary**. And
the geometry is worse than the type clash: measured,

$$\boxed{\;B = \hat n\times E \ \text{ exactly}\;}\qquad\Longrightarrow\qquad \hat n\times B = -E,$$

so $\partial_t E = \Omega B$ points along $B$ while $\nabla\times B \propto \hat n\times B$
points along $-E$. **The two sides are orthogonal 3-vectors of equal length.** The
residual is therefore $\sqrt2$ times either one, and

$$\frac{\lVert\partial_t E - i2\tilde n\times B\rVert}{(\lVert E\rVert+\lVert B\rVert)\lvert k\rvert}
= \frac{\sqrt2\,\lvert n(k/2)\rvert}{\lvert k\rvert} \longrightarrow \frac{c_\text{lat}}{\sqrt2},$$

which is $c_\text{lat}$ — by its own definition, $c_\text{lat}\equiv d\Omega/d\lvert k\rvert$ —
multiplied by a quadrature factor. It carries no information about the lattice.

**Read the amplitudes analytically and the equation closes.** With
$\hat E = \lvert n\rvert G_T$ and $\hat B = \hat n\times\hat E$, the whole equation
collapses to the scalar condition

$$\Omega = 2\lvert n\rvert \qquad\Longleftrightarrow\qquad \omega(k/2) = \sin\omega(k/2),$$

whose failure is exactly the arccos-versus-sine gap of the BCC walk:

$$\Omega - 2\lvert n\rvert = \frac{k^3}{72\sqrt3} + O(k^5), \qquad
R_\text{analytic} = \frac{c_\text{lat}^3 k^2}{48} = \frac{k^2}{144\sqrt3}.$$

**The curl violation is $O(k^3)$** — which is precisely the pass criterion recorded
in this repo's own reference summary at `references/qca-papers-1-4-overview.md:407`:
*"measured violation of the curl equations decays as $O(k^3)$ as $\lvert k\rvert\to0$."*
The construction meets it and always did.

## The measurement

Both residuals computed from the **same fields at the same $k$**, 8 random
directions, seed 0. This side-by-side is the finding; either column alone would
prove nothing.

| $k$ | original reading (real pair) | analytic-amplitude reading | closed form $c_\text{lat}^3k^2/48$ |
|---|---|---|---|
| $10^{-1}$ | 0.4100532 | $4.0643\times10^{-5}$ | $4.0094\times10^{-5}$ (1.37%) |
| $10^{-2}$ | 0.4084358 | $4.0149\times10^{-7}$ | $4.0094\times10^{-7}$ (0.14%) |
| $10^{-3}$ | 0.4082671 | $4.3648\times10^{-9}$ | $4.0094\times10^{-9}$ (8.86%) |
| limit | $c_\text{lat}/\sqrt2 = 0.4082483$ | $\to0$ as $k^2$ | — |

The original column is **flat** across two decades; the analytic column falls by a
factor of **9312**, i.e. $k^2$. Geometry (B $= \hat n\times E$) confirmed to
$\cos = 0.9999999999999999$.

The closed-form match is asserted for $k\ge10^{-2}$ only. The closed form is
isotropic while the measurement is a *max* over directions and inherits the $O(k)$
BCC anisotropy of $\Omega - 2\lvert n\rvert$, plus transverse-projection round-off
that does not scale with the residual — both worst at the smallest $k$. The
$k=10^{-3}$ row carries the $k^2$ *scaling* check instead.

## Why nothing anyone tried could have worked

Each of the three superseded findings tested a variable that the mechanism makes
irrelevant, and each got the correct null answer for the wrong reason.

| Tried | F-number | Why it could not work |
|---|---|---|
| Change the lattice geometry | F21 | $R = \sqrt2\sin(\Omega/2)/\lvert k\rvert$ holds for **any** walk $U = uI - i\sigma\cdot n$ with $u^2+\lvert n\rvert^2=1$. Universality in $c_\text{lat}$ is tautological once $c_\text{lat}\equiv d\Omega/d\lvert k\rvert$ |
| Smear over relative momentum | F23 | The LHS is real and the RHS imaginary for **any** real weighting $f_k(q)$, so $R$ is a strict quadrature: $R=0$ requires $B\equiv0$, a magnetically empty configuration |
| Take $\Delta t\to0$ | F23, F25 | $E$ is real *by construction*, so $\partial_t E = \Omega B$ is real at every $\Delta t$ including the exact derivative. Measured 0.4082469 / 0.4082468 / 0.4082469 at $\Delta t = 10^{-3}$, $10^{-6}$, exact |
| Drop the explicit $i$ | (obvious first fix) | Does **not** help — 0.40825 unchanged. Orthogonality, not the $i$, is what binds |

## Exactness

| Result | Class | Tolerance | Record |
|---|---|---|---|
| $R_\text{analytic} = c_\text{lat}^3k^2/48$ | quantitative | 5% for $k\ge10^{-2}$ | `F306-curl-closes-at-k3` |
| $R_\text{analytic}$ falls as $k^2$ | quantitative | $>5\times10^3$ over two decades | same |
| $B = \hat n\times E$ | machine | $1-\cos < 10^{-9}$ | same |
| original reading flat at $c_\text{lat}/\sqrt2$ | machine | spread $<10^{-2}$ | same (**control**) |

## What is not claimed

- **This is not a new photon.** The σ-bilinear construction remains retired for the
  photon by `S1-F69-sigma-bilinear-photon` (birefringent, excluded by GRB/AGN
  polarimetry — F65/F66/F67), and F302 showed the *transpose* form
  $\varphi^T\sigma\psi$ is not an SO(3) 3-vector. F306 says only that the curl
  equation was never the reason to retire it. The model's photon is still the
  paired-spinor photon (Core Design Decision 5).
- **No new physics is derived.** The $O(k^3)$ closure is a property the construction
  always had; what is new is the correct reading, the closed-form coefficient, and
  a test that can tell the two readings apart.
- **`maxwell_curl_residual` is unchanged, bit for bit.** Four call sites depend on
  its numbers — `tests/runners/run_L_tests.py:231`,
  `bilinear_2d.maxwell_curl_residual_2d`, and the F21 and F23 fork harnesses. The
  new reading is a **sibling** function, `maxwell_curl_residual_analytic`, with a
  banner on the old one. Deciding whether to migrate the four consumers is left
  open deliberately.

## Prior art and provenance

The $O(k^3)$ pass criterion is the source literature's own, recorded at
`references/qca-papers-1-4-overview.md:407`. The diagnosis was reached
independently three times during the 2026-08-04 review series, by three different
routes, all agreeing on $c_\text{lat}^3/48 = 1/(144\sqrt3)$:

1. the F21 adversarial referee, via the exact-derivative analytic amplitudes;
2. this session's own verification of that referee, independently coded;
3. the F25 blind agent, via $\omega = \sin\omega$ and $\Omega - 2\lvert n\rvert = k^3/(72\sqrt3)$.

**F23 got closest first and was steered away.** On 2026-05-23 it identified the
real-vs-imaginary phase structure correctly — two months before the reviews — and
named Finding 2's hypothesis #3 (operator-algebra vs c-number bilinear) as the
primary candidate. It then attached the wrong mechanism to the right hypothesis
(finite $\Delta t$), and prescribed a fork that would have returned 0.40823 and
struck H3 off the list. **F24 also anticipated part of this**: its
representation-theory section placed $\psi^T\sigma\psi$ in the $(1,0)$ irrep with a
$(0,0)$ scalar contamination, which is the same non-covariance F302 measured.

An independent prior observation also exists inside the repo:
`docs/audits/model-observations.md:19` flagged that "`maxwell_curl_residual` is
labeled L3 INFO but the residual is $O(k)$, not $O(k^3)$" and proposed demoting the
L3 layer. That audit item is now closed by this finding — the answer is that L3 was
right and the residual was wrong.

## What would falsify this

1. $R_\text{analytic}$ failing to scale as $c_\text{lat}^3k^2/48$ on any walk in the
   class $U = uI - i\sigma\cdot n$, $u^2+\lvert n\rvert^2 = 1$.
2. $\cos(B,\ \hat n\times E) \neq 1$ at any non-degenerate $k$ — that would break the
   orthogonality diagnosis and reopen the $O(k)$ question.
3. The original real-pair residual departing from $c_\text{lat}/\sqrt2$ under a
   change that should not matter — which would mean it is measuring something after
   all.
4. Any real weighting $f_k(q)$ producing $R\to0$ with a non-degenerate $(E,B)$ pair,
   which would break the quadrature theorem.

## Status

**Live.** Gate record `F306-curl-closes-at-k3`, 5/5, and
`tests/findings/test_F306_curl_closes_at_k3.py` 5/5.

Open, deliberately:

- whether to migrate the four `maxwell_curl_residual` consumers to the analytic
  reading, or leave them measuring the convention with a banner. Ben asked for the
  survey before the change; the survey is in this finding's `## What is not claimed`
  and the decision is not taken here.
- whether the $72$ in $\Omega/(2\lvert n\rvert) - 1 = k^2/72$ is the same $72$ as the
  constants registry's $1/(72\pi)$. The repo's own rule is that values which
  coincide stay separate constants, so this needs a deliberate check rather than an
  assumption.
- Finding 2's hypothesis #3 as originally posed — whether Paper 1 Eq. 35's
  $G_T^\dagger$ is an *operator* adjoint, which is the deeper reason the c-number
  implementation forces real fields. arXiv was unreachable from the sandbox
  throughout the review series, so this rests on the repo's own transcription.

## Cross-references

- Reviews that produced this: `docs/reviews/F21-review-2026-08-04.md`,
  `F23-review-2026-08-04.md`, `F25-review-2026-08-04.md`.
- Ledger: `S18-curl-residual-representation-artifact` in `docs/theory/supersessions.yaml`.
- [[F302-sigma-bilinear-so3-covariance]] — the transpose bilinear is not an SO(3)
  3-vector; independent of, and consistent with, this finding.
- [[F26-speed-of-light-as-rotation-rate]] — $c_\text{lat}\equiv d\Omega/d\lvert k\rvert$,
  which is what makes the old "law" tautological.
