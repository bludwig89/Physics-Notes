# F302 — ε = iσ₂ is the object that makes a transpose bilinear a 3-vector; and no live gauge sector was ever on the form that lacks it

**Date:** 2026-08-03 - 14:45
**Status:** Confirmed — 6/6 checks PASS (`tests/findings/test_F302_bilinear_so3.py`, registry record `F302-bilinear-so3-covariance`, gate tier). The algebraic core is **Tier-1 exact** (sympy, six residuals identically zero); the covariance and amplitude measurements are machine precision on this tree's own modules.
**Module:** `casim.engine.gauge.derive_bilinear_so3`
**Results:** `test-results/F302_bilinear_so3.json`
**Prompted by:** recommendation 3 of [the independent review of F17](../docs/reviews/F17-review-2026-08-03.md), which measured $\lVert G_T\rVert^2 = 2(\hat n\cdot\hat y)^2$ for the retired composite photon and flagged the same signature as a possible unnoticed isotropy violation in the sectors ledger record `S1-F69-sigma-bilinear-photon` retains.
**Cross-references:** [[F29-w-triplet-bilinear-su2-bridge]] (found the transpose form fails SU(2); this is its spatial-rotation counterpart and its vindication), [[F69-paired-spinor-photon]] (retired the transpose photon), [[F39-two-helicity-photon-bilinear]], [[F65-photon-birefringence-crisis]].

---

## Summary

Two results, graded differently.

**The algebra (exact).** For an arbitrary $2\times2$ matrix $U$,

$$U^{\mathsf T}\,\varepsilon\,U \;=\; \det(U)\,\varepsilon,\qquad \varepsilon \equiv i\sigma_2,$$

which is the adjugate identity, not an SU(2) fact — SU(2) enters only by fixing $\det U = 1$. Combined with the standard adjoint identity $U^\dagger\sigma^iU = R^{ij}\sigma^j$, this gives

$$U^{\mathsf T}(\varepsilon\sigma^i)U \;=\; \varepsilon\,(\varepsilon^{-1}U^{\mathsf T}\varepsilon)\,\sigma^i U \;=\; \varepsilon\,U^{-1}\sigma^i U \;=\; \varepsilon\,U^\dagger\sigma^i U \;=\; R^{ij}\,(\varepsilon\sigma^j).$$

So **$\varepsilon$ is precisely the object that converts dagger covariance into transpose covariance.** $\psi^{\mathsf T}\varepsilon\sigma\psi$ is a genuine spatial 3-vector; $\psi^{\mathsf T}\sigma\psi$ is not. The mechanism is visible in one line of matrix symmetry: $\varepsilon\sigma^i$ are all three *symmetric*, whereas $\sigma_2$ is antisymmetric, so $\psi^{\mathsf T}\sigma_2\psi \equiv 0$ and the plain triple is the covariant one **with its $\hat y$ component deleted**:

$$\psi^{\mathsf T}\sigma\psi = (2ab,\; \mathbf{0},\; a^2-b^2), \qquad \psi^{\mathsf T}\varepsilon\sigma\psi = (a^2-b^2,\; i(a^2+b^2),\; -2ab).$$

That deleted component is the entire origin of the $2(\hat n\cdot\hat y)^2$ amplitude law: the surviving amplitude tracks the axis of the one antisymmetric Pauli matrix, and the basis in which $\sigma_2$ is the antisymmetric one is a *convention*, so the preferred axis is an artifact of the Pauli basis, not of the lattice.

**The audit (negative, and this is the useful half).** The feared isotropy violation **is not in the gauge sectors.** W, Z and gluon never adopted the transpose form. F29 had already found it fails SU(2) isospin, `gluon.py`'s own comment records that it fails SU(3) too ("Hermitian only"), and every production construction is consequently the Hermitian one — which is covariant directly, by $U^\dagger\sigma U = R\sigma$, with no $\varepsilon$ needed. Measured, on this tree's code: **the transpose form misses SO(3) covariance by 1.96 (O(1)); every other construction lands at 2–6 × 10⁻¹⁶.** The transpose bilinear has **no live physics consumer** — only retired-photon diagnostics and one fork harness.

---

## Why the transpose form was reached for, and why "just use Hermitian" is not the fix

This is the part that makes the decision non-obvious, and it is measured here for the first time.

For a **single mode contracted with itself**, the Hermitian singlet is
$$\psi^\dagger\sigma\psi \;=\; \hat n \quad\text{exactly}$$
— the Bloch vector, i.e. the spin axis. Measured on a real BCC helicity eigenmode: $\lvert \psi^\dagger\sigma\psi - \hat n\rvert = 0.0$ exactly, transverse part $\lVert G_{H,T}\rVert^2 = 0$. **It is purely longitudinal: there is no transverse field at all.** So the Hermitian form, which is what the gauge sectors correctly use, is simply unavailable to a one-spinor photon-like construction — it would give the zero field. The transpose form was reached for because it *does* have transverse content.

