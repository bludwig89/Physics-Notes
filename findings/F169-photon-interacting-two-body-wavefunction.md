# F169 — The photon's interacting two-body wavefunction: a normalizable threshold bound state whose masslessness is inherited from gapless constituents

> **[SUB-CLAIM SUPERSEDED 2026-09-22 by F397 — ledger S24-F169-C3-threshold-search-replaced-by-closed-form]**
>
> **DEAD:** C3's quoted fit exponent 2.10, and the use of a stochastic search to obtain T(k) at all.
>
> **STILL LIVE:** EVERYTHING ELSE. C1 (threshold wavefunction in closed form, normalizable), C2 (g_c finite and positive), C4 (two-method agreement 5.6e-14), C5 (masslessness inherited from gapless constituents; T(0) = 0 exactly), C6 (finite RMS radius) are untouched -- all are statements at k = 0, or at fixed finite k about the secular problem, and none used the search. C3's QUALITATIVE content also stands: Omega_even >= T(k), the symmetric split is not the exact two-body floor at finite k, and F69's even law is the photon's leading dispersion, exact only as k -> 0. Only the number moved.
>
> **NOTE:** A third error was found in the same file and fixed in the same edit: the module docstring of photon_bound_state.py asserted 'for small k the continuum bottom sits AT the symmetric split p = 0, so T(k) = Omega_even(k) exactly', which is false and contradicted F169's own C3. A FOURTH was found 2026-09-22 while re-running the suite, and is DOCUMENTED RATHER THAN REPAIRED (F169 'C2/C4-note'): critical_coupling and threshold_wavefunction take T = E.min() on the L^3 grid, which is exact at k = 0 (floor at p = 0, a grid point, T = 0) but at finite k is a grid artifact lying between the closed-form floor and Omega_even, non-monotonically in L. It does not move any F169 conclusion -- C1/C2/C5/C6 are at k = 0, and C4 is a two-method agreement on the SAME H where T only sets an arbitrary scale -- but the finite-k g_c must not be read as the marginal coupling. Repair is a physics change and needs its own finding.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*

**Date:** 2026-06-29 - 17:55
**Status:** Confirmed (the interacting wavefunction is built) — 6/6 checks PASS (secular residual exactly 0; two-method agreement $5.6\times10^{-14}$; $T(0)=0$ exact). Builds the explicit two-constituent bound-state wavefunction that [F69](F69-paired-spinor-photon.md)/[F74](F74-two-constituent-bound-state-binding.md)/[F168](F168-paired-photon-binding-gauge-protected.md) deferred. The binding *coupling value* (criticality) remains the one external input, as in F74. **Corrected 2026-09-22 (C3 only):** the quoted fit exponent $2.10$ was stochastic-search noise; $T(k)$ and the offset $\Omega_\text{even}-T$ now have closed forms (converged exponent $2.007$). C1, C2, C4, C5, C6 are unchanged. Test re-run 6/6 PASS.
**Module:** `ca-simulation/ca_photon_bs.py`
**Verification script:** `tests/findings/test_F169_photon_bound_state.py`
**Result file:** `test-results/F169_photon_bound_state.json`
**Cross-references:** [[F168-paired-photon-binding-gauge-protected]] (the protection argument this realizes as a wavefunction), [[F69-paired-spinor-photon]] (the kinematic pair, now the leading small-k form), [[F74-two-constituent-bound-state-binding]] (the scalar sibling + the two-method standard + g_c/Watson), [[F73-spin0-bound-pair-scalar]], [[F26-speed-of-light-as-rotation-rate]], [[F46-pythagorean-lattice-mass]], [[F397-notebook-factorization-route-pp176-182]] (the 2026-09-22 C3 correction and the closed-form offset), [[F30-photon-dispersion-order-anisotropy-birefringence]] (the $(111)$ chiral term); McPhee notebook pp.5–6.

---

## Goal

[F168](F168-paired-photon-binding-gauge-protected.md) argued the photon-pair's zero binding energy is gauge-protected, but closed with one outstanding build: *"a full interacting two-body kernel that produces the marginal pole … the relativistic Bethe–Salpeter build flagged in F74."* This finding constructs the **explicit interacting two-body bound-state wavefunction** and shows the photon is the *marginally-bound threshold state* of a genuine two-constituent problem — not a kinematic sum — with its masslessness inherited from the gapless constituents.

## Construction

In the relative-momentum coordinate $p$ of the two Weyl constituents (one on the $+$ branch at $k/2+p$, one on the $-$ branch at $k/2-p$, total momentum $k$), the free two-body dispersion is

