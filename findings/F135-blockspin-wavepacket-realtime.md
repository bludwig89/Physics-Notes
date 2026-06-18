# F135 — Real-time wave-packet dynamics survive block-spin: a moving, spreading massive Dirac packet coarse-grains faithfully, and mass is the matter sector's one relevant operator (rest-gap eigenvalue $b$)

**Date:** 2026-06-11
**Status:** Confirmed — 5/5 checks PASS. RT1 faithfulness and RT4 mass-eigenvalue are **machine-precision**; RT2/RT3 are quantitative (velocity/width agree fine-vs-coarse); RT5 unitarity at the FFT floor. Closes the dynamical check left open by [[F132-blockspin-dynamical-bound-states]] §6 (RG commutes with binding was shown only for static eigenstates). Phase-2 item "real-time wave-packet dynamics under $R_b$" of `docs/roadmaps/roadmap-scale-to-real-space.md`.
**Script:** `tests/findings/test_F135_blockspin_wavepacket_realtime.py`
**Results:** `test-results/F135_blockspin_wavepacket_realtime.json`, `..._summary.md`
**Cross-references:** [[F129-blockspin-free-photon]] (the massless analog — this is its massive counterpart), [[F130-blockspin-gauge-gravity]] (T1 marginal $c$, T2 irrelevant LIV, C1 relevant $\sigma$), [[F132-blockspin-dynamical-bound-states]] (the static-eigenstate case this completes), [[F85-p0-dynamical-fermions]] (the real-time fermion wave-packets), [[F9]]/`ca_dirac.py` (the exact-QCA 2D Dirac propagator used).

---

## 1. Why this finding exists

F131/F132 proved the block-spin RG $\mathcal R_b$ commutes with binding for **static
energy eigenstates** — but there $\mathcal R_b\circ e^{-iHt}$ is a trivial global
phase, so it is the weakest possible dynamical statement. The open question (F132 §6):
does coarse-graining commute with *genuine* real-time dynamics — a wave-packet that
**moves and spreads**? This is the matter-sector analog of the F129 free-photon
faithfulness result, and it is the one that licenses running matter at a coarse-grained
"real-space-analogous" scale.

## 2. Setup

The model's exact-QCA 2-D Dirac propagator (`ca_dirac.dirac_step_2d_splitstep`),
dispersion $\omega(\mathbf k)=\arccos\!\big(\sqrt{1-m^2}\,\cos\tfrac{k_x}{\sqrt2}\cos\tfrac{k_y}{\sqrt2}\big)$.
The wave-packet is a strictly band-limited **positive-energy** state (built in
$k$-space on a thin axis band, each mode carrying its $+\omega$ eigenvector,
phase-aligned for a smooth localised lump), so it propagates at the group velocity
with no zitterbewegung splitting. The renormalised coarse rule (one coarse tick $=b$
fine ticks, space $\to ba$) is

$$\Omega_\text{coarse}(\mathbf q)=b\,\omega(\mathbf q/b),$$

realised by evaluating the audited $D_k$ machinery at the fine wavenumber $\mathbf q/b$
and advancing $b$ ticks via the propagator's own analytic $dt$-interpolation. The block
average $\mathcal R_b$ on the 4-spinor is **complex-safe** (preserves the imaginary
part the float-casting `ca_blockspin.block_average` would drop — CLAUDE.md caveat).

## 3. Results

| check | statement | result |
|---|---|---|
| **RT1** faithfulness | $\mathcal R_b\!\circ\!\text{evolve}_\text{fine}^{bN}=\text{evolve}_\text{coarse}^{N}\!\circ\!\mathcal R_b$, checked at every coarse tick | $1.4\times10^{-15}$ ($b{=}2$), $2.5\times10^{-15}$ ($b{=}3$) over the whole trajectory |
| **RT2** group velocity | packet centroid speed, fine vs coarse (physical units) | $0.5330$ vs $0.5317$ cells/tick (moves; agree $<5\times10^{-3}$) |
| **RT3** spreading | rms-width growth, fine vs coarse | $0.0672$ vs $0.0679$ fine-cells (spreads; agree) |
| **RT4** mass relevant | rest-gap $\omega(0)=\arcsin m$ eigenvalue under $\mathcal R_b$ | exactly $b$ for $b=2,3,4$, all $m$; $\lambda_C^\text{phys}$ invariant ($<10^{-12}$) |
| **RT5** unitarity | norm drift, both lattices | $\le8\times10^{-16}$ |

RT1 is the heart: a coarse run on $b^2\times$ fewer cells and $b\times$ fewer ticks
reproduces the fine packet's *entire* real-time trajectory — position, shape, phase —
to the FFT floor, not just a final snapshot.

## 4. The headline: mass is the matter sector's relevant operator

The renormalised rule makes the RG flow of every operator explicit, and it completes
the classification begun in the photon/gauge sectors:

$$\Omega_\text{coarse}(\mathbf q)=b\,\omega(\mathbf q/b)=\underbrace{b\,\omega(0)}_{\text{rest gap}}+\underbrace{c\,|\mathbf q|}_{\text{marginal}}+\underbrace{O(|\mathbf q|^3/b^2)}_{\text{irrelevant}}+\cdots$$

| operator | RG eigenvalue | class | where |
|---|---|---|---|
| **mass** (rest gap $\omega(0)=\arcsin m$) | $b$ | **relevant** | **F135 (this)** |
| string tension $\sigma$ | $b$ | relevant | F130-C1 |
| contact coupling | runs ($g/g_c$) | relevant | F132-P |
| speed of light $c_\text{lat}$ | $1$ | marginal | F129/F130-T1 |
| LIV / lattice artifacts | $b^{-n}$ | irrelevant | F130-T2 |
| finite-range / smooth potentials | $b^{-2}$ | irrelevant | F132-D |

The dimensionless lattice mass runs $m\to\sin(b\arcsin m)\approx b\,m$ (small-$m$
continuum limit); the **physical** Compton wavelength $\lambda_C=a/\arcsin m$ is
invariant (the gap grows by $b$, the cell grows by $b$). Mass setting an inverse
length is *why* it is relevant — exactly parallel to the string tension. So a coarse
lattice keeps a massive particle's physical size and speed fixed while its
dimensionless mass scales with the blocking factor; the RG knows the difference
between a length scale (relevant) and a dimensionless velocity (marginal).

## 5. Scope and limits

- 2-D exact-QCA Dirac (the model's verified massive propagator). The 3-D BCC Weyl
  step has the same linear structure; the per-mode argument (a real scalar block
  kernel commutes with any per-mode unitary) is dimension-independent, so the
  faithfulness result is not 2-D-specific, but only 2-D is run here.
- Single free particle. Coarse-graining of a *bound, real-time-evolving* state (e.g. a
  proton wave-packet) is downstream of a real-space confined proton (Phase-2 item #1,
  open).
- Positive-energy packet by construction; a $\pm$-mixed (zitterbewegung) packet is
  also band-limited so RT1 holds for it identically — only the clean velocity/width
  readouts (RT2/RT3) need the single-branch state.

## 6. Exact vs numeric

| Result | Tier |
|---|---|
| RT4 rest-gap eigenvalue $=b$; $\lambda_C^\text{phys}$ invariant | machine precision ($<10^{-12}$) |
| RT1 real-time faithfulness (whole trajectory) | $\le2.5\times10^{-15}$ |
| RT5 norm drift | $\le8\times10^{-16}$ |
| RT2 group velocity fine vs coarse | $0.5330$ vs $0.5317$ ($<5\times10^{-3}$) |
| RT3 rms spreading fine vs coarse | $0.0672$ vs $0.0679$ |
