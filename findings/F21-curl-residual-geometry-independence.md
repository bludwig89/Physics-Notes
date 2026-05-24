# Finding 21 — The composite-photon curl residual is geometry-independent: $\text{curl}/|k| = c_\text{lat}/\sqrt2$

*Recorded 2026-05-22 - 13:42. Run: `ca-simulation/forks/curl_fork_harness.py`. Result: `test-results/curl_fork_results_2026-05-22.json`. Forks: `forks/curl_fork_baseline_bcc.py`, `forks/curl_fork_cubic.py`.*

## Question

Finding 2 / Finding 7 established that the pointwise composite-photon bilinear
(Paper 1 Eq. 35) satisfies the Maxwell curl equation only to $O(k)$, with
normalized residual coefficient $1/\sqrt{2d}$ ($1/\sqrt6$ on the 3D BCC lattice).
**User hypothesis (2026-05-22):** working backwards from "$c_\text{lat}$ should
be 1, not $1/\sqrt3$" — is the BCC geometry to blame, and would a simple-cubic
lattice (which should give $c=1$) *also* fix the curl equation?

## Method

A geometry fork interface (mirroring the GR-3 fork pattern): each geometry
module exposes `uvec`, `unitary`, `dispersion`, `eigenmodes`. The harness runs
identical diagnostics on each — emergent $c_\text{lat}$ (axis + diagonal),
dispersion isotropy, curl-residual $k$-scan (log-log slope + leading
coefficient), and fermion-doubler count on the FFT grid. The curl residual
reuses `ca_maxwell.EM_bilinears` verbatim, so the BCC arm reproduces Finding 2
bit-for-bit as a built-in self-check.

**Simple-cubic Weyl QCA:** naive lattice momentum $s_i=\sin k_i$,
$U(k)=\cos|s|\,I - i(\sigma\cdot s)\sin|s|/|s|$, dispersion $\omega=|s|=\sqrt{\sum_i\sin^2 k_i}$, so $\omega\approx|k|$ and $c_\text{lat}=1$ at small $k$.

## Results

| metric | BCC (baseline) | simple-cubic |
|---|---|---|
| $c_\text{lat}$ (axis) | 0.577350 | **1.000000** |
| $c_\text{lat}$ (diagonal) | 0.577344 | 1.000000 |
| dispersion isotropy (diag/axis at $|k|=0.1$) | 0.98864 | 1.00111 |
| **fermion doublers (on grid)** | **1** | **8** |
| curl residual log-log slope | 1.0004 | 0.99995 |
| **curl residual $/|k|$** ($k\to0$) | **0.408248** $=1/\sqrt6$ | **0.707107** $=1/\sqrt2$ |

BCC self-check: curl$/k = 0.408248$ vs $1/\sqrt6$, rel err $4.6\times10^{-7}$ — harness faithful.

### The invariant

Computing curl$/k$ divided by $c_\text{lat}$:

| geometry | $c_\text{lat}$ | curl$/k$ | $(\text{curl}/k)/c_\text{lat}$ |
|---|---|---|---|
| BCC | 0.577350 | 0.408248 | **0.707107** |
| simple-cubic | 1.000000 | 0.707107 | **0.707107** |
| scaled-cubic $\alpha=0.5$ | 0.500000 | 0.353553 | **0.707107** |
| scaled-cubic $\alpha=1.0$ | 1.000000 | 0.707107 | **0.707107** |
| scaled-cubic $\alpha=2.0$ | 2.000000 | 1.414214 | **0.707107** |

To six figures across five geometries spanning $c_\text{lat}\in[0.5,2]$:

$$\boxed{\ \frac{\|\partial_t \mathbf E_G - i\,2\tilde{\mathbf n}\times\mathbf B_G\|}{(\|\mathbf E_G\|+\|\mathbf B_G\|)\,|k|}\ =\ \frac{c_\text{lat}}{\sqrt2}\ }$$

## Interpretation

1. **The user's speed intuition is correct.** Simple-cubic geometry gives $c_\text{lat}=1$ exactly, and is *more* isotropic at leading order (0.1% vs the BCC's 1.1% at $|k|=0.1$).

2. **But geometry does NOT fix the curl equation.** The residual stays $O(k)$ (slope $=1$) on every geometry; only the coefficient changes, and for cubic it is *larger* ($1/\sqrt2 > 1/\sqrt6$). The curl failure is **intrinsic to the pointwise un-smeared bilinear**, not the lattice.

3. **$1/\sqrt{2d}$ was the BCC special case.** The previously-recorded coefficient $1/\sqrt{2d}$ (Exactness Inventory #7) equals $c_\text{lat}/\sqrt2$ *only because* the QCA family has $c_\text{lat}=1/\sqrt d$. Decoupling $c_\text{lat}$ from $d$ (cubic: $c=1$; scaled-cubic: $c=\alpha$) shows the deeper invariant is $c_\text{lat}/\sqrt2$. The $\sqrt2$ is geometry- and dimension-independent — it is the intrinsic mismatch of the construction. Check: 2D-square has $c_\text{lat}=1/\sqrt2$, giving $1/2 = 1/\sqrt{2\cdot2}$ ✓.

4. **Cubic geometry costs the fermion sector 8 doublers.** Nielsen–Ninomiya $2^d=8$ zero modes appear at $k_i\in\{0,\pi\}$ — exactly the doubling the BCC QCA was constructed to avoid (it has a single Weyl point). Switching to cubic to buy $c=1$ would replace the model's single electron with 8 species. This is the concrete cost the QCA uniqueness theorem warns about.

## Verdict on the hypothesis

Half-vindicated, half-refuted, and informative either way:
- ✔ Cubic geometry → $c_\text{lat}=1$ and better isotropy.
- ✘ Cubic geometry → curl residual still $O(k)$ (worse coefficient), **and** 8 fermion doublers.
- **Geometry is ruled out as the cause of the $O(k)$ curl residual.** The next fork should target the **smearing function $f_{\mathbf k}(\mathbf q)$** (Bisio et al. lines 84–90) — Finding 2's hypothesis #1 — or the operator-ordering / c-number-vs-commutator question (hypothesis #3), not the lattice. The $c_\text{lat}/\sqrt2$ law gives that fork a sharp target: a successful smearing should drive the coefficient to $0$ (closing at $O(k^3)$), with the un-smeared $c_\text{lat}/\sqrt2$ as the baseline to beat.

## Caveats

- The doubler count is on the FFT grid the steppers actually sample ($N=12$, even, so $k_i=\pm\pi$ is hit). It measures doublers *as simulated*, which is the physically relevant count.
- The $c_\text{lat}/\sqrt2$ law is established for the specific pointwise-bilinear prescription used here (both Weyl fields = $+$-helicity eigenmode at $k/2$, evolved by $e^{-i\omega}$). A different spinor correlation could in principle change the $O(1)$ factor; testing that is part of the smearing-function fork.

## Cross-references

- Refines [[finding-2-curl-residual]] and Exactness Inventory #7 ($1/\sqrt{2d}\to c_\text{lat}/\sqrt2$).
- Geometry uniqueness context: `qca-papers-1-4-overview.md` (BCC vs cubic), `ca-reference.md`.
- $c_\text{lat}=1/\sqrt d$ origin: [[finding-10-sqrt-d-light-speed]].
- Propagation companion: [[F20-photon-fermion-propagation-demo]].