$$E_0(p;k)=\omega^+(k/2+p)+\omega^-(k/2-p),\qquad T(k)\equiv\min_p E_0(p;k),$$

and the F69 paired photon is the symmetric member $p=0$, energy $\Omega_\text{even}(k)=\omega^+(k/2)+\omega^-(k/2)$. A single attractive contact in the relative coordinate (the lattice ladder / NJL contact; the $\sigma$-sibling is [F74](F74-two-constituent-bound-state-binding.md)) binds the pair. Because the contact is rank-1, the bound state is the exact root of the Koster–Slater secular equation

$$1=g\left\langle\frac{1}{E_0(p;k)-E_b}\right\rangle_\text{BZ},\qquad E_b<T(k),\qquad \psi_k(p)\propto\frac{1}{E_0(p;k)-E_b}.$$

The **photon is the marginally-bound threshold state** $E_b\to T(k)$ at the critical coupling $g_c(k)=1/\langle1/(E_0-T)\rangle_\text{BZ}$.

## Results

**C1 — The threshold wavefunction exists in closed form and is normalizable.** At $k=0$, $\psi_0(p)\propto1/E_0(p;0)$ is the *exact* $E=0$ secular solution at $g=g_c$ (residual identically $0$), and $\sum|\psi|^2$ is finite — the photon is a genuine normalizable zero-energy bound state. Normalizability is the same 3-D Watson finiteness ($\int d^3p/\omega^2\sim\int d^3p/p^2$ converges) that makes $g_c$ finite.

**C2 — There is a real 3-D binding threshold.** $g_c=2.2596$ (on the $L=12$ relative grid) is finite and positive: a minimum coupling is required to bind (the F74 Watson result, here in the photon channel), not "binds for any attraction."

**C3 — Massless, luminal, and F69 is the leading small-k form.** *(Corrected 2026-09-22 — see §C3-correction. The originally quoted fit exponent 2.10 was search-noise; the threshold and the offset both have closed forms.)* The threshold state is massless and luminal — light speed $\Omega_\text{even}/|k|\to1/\sqrt3=0.57734$ — and $\Omega_\text{even}(k)$ is the **leading small-$k$ form** of the true threshold. The two-body floor is **exact, not searched**:

$$T(\mathbf k)=\min\bigl(\omega^+(\mathbf k),\ \omega^-(\mathbf k)\bigr),$$

attained at the **collinear endpoint** $p=\pm\mathbf k/2$ — one constituent carries all of $\mathbf k$, the other carries zero, and $\omega^\pm(0)=\arccos 1=0$ identically. The offset of the symmetric split above it also has a closed form:

$$\boxed{\ \Omega_\text{even}(\mathbf k)-T(\mathbf k)=|\varepsilon(\mathbf k)|+O(k^3)=\frac{|k_xk_yk_z|}{3|\mathbf k|}+O(k^3)\ }$$

with $\varepsilon$ the odd, degree-2-homogeneous chiral term in $\omega^\pm(\mathbf q)=c|\mathbf q|\pm\varepsilon(\mathbf q)+O(q^3)$, $\varepsilon(\mathbf q)=-q_xq_yq_z/(3|\mathbf q|)$ ([F397](F397-notebook-factorization-route-pp176-182.md) R6; the $(111)$ case is in [F30](F30-photon-dispersion-order-anisotropy-birefringence.md)). Measured ratio to $|\varepsilon|$: $1.0084$ at $|k|=0.05$ and $\to1$ as $|k|\to0$; converged exponent **2.007** on $|k|\in[0.0125,0.1]$ along $(111)$. The offset is **direction-dependent** and vanishes on the coordinate planes, where it drops to $O(k^3)$ — it is *not* a single universal $k^2$ law.

Honest refinement of F69: the symmetric split $p=0$ is *not* the exact two-body floor at finite $k$ (its gradient is $O(k)$); it sits $O(k^2)$ above the true minimum — the same order as the F168/B3 birefringent split. F69's even law is therefore the photon's leading dispersion, exact only as $k\to0$.

