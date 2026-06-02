# F65 — The two photon helicities map onto the two BCC chiral branches, and the map is dynamically forced (birefringence is physical, not optional)

**Date:** 2026-06-01 - 02:25
**Status:** Confirmed — independent from-scratch reproduction of the F37/F39 identification, plus the new "forced vs optional" result. 4/4 sections PASS (residuals 0, 0, 4.5×10⁻⁵, ≤4.4×10⁻¹⁶).
**Script:** `model-tests/test_F65_helicity_chirality_map.py` (self-contained; closed-form 2×2 Weyl unitary + (E,B) rotation, no numpy chiral eig per CLAUDE.md).
**Cross-references:** [[F37-rs-bcc-chirality-helicity]] (algebraic identification), [[F39-two-helicity-photon-bilinear]] (bilinear bridge), [[F30-photon-dispersion-order-anisotropy-birefringence]] (the −√3/27 coefficient), [[F26-speed-of-light-as-rotation-rate]], [[F64-em-connection-gravity]] / `si-units-options.md` (the cell-size anchor this confronts).

---

## The question

F30 left open: *do the two physical photon helicities — the Riemann–Silberstein (RS) eigenstates $\mathbf F^\pm = \mathbf E \pm i\mathbf B$ — correspond to the two BCC Weyl chirality branches $\Omega^\pm(k)=2\omega_\pm(k/2)$?* If yes, the model predicts **linear vacuum birefringence**; once the cell size $a$ is pinned (F64: $a\approx6.2\times10^{-35}$ m), that prediction becomes a hard, confrontable number. F37 proved the *algebraic* identification and F39 built the two-branch bilinear, but both left a genuine ambiguity: the **even-dispersion** law $\Omega_\text{even}=(\Omega^++\Omega^-)/2$ *also* preserves Hermitian symmetry (it was the original `_f26_rotation_step`), so reality of $(\mathbf E,\mathbf B)$ alone does **not** decide between a birefringent and a non-birefringent photon. F65 settles which law the model's own construction forces.

## What the test shows (4/4)

**A — RS eigenstates are exactly the (E,B)-rotation eigenvectors, and physical helicity projects onto them. [exact, residual 0]**
The $2\times2$ field rotation $R(\Omega)=\begin{pmatrix}\cos\Omega&\sin\Omega\\-\sin\Omega&\cos\Omega\end{pmatrix}$ has eigenvectors $(1,\mp i)^T$ with eigenvalues $e^{\mp i\Omega}$, i.e. $\mathbf F^\pm=\mathbf E\pm i\mathbf B$. A right-circular wave ($\mathbf B=-i\mathbf E$) gives $\mathbf F^-=0$; left-circular ($\mathbf B=+i\mathbf E$) gives $\mathbf F^+=0$. Residual $0$ (machine zero). So helicity $\leftrightarrow$ RS eigenstate is an exact identity, independent of dispersion.

**B — Parity $\omega_+(-k)=\omega_-(k)$ holds exactly. [max residual 0 over 2000 random $k$]**
This is the constraint (F37 Part 2) that makes the chiral assignment $\mathbf F^+\!\to\!\Omega^+,\ \mathbf F^-\!\to\!\Omega^-$ the *unique* Hermitian-symmetry-preserving one — **if** the helicities split at all.

**C — The branches genuinely differ off-axis. [rel err 4.5×10⁻⁵]**
Along the body diagonal $(1,1,1)$, $\Delta\Omega=\Omega^+-\Omega^- = c\,k^2$ with $c_\text{meas}=-0.0641529$ vs the F30 closed form $-\sqrt3/27=-0.0641500$. Zero along cube axes; quadratic along face diagonals; linear-in-$k$ phase-velocity split $\Delta v_\phi/c=-k/18$ along body diagonals.