The Cartan/Penrose form is the object that is **both** covariant and transverse. On the same eigenmodes it is exactly null ($G\cdot G = 0$ with no helicity condition), exactly transverse ($\hat n\cdot G \sim 10^{-17}$), and carries the **direction-independent** amplitude $\lVert G_T\rVert^2 = 2$.

That is the decision:

| Construction | Two spinors? | SO(3) 3-vector | Transverse content | Verdict |
|---|---|---|---|---|
| $\phi^\dagger\sigma\psi$ (Hermitian) | needs $\phi\ne\psi$, or a $\tau^a$/$T^a$ that mixes | **yes** (2–6e-16) | yes when the indices mix; **zero** for $\phi=\psi$ | **correct for W / Z / gluon — and already in use** |
| $\phi^{\mathsf T}\sigma\psi$ (transpose) | any | **no** (1.96) | yes, but $\propto(\hat n\cdot\hat y)^2$ | **wrong; retired with the photon, no live consumer** |
| $\phi^{\mathsf T}\varepsilon\sigma\psi$ (Cartan) | any | **yes** (4e-16) | yes, $\lVert G_T\rVert^2\equiv2$ | **the covariant completion, if a transpose bilinear is ever wanted again** |

---

## Measurements

### SO(3) covariance — $\max_{40\ \text{rotations}} \lVert G(U\psi) - R\,G(\psi)\rVert / \lVert G\rVert$

$U$ is a random SU(2) element and $R^{ij} = \tfrac12\operatorname{tr}(\sigma^iU\sigma^jU^\dagger)$ its adjoint image, so $U^\dagger\sigma^iU = R^{ij}\sigma^j$ holds by construction and any failure is a property of the contraction.

| Construction | Where | Max rel. error | |
|---|---|---|---|
| `bilinear_G` — transpose $\phi^{\mathsf T}\sigma^i\psi$ | `gauge/bilinear.py:186` | $1.962$ | **FAILS** |
| Cartan $\phi^{\mathsf T}\varepsilon\sigma^i\psi$ | *(not previously in the tree)* | $3.96\times10^{-16}$ | covariant |
| `_singlet_bilinear_H` | `gauge/bilinear.py:347` | $6.00\times10^{-16}$ | covariant |
| `_triplet_bilinear_H` — the F29 $W^{a,i}$ | `gauge/bilinear.py:358` | $3.72\times10^{-16}$ | covariant |
| `fermion_current_isospin` — the production W current | `gauge/weak_wmu.py:1218` | $3.15\times10^{-16}$ | covariant |
| `quark_colour_octet_bilinear_bcc` | `gauge/gluon.py:346` | $3.75\times10^{-16}$ | covariant |
| `quark_colour_octet_bilinear_2d` | `gauge/gluon.py:283` | $2.38\times10^{-16}$ | covariant |

### The amplitude law, on real BCC helicity eigenmodes ($k = 0.05$)

| $\hat k$ | $\hat n\cdot\hat y$ | $\lVert G_T\rVert^2$ transpose | $2(\hat n\cdot\hat y)^2$ | $\lVert G_T\rVert^2$ Cartan |
|---|---|---|---|---|
| $\hat x$ | $0.0000$ | $0.0000000000$ | $0.000000$ | $2.0000000000$ |
| $\hat y$ | $-1.0000$ | $2.0000000000$ | $2.000000$ | $2.0000000000$ |
| $\hat z$ | $0.0000$ | $0.0000000000$ | $0.000000$ | $2.0000000000$ |
| $(1,1,1)$ | $-0.5708$ | $0.6516881986$ | $0.651688$ | $2.0000000000$ |
| $(1,0,1)$ | $+0.0144$ | $0.0004166956$ | $0.000417$ | $2.0000000000$ |
| $(1,2,3)$ | $-0.5300$ | $0.5618092495$ | $0.561809$ | $2.0000000000$ |

Over ten directions (six named, four random): $\max\bigl\lvert\lVert G_T\rVert^2_\text{transpose} - 2(\hat n\cdot\hat y)^2\bigr\rvert = 8.9\times10^{-16}$ and $\max\bigl\lvert\lVert G_T\rVert^2_\text{Cartan} - 2\bigr\rvert = 8.9\times10^{-16}$. The review's measured law is confirmed as an identity, and the zero at $\hat n\perp\hat y$ is exact, not small: $\hat x$ and $\hat z$ give $0.0000000000$.

### Symbolic core — six residuals, all identically zero