**C3-correction (2026-09-22).** The original C3 obtained $T(k)$ from `true_threshold`, a local stochastic descent starting at $p=0$ with a decaying step. The true minimum is at the collinear *endpoint*, far from $p=0$ in relative momentum, along a valley that is **flat at leading order** — so the descent had nothing to follow and under-converged badly at small $|k|$: measured ratios to $|\varepsilon|$ of $1.043,\,0.986,\,0.876$ at $|k|=0.1,0.05,0.025$, and in a generic direction such as $(321)$ it returned *no improvement at all* over $\Omega_\text{even}$ at $|k|=0.025$. The quoted exponent **2.10 was therefore a fit to search noise, not physics**, and is withdrawn in favour of the closed forms above. The endpoint value is exact: at 60-digit precision $E_0(\mathbf k,\mathbf k/2)-\min_b\omega^b(\mathbf k)$ is identically $0$, and a deterministic coordinate pattern search from five starts, 2M random BZ points and Nelder–Mead from the zero-energy BZ nodes find nothing below it (F397). `casim.engine.gauge.photon_bound_state` now exposes `threshold_closed_form` and `threshold_offset_closed_form`; `true_threshold` defaults to the closed form, with `method="stochastic"` retained only to reproduce this correction. The module docstring's claim that "for small k the continuum bottom sits AT the symmetric split $p=0$, so $T(k)=\Omega_\text{even}(k)$ exactly" was false and is corrected in the same edit.

**C3-note — what sits at the threshold.** Because $T(\mathbf k)$ is attained where one constituent carries all of $\mathbf k$ and the other carries none, the configuration *at* the floor is not the symmetric spin-1 pair: the spin-1 identification lives at $p=0$, **above** $T$ by $|\varepsilon(\mathbf k)|$. This does not affect C1/C2/C4/C5/C6 — all of which are statements at $k=0$ or at fixed finite $k$ about the secular problem, where $T(0)=0$ exactly and the $k=0$ threshold state *is* the symmetric one — but it does mean the phrase "the photon is the marginally bound threshold state" is exact only at $\mathbf k=0$ and leading order in $k$. Flagged by [F397](F397-notebook-factorization-route-pp176-182.md); the physical resolution is [F250](F250-allk-gauge-pole-paired-photon.md)/[F168](F168-paired-photon-binding-gauge-protected.md) — the EM channel rides $\Omega_\text{even}$ by the gauge/identity structure, so the gauge pole does not descend to the free-continuum floor.

**C2/C4-note — the finite-$k$ grid threshold is an artifact (found 2026-09-22 while re-running the suite after the C3 fix; *not* caused by it).** `critical_coupling` and `threshold_wavefunction` take $T$ as `E.min()` over the $L^3$ relative grid. **At $k=0$ this is exact** — the floor is at $p=0$, which *is* a grid point, and $T(0)=0$ identically — so **C1, C2, C5, C6 and the quoted $g_c=2.2596$ are unaffected.** At *finite* $k$ the true floor is at the collinear endpoint $p=\pm\mathbf k/2$, generally not a grid point, and the grid value is an artifact lying somewhere between the closed-form floor and $\Omega_\text{even}$, **non-monotonically in $L$**. Measured fraction of the offset still missed at $|k|=0.2$ along $(111)$: $1.00,\,1.00,\,1.00,\,1.00,\,0.36,\,0.25,\,0.36$ at $L=12,24,32,48,96,144,192$ — it does not converge cleanly over that range, because $E_0$ carries several near-degenerate minima and which grid point wins depends on commensurability with the narrow valley. Nothing ever falls *below* the closed form, consistent with F397's exhaustive search.

**This does not move C4's conclusion.** C4 compares two diagonalisations of the *same* $H=\mathrm{diag}(E_0)-g|c\rangle\langle c|$; $T$ enters only through the arbitrary scale $g=1.5\,g_\text{loc}$. The two-method agreement at $5.6\times10^{-14}$ tests the **solver**, and remains valid. What is *not* warranted is reading the finite-$k$ `critical_coupling` output as the marginal coupling, or the finite-$k$ $T$ as the continuum threshold. The test now records `offset_fraction_missed` and `grid_never_below_closed_form` so the artifact is visible rather than silent, and the module docstrings carry the caveat.

**Deliberately not repaired.** Substituting the closed-form $T$ at finite $k$ would change $g_c$ and every quantity scaled by it — a physics change, not a bug fix. It belongs in a finding of its own, with its own review pass.

**C4 — The solver is exact.** At finite total momentum ($|k|=0.4$, clean gap), the secular root and an independent dense Hermitian diagonalisation of $H=\mathrm{diag}(E_0)-g\,|c\rangle\langle c|$ agree to $5.6\times10^{-14}$ — the F74 two-method standard, now in the photon channel.

**C5 — Masslessness is inherited from the gapless constituents, not tuned.** $T(0)=\omega^+(0)+\omega^-(0)=0$ **exactly** (pure-hop $A_0=0$, [F168](F168-paired-photon-binding-gauge-protected.md)/B1). The photon's $E_b=0$ is the gaplessness of its constituents: the two-body continuum bottom is pinned at $0$, so any threshold bound state there is massless. The coupling sets *whether* a marginal state exists (criticality $g_c$); the *masslessness* is the constituent gaplessness, independent of the coupling value. The EM channel sits **at** threshold — not below (which would be tachyonic at $k=0$, since the continuum bottom is $0$) — by the gauge/identity structure of F168.