**D — Decisive dynamical test: the map is realised and the split is forced. [phase residuals ≤4.4×10⁻¹⁶]**
A real, linearly polarized body-diagonal mode (carrying *both* helicities) is evolved two ways:
- **chiral law** (each RS eigenstate at its own branch — the honest two-branch Weyl-bilinear dynamics, and the model's actual propagator since F37 where `w_propagation_step_spectral = w_propagation_step_chiral`): $\mathbf F^+$ acquires phase $-\Omega^+ n$ and $\mathbf F^-$ acquires $+\Omega^- n$ to $\le4.4\times10^{-16}$. The two helicities accumulate **different** phase magnitudes, split $=|\Delta\Omega|\,n$ exactly.
- **even law** ($\Omega_\text{even}$ for both): the two helicities accumulate **identical** phase (split $=4.4\times10^{-16}\approx0$). No birefringence.

## Verdict

**Yes — the identification holds, it is realised in the model's propagator, and it is forced rather than optional.** Hermitian symmetry permits *both* laws (B guarantees the chiral law is consistent; the even law is trivially consistent), so reality does not decide. What decides is the model's foundational premise that the photon **is** a bilinear of the two BCC Weyl branches (F26/F29/F39): each branch carries its own dispersion $\omega^\pm$, so the RS components built from them inherit $\Omega^\pm$ and split. The even law replaces each helicity's true dispersion with the average — it has **no representation as an honest two-branch bilinear**. A generic linearly polarized photon populates both $\mathbf F^\pm$ (test A/D), so it is birefringent. The only escape — restricting real light to a single helicity or to a fine-tuned cancellation — contradicts observed linear polarization.

**Therefore the birefringence channel of F30 is a genuine physical prediction, not a gauge/convention artifact.**

## Observational consequence at the F64 cell size (the bite)

With $a=6.2\times10^{-35}$ m ($g_*=16$, one generation; F61/F64), the linear birefringence scale is $E_\text{QG}\simeq 9\,E_*=9\hbar c/a\approx 2.9\times10^{19}$ GeV $\approx 2.4\,E_\text{Planck}$. The helicity phase slip for a polarized $\gamma$-ray burst (~100 keV, $z\sim1$, $L\sim3$ Gpc) is

$$\Delta\phi \simeq \frac{E^2 L}{\hbar c\,E_\text{QG}} \approx 2\times10^{14}\ \text{rad},$$

which would completely depolarize the source. Yet GRBs are *observed* polarized at these energies, forcing $E_\text{QG}\gtrsim10^{33}$–$10^{36}$ GeV. **The model at this $a$ overshoots the birefringence by ~14–17 orders of magnitude** — unless the effect is suppressed by the lattice anisotropy (the split is zero along cube axes, maximal along body diagonals; a fixed lattice orientation makes this a direction-dependent, partially evadable signal, but only by O(1), not 14 decades).

So fixing $a$ via the gravity match (F64) and confirming the helicity↔chirality map (F65) together **close the escape hatch**: the model now makes a sharp linear-birefringence prediction that is in severe tension with polarimetry. The live options are (i) the lattice orientation / anisotropy story genuinely suppresses the accumulated rotation for observed sources (needs a quantitative all-sky calculation), (ii) the photon's RS content is constrained away from generic linear polarization by the bilinear structure (contradicted by test A/D as it stands), or (iii) the model is falsified at $a\approx6.2\times10^{-35}$ m. This is the highest-priority follow-up.

## Exact vs numeric

| Result | Tier | Residual |
|---|---|---|
| $R(\Omega)(1,\mp i)^T=e^{\mp i\Omega}(1,\mp i)^T$; RCP$\to\mathbf F^-=0$, LCP$\to\mathbf F^+=0$ | exact algebra | $0$ |
| $\omega_+(-k)=\omega_-(k)$ | machine | $0$ (2000 $k$) |
| $\Delta\Omega=-\sqrt3/27\,k^2$ along $(1,1,1)$ | quantitative fit | $4.5\times10^{-5}$ rel |
| chiral: $\mathbf F^+\!\to\!-\Omega^+$, $\mathbf F^-\!\to\!+\Omega^-$ | machine | $\le4.4\times10^{-16}$ |
| chiral split $=|\Delta\Omega|n$; even split $=0$ | machine | $\le4.4\times10^{-16}$ |

## Files
- Test: `model-tests/test_F65_helicity_chirality_map.py`
- Builds on `ca-simulation/ca_bcc.py` (`_bcc_uvec`, `bcc_dispersion`), `ca_wmu.py` (`w_propagation_step_chiral`), `ca_maxwell.py` (`riemann_silberstein_decomp`, two-helicity bilinear).
