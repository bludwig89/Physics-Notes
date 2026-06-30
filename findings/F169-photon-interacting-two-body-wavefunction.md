# F169 — The photon's interacting two-body wavefunction: a normalizable threshold bound state whose masslessness is inherited from gapless constituents

**Date:** 2026-06-29 - 17:55
**Status:** Confirmed (the interacting wavefunction is built) — 6/6 checks PASS (secular residual exactly 0; two-method agreement $5.6\times10^{-14}$; $T(0)=0$ exact). Builds the explicit two-constituent bound-state wavefunction that [F69](F69-paired-spinor-photon.md)/[F74](F74-two-constituent-bound-state-binding.md)/[F168](F168-paired-photon-binding-gauge-protected.md) deferred. The binding *coupling value* (criticality) remains the one external input, as in F74.
**Module:** `ca-simulation/ca_photon_bs.py`
**Verification script:** `tests/findings/test_F169_photon_bound_state.py`
**Result file:** `test-results/F169_photon_bound_state.json`
**Cross-references:** [[F168-paired-photon-binding-gauge-protected]] (the protection argument this realizes as a wavefunction), [[F69-paired-spinor-photon]] (the kinematic pair, now the leading small-k form), [[F74-two-constituent-bound-state-binding]] (the scalar sibling + the two-method standard + g_c/Watson), [[F73-spin0-bound-pair-scalar]], [[F26-speed-of-light-as-rotation-rate]], [[F46-pythagorean-lattice-mass]]; McPhee notebook pp.5–6.

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

**C3 — Massless, luminal, and F69 is the leading small-k form.** The threshold state is massless and luminal — light speed $\Omega_\text{even}/|k|\to1/\sqrt3=0.57734$ — and $\Omega_\text{even}(k)$ is the **leading small-$k$ form** of the true threshold:

$$\Omega_\text{even}(k)\;\ge\;T(k),\qquad \Omega_\text{even}(k)-T(k)=O(k^2)\ \ (\text{fit exponent }2.10).$$

Honest refinement of F69: the symmetric split $p=0$ is *not* the exact two-body floor at finite $k$ (its gradient is $O(k)$); it sits $O(k^2)$ above the true minimum — the same order as the F168/B3 birefringent split. F69's even law is therefore the photon's leading dispersion, exact only as $k\to0$.

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
