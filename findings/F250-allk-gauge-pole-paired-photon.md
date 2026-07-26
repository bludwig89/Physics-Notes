# F250 — The all-k gauge pole of the dual-spinor (paired) photon: a single massless transverse pole across the whole Brillouin zone

**Date:** 2026-07-16 - 08:56
**Status:** Confirmed — 8/8 checks PASS. Pole location, Ward commutator, and massless anchor are **algebraically exact** (residual literal 0); residue rank, eigenphases, unitarity/completeness, and the independent-projector cross-check hold to machine precision ($\le7\times10^{-16}$). The doubler scan finds a **single** BZ zero (at $k=0$).
**Module:** none new (analytic proof + verification harness over the audited `ca_photon_pair` even-law propagator and the `ca_bcc` walk)
**Verification script:** `tests/findings/test_F250_allk_gauge_pole.py`
**Result file:** `test-results/F250_allk_gauge_pole.json`
**Cross-references:** [[F69-paired-spinor-photon]] (the even-law propagator this analyses), [[F68-minimal-coupling-forces-even-photon]] (the U(1) identity channel), [[F168-paired-photon-binding-gauge-protected]] (why the pole is massless/gauge-protected), [[F169-photon-interacting-two-body-wavefunction]] (the $O(k^2)$ two-body-floor refinement, scoped below), [[F105-axial-photon-exactly-dispersionless]] (axis-aligned exactness), [[F87-charge-coupling-paired-photon]], [[F26-speed-of-light-as-rotation-rate]]; McPhee notebook pp.5–6.

---

## The claim

The dual-spinor photon (F69) propagates each Fourier mode by the **even-law** $SO(2)$ rotation of the real $(\mathbf E,\mathbf B)$ pair at rate

$$\Omega_\text{pair}(k)=\omega^+(k/2)+\omega^-(k/2),\qquad \omega^\pm(q)=\arccos\big(c_xc_yc_z\pm s_xs_ys_z\big),$$

applied **identically in every Cartesian polarisation component** (`ca_photon_pair.photon_step_spectral`). Written on the 6-vector field $(\mathbf E,\mathbf B)=(E_x,E_y,E_z,B_x,B_y,B_z)$ the one-tick evolution is the block operator

$$M_6(k)=M_2(\Omega_\text{pair})\otimes \mathbb I_3,\qquad M_2(\Omega)=\begin{pmatrix}\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{pmatrix}.$$

The discrete-time photon propagator is the resolvent $G(z,k)=\big(z\,\mathbb I-M_6(k)\big)^{-1}$ with $z=e^{i\omega_\text{freq}}$. The **all-k gauge pole** claim is:

> For **every** $k$ in the first Brillouin zone — not merely in the $k\to0$ continuum limit — $G(z,k)$ has a single simple **massless** pole at $\omega_\text{freq}=\pm\Omega_\text{pair}(k)$ whose residue is the **transverse (2-polarisation) gauge projector**, with no longitudinal/scalar pole and no fermion-doubler copy.

This is the lattice statement of "the photon is a massless spin-1 gauge boson", promoted from the usual $k\to0$ (long-wavelength) reduction to an exact statement valid across the entire BZ.

---

## The proof

### 1. Pole location, all k (GP1) — exact

$M_2(\Omega)=e^{\Omega J}$ with $J=\begin{psmallmatrix}0&1\\-1&0\end{psmallmatrix}$, so its eigenvalues are **exactly** $e^{\mp i\Omega}$ for any real $\Omega$. Hence

$$\det\!\big(e^{\pm i\Omega_\text{pair}(k)}\,\mathbb I_2-M_2\big)=0\quad\text{for all }k,$$

i.e. the resolvent has poles at $z=e^{\pm i\Omega_\text{pair}(k)}$, equivalently $\omega_\text{freq}=\pm\Omega_\text{pair}(k)$. This is an algebraic identity (rotation spectrum), not a $k\to0$ expansion; verified to $1.1\times10^{-16}$ over 4000 random BZ points. The poles are **simple** wherever $\sin\Omega_\text{pair}\neq0$ (distinct eigenvalues), which holds everywhere in the open BZ except the single point $k=0$ (see §5).

### 2. Massless anchor (GP2) — exact

The pole sits at zero frequency at $k=0$:

$$\Omega_\text{pair}(0)=\omega^+(0)+\omega^-(0)=\arccos 1+\arccos 1=0\quad\text{(literal 0).}$$