**C6 — The pair has a finite size.** The threshold wavefunction has real-space RMS relative radius $\approx1.91$ lattice units: an explicit, localized, finite-size bound pair, not a point or a delocalized scattering state.

---

## Verification summary

Module `ca-simulation/ca_photon_bs.py`; script `tests/findings/test_F169_photon_bound_state.py`; results `test-results/F169_photon_bound_state.json`. Closed-form $\arccos(u)$ dispersion + real linear algebra; own bisection root-finder (no scipy); no `eig` on chiral matrices.

| # | Check | Type | Result |
|---|-------|------|:------:|
| C1 | $\psi_0\propto1/E_0$ is exact $E{=}0$ secular root at $g_c$; normalizable | exact (residual $0$) | PASS |
| C2 | $g_c$ finite (3-D Watson binding threshold) | quantitative | PASS |
| C3 | massless, luminal $1/\sqrt3$; $\Omega_\text{even}-T=O(k^2)\ge0$ | quantitative | PASS |
| C4 | secular root $=$ dense diagonalisation (solver exact) | machine ($5.6\times10^{-14}$) | PASS |
| C5 | $T(0)=\omega^\pm(0)=0$ — masslessness inherited from gapless constituents | exact | PASS |
| C6 | finite real-space RMS radius (localized pair) | quantitative | PASS |

---

## Verdict — what this closes, and what remains

**Built (this finding).** The interacting two-body wavefunction is no longer a deferred item: the photon is realised as an explicit, normalizable, *marginally-bound threshold* state of a genuine two-constituent bound-state problem (C1, C4, C6), with masslessness **inherited from the gapless constituents** rather than tuned (C5), and with the F69 even law recovered as its leading small-$k$ dispersion (C3). Together with [F168](F168-paired-photon-binding-gauge-protected.md) (why the channel sits at threshold and not below/above), the binding is now both *explained* (gauge-protected) and *exhibited* (a wavefunction).

**Still external (one input, unchanged since F74).** The binding **coupling value** — why the EM channel sits exactly at criticality $g_c$ — is not derived from first principles here; it is the same external strong-contact input F74 isolated. F168 gives the structural reason the marginal (threshold) point is the gauge-consistent one, but a derivation of $g=g_c$ from the U(1) minimal coupling is open.

**Still open (harder builds).**
- A fully **gauge-invariant polarization-tensor** demonstration of the protected massless pole over *all* $k$ (the Ward/transversality route): the naive single-cone f-sum does not cleanly cancel at the gapless Weyl point, so this needs the proper regularised treatment — not done here.
- A **relativistic Bethe–Salpeter / ladder** treatment with the full [F46](F46-pythagorean-lattice-mass.md) dispersion (deep-binding and large-$k$); the present solver is a contact ladder in the relative coordinate, quantitative near threshold.

Net for audit G2: from *"binding is kinematic, mechanism unknown"* (original) → *"zero binding energy is gauge-protected"* (F168) → *"the photon is an explicit normalizable threshold bound state whose masslessness is inherited from gapless constituents; only the coupling value (criticality) and the all-$k$ gauge-pole proof remain"* (this finding).

---

## Relationship to prior findings

| Finding | Connection |
|---------|-----------|
| [F168](F168-paired-photon-binding-gauge-protected.md) | Gave the protection argument (threshold, not below/above); F169 realizes it as a normalizable bound-state wavefunction and ties $E_b=0$ to $T(0)=0$. |
| [F69](F69-paired-spinor-photon.md) | The kinematic pair $\Omega_\text{even}$ is recovered as the leading small-$k$ threshold dispersion; F169 refines it ($\Omega_\text{even}-T=O(k^2)$). |
| [F74](F74-two-constituent-bound-state-binding.md) | Same solver standard (two-method, Watson $g_c$) in the photon channel; the scalar sibling is below-threshold-tunable, the photon is the protected threshold. |
| [F46](F46-pythagorean-lattice-mass.md) | The dispersion map underlying a future relativistic Bethe–Salpeter upgrade. |

---

## Files

- `findings/F169-photon-interacting-two-body-wavefunction.md` — this finding
- `ca-simulation/ca_photon_bs.py` — the two-body bound-state solver
- `tests/findings/test_F169_photon_bound_state.py` — C1–C6 verification
- `test-results/F169_photon_bound_state.json` — numerical output

---

*End of finding.*