| Statement | Residual |
|---|---|
| $U^{\mathsf T}\varepsilon U - \det(U)\,\varepsilon = 0$, arbitrary $2\times2$ $U$ | $0$ |
| $\varepsilon\sigma^i$ symmetric, all three | $0$ |
| $\sigma_2$ antisymmetric | $0$ |
| $(\psi^{\mathsf T}\varepsilon\sigma\psi)\cdot(\psi^{\mathsf T}\varepsilon\sigma\psi) = 0$, every $\psi$ | $0$ |
| $(\psi^{\mathsf T}\sigma\psi)\cdot(\psi^{\mathsf T}\sigma\psi) = (\psi^{\mathsf T}\psi)^2$ (Fierz) | $0$ |
| $\psi^{\mathsf T}\sigma_2\psi = 0$, every $\psi$ | $0$ |

---

## Sector audit

| Sector | Module | Form | Note |
|---|---|---|---|
| photon (canonical, F69) | `gauge/photon.py` | **none** | paired-spinor; builds no σ-bilinear at all |
| photon (retired, F65–F67) | `gauge/bilinear.py` | **transpose** | `bilinear_G`; retired as the photon, diagnostics only |
| W triplet | `bilinear.py:_triplet_bilinear_H` | hermitian | the F29 construction |
| W current (production) | `weak_wmu.py:fermion_current_isospin` | hermitian | $\eta^\dagger\sigma^i\tau^a\eta$ |
| W (SU(2) action) | `gauge/weak.py` | none | SU(2) acts *on* the doublet; no field built from spinors |
| Z | `gauge/weak_z.py` | none | independent $(E_Z,B_Z)$ pair; scalar site-density currents |
| charged current | `gauge/charged_current.py` | none | scalar isospin ladder, no $\sigma^i$ |
| gluon / colour octet | `gluon.py:quark_colour_octet_bilinear_{2d,bcc}` | hermitian | its own comment: transpose fails SU(3) too |
| strong / su3_ladder / colour_* | `gauge/{strong,su3_ladder,colour_*}.py` | none | link variables and irrep labels |

Remaining transpose call sites, all retired-photon diagnostics: `bilinear.py` (internal), `bilinear_2d.py`, `forks/gauge/curl_fork_harness.py`, `forks/lattice/smearing_fork_harness.py`, and two test files. **Zero live physics consumers.**

---

## What this corrects

**Ledger record `S1-F69-sigma-bilinear-photon` is inaccurate as written.** Its `retained:` clause says *"the sigma-bilinear FIELD CONSTRUCTION survives for the massive and non-Abelian sectors (W / Z / gluon)"*. What survives for those sectors is the **Hermitian** bilinear; the σ-**transpose** construction survives nowhere. The clause reads as though the retired object were still load-bearing somewhere, which is what made the F17 review's isotropy concern reasonable — and the concern was worth chasing precisely because the ledger said the object was retained.

**F29 is vindicated and extended.** F29 found the transpose form fails SU(2) *isospin* invariance ($\approx 4.18$, O(1)). This is the same defect in the spatial-rotation channel, and it has the same one-line cause: $U^{\mathsf T}\ldots U$ is not a similarity transform unless the invariant tensor $\varepsilon$ is inserted. F29's fix — go Hermitian — propagated into production code three times independently (`bilinear.py`, `weak_wmu.py`, `gluon.py`), which is why this audit closes negative. **The gauge sectors were protected by a finding written for a different symmetry.**

---

## What this does not establish

- **It does not revive the transpose photon.** The Cartan form fixes covariance and the amplitude; it does not touch the reason F69 retired the construction, which is the helicity↔branch birefringence excluded by GRB/AGN polarimetry (F65–F67). The canonical photon builds no bilinear at all.
- **Boosts are a separate question.** `bilinear.py:951-968` already documents a scalar $(0,0)$ contamination of the transpose bilinear under boosts. Whether $\varepsilon$ repairs the boost channel too — $\varepsilon$ is the SL(2,ℂ) invariant tensor as well, so the algebra suggests yes — was not tested here.
- **No sector was changed.** This is a measurement of what the tree already does. `bilinear_G` was left exactly as it is: it is the historical record of the retired photon, and rewriting it would falsify the F65–F67 falsification record.
- **The audit is over the sectors named in `S1-F69` plus their neighbours.** It does not sweep the particle sector, where `baryon.py`'s $\varepsilon^{abc}$ is an unrelated colour contraction.

---

## What would falsify this

The algebraic core is an identity and cannot be falsified by measurement; the audit can be, in two ways. **Either** a live consumer of `bilinear_G` is found outside the retired-photon diagnostics and the fork harnesses listed above — the `sector_audit()` entry point encodes that list, and check C6 fails if a sector is added to it with `form: transpose`. **Or** a future W/Z/gluon construction is written with a transpose contraction, in which case its SO(3) residual will be O(1) rather than $10^{-16}$ and C3 fails. The gate record makes both failures loud.