This is the pure-hop ($A_0=0$) gaplessness of [F168](F168-paired-photon-binding-gauge-protected.md)/B1, inherited by the pair. The pole is anchored to zero mass, and by the gauge-protection argument of F168 (the U(1) identity vertex $e^{i\theta}\mathbb I$ carries **no** branch-coupling $X$ component, the only object that can open a gap) no mass term can be induced at any $k$: the pole branch stays gapless across the whole BZ. Masslessness is structural, not tuned.

### 3. Ward identity / transverse invariance (GP3) — exact

Because $M_6=M_2\otimes\mathbb I_3$ acts as a **scalar in Cartesian polarisation space**, it commutes with the transverse projector $P_T(k)=\mathbb I_3-\hat k\hat k^{\!\top}$ (extended to both $\mathbf E$ and $\mathbf B$ blocks):

$$\big[\,M_6(k),\;P_T(k)\otimes\mathbb I_2\,\big]=0\qquad\text{(residual literal 0, all }k).$$

So the physical transverse subspace $\{\,\hat k\cdot\mathbf E=0,\ \hat k\cdot\mathbf B=0\,\}$ is a **dynamically invariant** eigenspace of the propagator at every $k$: a transverse field stays transverse, and the source-free Gauss constraint $\nabla\!\cdot\!\mathbf E=0$ is preserved. This is the lattice Ward identity — the gauge (transverse) sector never leaks into the longitudinal/scalar sector.

### 4. Transverse residue = the 2-polarisation gauge projector (GP4) — machine

The residue of $G$ at $z=e^{-i\Omega}$ is the eigenprojector $P_-=\dfrac{M_6-e^{+i\Omega}\mathbb I}{e^{-i\Omega}-e^{+i\Omega}}$, of rank 3 (one copy per Cartesian axis). Projecting onto the transverse subspace,

$$R_T(k)=\big(P_T\otimes\mathbb I_2\big)\,P_-\,\big(P_T\otimes\mathbb I_2\big),$$

has **rank exactly 2** — the two physical photon polarisations — and satisfies the **Ward contraction** $\hat k\cdot R_T=0$ ($\le9.3\times10^{-17}$). The one remaining Cartesian direction is longitudinal ($\parallel\hat k$); on the source-free constraint surface it is non-dynamical and carries no physical pole. So the gauge-pole residue is the transverse projector — two massless propagating states, no third (scalar/longitudinal) photon — for all $k$.

### 5. Unitarity, spectral weight, and no ghost (GP5, GP6) — machine

An independent dense diagonalisation of the real $6\times6$ $M_6$ returns eigenphases $=\pm\Omega_\text{pair}(k)$ to $4.4\times10^{-16}$ (GP5; no `eig` on chiral matrices — $M_6$ is real orthogonal). $M_6M_6^{\!\top}=\mathbb I$ to $2.2\times10^{-16}$ (unitary), and the two eigenprojectors are complete, $P_++P_-=\mathbb I$, to $1.1\times10^{-16}$ (GP6). The pole therefore carries **residue weight 1** (no wavefunction renormalisation, $Z=1$) and the spectral function is the clean single-particle pair $\rho(\omega,k)=\delta(\omega-\Omega_\text{pair})+\delta(\omega+\Omega_\text{pair})$ in the transverse channel — no ghost, no continuum. A second, fully independent construction of the residue (eigenvector outer product vs closed-form projector, GP8) agrees to $7.2\times10^{-16}$.

### 6. A single gauge pole — the pairing folds out the doublers (GP7)

Scanning $\Omega_\text{pair}(k)$ on a $61^3$ grid over the photon BZ $[-\pi,\pi]^3$ finds $\min\Omega_\text{pair}=0$ attained at **exactly one** point, $k=0$; all corners/faces/edges are gapped ($\Omega_\text{pair}(\pi,\pi,\pi)=2.59$, $(\pi,0,0)=1.81$, $(\pi,\pi,0)=2.36$). The mechanism is the $k/2$ momentum sharing: the constituent Weyl walk $\omega^\pm$ has its extra zeros (doublers) on the **constituent** BZ boundary $\lvert q_i\rvert=\pi$, but the photon evaluates its constituents at $q=k/2$, so as $k$ sweeps the photon BZ the constituents only reach $\lvert q_i\rvert\le\pi/2$ — the interior half, containing the single Weyl point $q=0$. The doubler copies are pushed to photon momentum $\lvert k_i\rvert=2\pi$, **outside** the photon BZ. So the paired photon has one gauge pole, not $2^d$ — the same pairing that makes it non-birefringent (F69) and gauge-protected (F168) also removes fermion doubling from the gauge sector.

---

## Verification summary (8/8)

Script `tests/findings/test_F250_allk_gauge_pole.py`; results `test-results/F250_allk_gauge_pole.json`. Closed-form $\arccos(u)$ dispersion + real linear algebra only (no `np.linalg.eig` on chiral matrices, CLAUDE.md).

| # | Check | Type | Result |
|---|-------|------|:------:|
| GP1 | Pole location all $k$: $\det(e^{\pm i\Omega}\mathbb I-M_2)=0$ (4000 BZ pts) | exact | $1.1\times10^{-16}$ |
| GP2 | Massless anchor $\Omega_\text{pair}(0)=0$ | exact | $0$ |
| GP3 | Ward / transverse invariance $[M_6,P_T\!\otimes\!\mathbb I_2]=0$ | exact | $0$ |
| GP4 | Residue transverse rank $2$, full rank $3$, $\hat k\!\cdot\!R_T=0$ | machine | rank exact; Ward $9.3\times10^{-17}$ |
| GP5 | Eigenphases (independent diag) $=\pm\Omega_\text{pair}$ | machine | $4.4\times10^{-16}$ |
| GP6 | Unitary $M_6M_6^{\!\top}=\mathbb I$; completeness $P_++P_-=\mathbb I$ | machine | $2.2\times10^{-16}$ / $1.1\times10^{-16}$ |
| GP7 | Single gauge pole: unique BZ zero at $k=0$ (no doubler) | quantitative | 1 zero, $\min=0$ |
| GP8 | Independent residue (eigvec vs closed form) | machine | $7.2\times10^{-16}$ |

Also recovered: $\Omega_\text{pair}/\lvert k\rvert\to1/\sqrt3=0.5773503$ (luminal massless slope).

---

## Scope and honesty

- **This is a statement about the even-law propagator** — the field that actually propagates in `ca_photon_pair` and that minimal coupling forces as the U(1) identity channel (F68). The pole law $\Omega_\text{pair}(k)$ is exact by construction/forcing at all $k$; the proof establishes that this propagator's analytic structure is a single massless transverse pole across the BZ.
- **Relation to F169's $O(k^2)$ refinement.** [F169](F169-photon-interacting-two-body-wavefunction.md)/C3 showed that the symmetric split $p=0$ is not the exact *two-body continuum floor* $T(k)=\min_p[\omega^+(k/2+p)+\omega^-(k/2-p)]$ at finite $k$: $\Omega_\text{pair}(k)-T(k)=O(k^2)\ge0$. That refinement concerns where the free two-constituent continuum bottom sits, **not** the gauge propagator's pole: the EM channel rides $\Omega_\text{pair}$ by the F168 gauge/identity structure (it sits *at* the identity-channel rate, which is why it is non-birefringent), so the gauge pole is at $\Omega_\text{pair}(k)$ at all $k$ by the same protection that pins it at threshold. The two statements are consistent: F250 is the propagator pole; F169 is the free-continuum floor beneath it.
- **What is exact vs machine.** Pole location, massless anchor, and the Ward commutator are algebraic identities (literal 0). Residue ranks are integer-exact; the residue magnitudes, eigenphases, unitarity/completeness, and the cross-check are at the float/FFT floor.
- **Not addressed here.** The interacting (loop-corrected) photon self-energy and any radiative shift of the residue — the free/tree propagator is what carries the gauge pole; interactions are the F87/charge-coupling and self-energy program (F155/F162), out of scope.

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| [F69](F69-paired-spinor-photon.md) | Supplies the even-law propagator $\Omega_\text{pair}=\omega^+(k/2)+\omega^-(k/2)$; F250 proves its pole is a single massless transverse gauge pole for all $k$. |
| [F68](F68-minimal-coupling-forces-even-photon.md) | The U(1) identity channel; F250's transverse-rank-2 residue is that channel's polarisation content realised at all $k$. |
| [F168](F168-paired-photon-binding-gauge-protected.md) | Gauge protection of $\Omega(0)=0$; F250 upgrades it to the massless *anchor of the propagator pole* and shows no gap opens across the BZ. |
| [F169](F169-photon-interacting-two-body-wavefunction.md) | The $O(k^2)$ two-body-floor refinement; F250 clarifies it does not move the gauge pole. |
| [F105](F105-axial-photon-exactly-dispersionless.md) | Axis-aligned exact $\lvert k\rvert/\sqrt3$; consistent with the gapless single pole here. |

---

## Files
- Test: `tests/findings/test_F250_allk_gauge_pole.py`
- Results: `test-results/F250_allk_gauge_pole.json`
- Propagator under analysis: `ca-simulation/ca_photon_pair.py` (`pair_dispersion`, `photon_step_spectral`)
