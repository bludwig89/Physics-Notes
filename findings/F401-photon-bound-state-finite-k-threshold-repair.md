# F401 — Repairing the photon's finite-k grid-threshold artifact: an exact axis identity, a sharply-reduced (not eliminated) commensurability artifact, and a direction-dependent finite-k critical coupling

**Date:** 2026-09-23 - 21:45
**Status:** Confirmed — 5/5 gate legs PASS, one declared negative control verified sound (flips exactly the leg it targets).
**Reviewed:** 2026-09-23 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F401-review-2026-09-23.md)) — the axis identity, the k=0 invariance, and the (111)/(3,1,1) decreasing-$g_c(k)$ trend (extended to $|k|=1.0$) all independently re-derived and confirmed; one real overclaim found and fixed in-session: "clean, monotonic convergence... at every step" held only at F169's own 7 quoted $L$ values, not at a denser scan (a real, mechanistically-understood commensurability dip persists, e.g. at $L=92$) — narrowed to a quantified worst-case-severity reduction (~4x smaller backslide than the grid version); and "along a generic direction" was found to imply more than is true — $(2,1,0)$ is a genuine counterexample to the decreasing trend, so the result is now scoped to the $(111)$/$(3,1,1)$-class of directions actually checked, not generic directions universally.
**Module:** `src/casim/engine/gauge/photon_bound_state_finite_k.py` (extends `src/casim/engine/gauge/photon_bound_state.py`, which gains a new `threshold=` parameter — default unchanged)
**Test record:** `F401-photon-bound-state-finite-k` (gate, quantitative)
**Results:** `test-results/F401_photon_bound_state_finite_k.json`
**Claim:** CL313
**Cross-references:** [[F169-photon-interacting-two-body-wavefunction]] (the finding whose own "C2/C4-note" and docstring named this artifact and deferred its repair), [[F397-notebook-factorization-route-pp176-182]] (the closed-form $T(k)$ and offset $|\varepsilon(k)|$ this finding builds on), [[F168-paired-photon-binding-gauge-protected]], [[F250-allk-gauge-pole-paired-photon]] (why the physical photon rides $\Omega_\text{even}(k)$, not $T(k)$ — the reason this finding's scope stops short of "the photon's own coupling at finite k"); `docs/theory/notebook-followup-2026-09-22.md` Part VI.3 (first documented the artifact); `docs/theory/notebook-v2/index.md` §5 Prompt E (the question this answers).

---

## The question

F169's construction of the photon as an interacting two-body threshold bound state uses `critical_coupling`/`threshold_wavefunction` (`casim.engine.gauge.photon_bound_state`), which take the two-body continuum floor $T$ as `E.min()` over a finite $L^3$ relative-momentum grid. F169's own "C2/C4-note" and `docs/theory/notebook-followup-2026-09-22.md` Part VI.3 documented — but explicitly did not repair — that this is exact only at $k=0$ (where the floor sits at $p=0$, a grid point) and a **non-monotonic grid artifact** at finite $k$ (where the true floor sits at the collinear endpoint $p=\pm k/2$, generally off-grid). Both sources named the fix as "a genuine physics change... belongs in a finding of its own, with its own review pass." This finding is that repair.

## The fix

`critical_coupling` and `threshold_wavefunction` now accept `threshold="grid"` (default, **unchanged** — F169's own artifact-diagnostic test keeps running exactly as before) or `threshold="closed"` (new): the latter substitutes `threshold_closed_form(k)`, already exact and already validated by F397's exhaustive search, in place of the grid minimum. This is additive, not destructive — no existing test or result changes.

## 1. An exact identity, sharper than F169's own leading-order statement

F169/CL149 states $\Omega_\text{even}(k)-T(k)=|k_xk_yk_z|/(3|k|)+O(k^3)$, vanishing whenever any **one** component of $k$ is zero (a 2-D coordinate **plane**) — but only stated to leading order there. Checked here (check A2): a genuine in-plane point with **two** nonzero components (e.g. $k=(0.2,0.2,0)$) has a real, nonzero residual offset ($1.4\times10^{-4}$, well above numerical noise) — the leading-order vanishing does not extend to an exact one across the whole plane.

Along a pure coordinate **axis** (only **one** component nonzero), it is different: checked here symbolically (check A1, re-derived independently of the module from `dimensionality.bloch_vector`, and cross-checked numerically against the engine's own `bcc` dispersion at several $q$) that

$$\omega^+(q,0,0)=\omega^-(q,0,0)=\frac{|q|}{\sqrt3}\qquad\text{(exact, all orders, both chiral branches identical)},$$

because the chiral (helicity-distinguishing) term in the BDPT Bloch vector vanishes identically whenever two of the three momentum components are zero — both branches collapse onto the *same* isotropic cone. Consequently

$$\Omega_\text{even}(k,0,0)=2\cdot\frac{|k|/2}{\sqrt3}=\frac{|k|}{\sqrt3}=\min\bigl(\omega^+(k,0,0),\omega^-(k,0,0)\bigr)=T(k,0,0)$$

**exactly, for every $|k|$** along a coordinate axis — not merely $O(k^3)$-small as the general off-axis formula implies. This is a genuine **double degeneracy** of the two-body floor along axis directions: the symmetric split $p=0$ and the collinear endpoint $p=\pm k/2$ sit at the *identical* energy, not merely close. This is the structural reason (§3) that the finite-$k$ re-derived $g_c(k)$ converges more slowly and noisily along axis directions than along a generic direction — there are two coincident near-singular contributions to resolve on the grid instead of one.

## 2. The commensurability artifact is sharply reduced, not eliminated

At the same $L$ values F169's own docstring quotes for the artifact ($L=12,24,32,48,96,144,192$, $|k|=0.2$ along $(111)$), the grid threshold reproduces the documented non-monotonicity, and the closed form is monotonic at these seven points (check B1):

| $L$ | 12 | 24 | 32 | 48 | 96 | 144 | 192 |
|---|---:|---:|---:|---:|---:|---:|---:|
| $g_c$ (grid) | 2.081 | 2.059 | 1.994 | 2.083 | 2.117 | 2.126 | 2.126 |
| $g_c$ (closed) | 1.434 | 1.962 | 2.023 | 2.096 | 2.118 | 2.127 | 2.132 |

**Found on review, and corrected here (attack 4, `docs/reviews/F401-review-2026-09-23.md`).** The original text claimed this generalizes to "monotonic at every step." It does not: a denser scan at the identical $(111)$, $|k|=0.2$ point (every $L$ from 12 to 200 in steps of 4, 48 points, check B2) shows the closed form still has occasional grid-commensurability dips — a real one at $L=92$ ($g_c$ drops from 2.121 at $L{=}88$ to 1.926 at $L{=}92$). The underlying phenomenon (a Riemann sum whose worst term is set by whichever grid point happens to land closest to the true, generically off-grid, floor) is not eliminated by fixing $T$; fixing $T$ removes only the artifact's other source (the *floor itself* wandering with $L$).

What is real and quantified instead: over the same 48-point dense scan, the **closed form's worst-case single-step backslide is $0.19$, against the grid form's $0.76$ — roughly a $4\times$ reduction** — and the closed form settles into a stable range ($\pm0.02$) by $L\approx100$–144, well before the grid form does (which still shows $L{=}164$ and $L{=}184$ excursions of comparable size to its worst dense-scan value). The seven-point table above is a real fact (those are F169's own $L$ values, not chosen for this finding to look clean) but is not representative of "clean convergence at every $L$"; the honest claim is a substantial, quantified reduction in the artifact's severity, not its removal.

## 3. The re-derived $g_c(k)$: real, but direction-dependent

Along $(111)$, at $L=192$, extended on review to $|k|=1.0$ (well past the originally-checked $0.4$) and confirmed to still decrease monotonically (check B3):

| $\lvert k\rvert$ | 0 | 0.05 | 0.1 | 0.2 | 0.4 | 0.6 | 0.8 | 1.0 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $g_c(k)$, $(111)$ | 2.2596 | 2.2545 | 2.2183 | 2.1324 | 1.9738 | 1.8413 | 1.7353 | 1.6549 |

The same monotonic decrease holds along $(3,1,1)$ (2.2530 → 1.6606 over $|k|=0.05$ to $0.8$). **Declared control, verified**: at $k=0$ the grid and closed-form thresholds agree exactly ($T=0$ either way, $g_c=2.2595484878546777$ to the last printed digit under both), confirming the fix changes nothing F169 already certified.

**Found on review, and corrected here (attack 12).** The original text described this as holding "along a generic direction," implying it as a property of finite-$k$ momentum generically. It is not: along $(2,1,0)$, $g_c(k)$ is **not** monotonic — it drops sharply to $1.36$ at $|k|=0.05$ (below the $|k|=0.1$ value of $2.05$), then falls again at $|k|=0.8$ to $1.14$, an emphatically non-monotonic sequence. The decreasing trend is real and now checked over a wide range along two specific directions, $(111)$ and $(3,1,1)$; it is **not** a universal law of all finite-$k$ directions, and the finding's own text is corrected to say so rather than imply it.

## What this does and does not establish

**Established.** As a function of total pair momentum along at least the $(111)$ and $(3,1,1)$ directions, the coupling required to place a Koster–Slater bound state exactly at the two-body continuum floor $T(k)$ is not constant — it decreases substantially and monotonically over $|k|\in[0,1]$ in these units, a trend the grid-artifact numbers could not have supported (their own non-monotonicity swamped it at the $L$ values previously used). Separately, substituting the exact floor for the grid minimum gives a real, quantified (though partial) improvement in numerical stability with $L$.

**Not established — named, not overclaimed.** This is *not* a derivation of "the photon's own coupling at finite $k$," and it is *not* a universal statement about all finite-$k$ directions (see the $(2,1,0)$ counterexample, §3) or about convergence at every $L$ (see §2). Per F169's own C3-note, the symmetric configuration usually identified with the spin-1 photon sits at $\Omega_\text{even}(k)$, which is *above* $T(k)$ at generic finite $k$ (by the offset in §1) — i.e. **inside** the two-body continuum, not at its lower edge. $g_c(k)$ as computed here is the coupling for a *different* point in the spectrum (the continuum floor itself), not the coupling F168/F250's gauge-protection argument is about. Whether the *physical* photon's binding strength varies with $k$ the way $g_c(k)$ does here — along whichever directions it actually does — remains the harder, still-open question — the "all-$k$ gauge-pole proof" F169 already flagged as unsolved. This finding repairs and characterizes a well-posed diagnostic quantity, at the specific directions and scales checked; it does not close that harder question, and it does not claim more generality than what was actually checked.

---

## Verification summary

Module `photon_bound_state_finite_k.py`; test `tests/findings/test_F401_photon_bound_state_finite_k.py`; results `test-results/F401_photon_bound_state_finite_k.json`.

| # | Check | Type | Result |
|---|-------|------|:------:|
| A1 | $\omega^+(q,0,0)=\omega^-(q,0,0)=\lvert q\rvert/\sqrt3$ exactly, both branches identical on-axis | exact (sympy) | PASS |
| A2 | A genuine in-plane point has a real nonzero offset (leading-order vanishing does not extend exactly) | quantitative | PASS |
| B1 | `threshold="closed"` converges monotonically along $(111)$ at F169's own 7 quoted $L$ values; `threshold="grid"` does not | quantitative | PASS |
| B2 | Dense 48-point $L$-scan: closed form's worst-case backslide ($0.19$) is $<$ half the grid form's ($0.76$); at least one closed-form dip still found (honesty check) | quantitative | PASS |
| B3 | $g_c(k)$ decreases monotonically with $\lvert k\rvert$ along $(111)$ (to $\lvert k\rvert=1.0$) and $(3,1,1)$; $(2,1,0)$ is confirmed NOT monotonic; declared control: grid/closed agree exactly at $k=0$ | quantitative | PASS |

---

## Falsifiers

1. **Exhibit a coordinate-axis $q$ where $\omega^+(q,0,0)\ne\omega^-(q,0,0)$.** §1's exact identity dies — it is a symbolic sympy result and should not be findable, but is stated for completeness.
2. ~~**Exhibit an $L$ sequence along a generic direction where `threshold="closed"` fails to converge monotonically.**~~ **Already met, on review** (attack 4): a denser scan at the same $(111)$, $|k|=0.2$ point does exactly this (a real dip at $L=92$). §2 is narrowed accordingly, not falsified outright — the quantified worst-case-severity reduction (check B2) survives.
3. **Exhibit a $k$ along $(111)$ or $(3,1,1)$ where the closed-form $g_c(k)$ exceeds its value at a smaller $|k|$ on the same ray, within the checked range $|k|\le1.0$.** §3's monotonic-decrease claim (for these two directions specifically) dies within that range.
4. **Derive the physical, gauge-consistent coupling at finite $k$ (the harder question this finding declines) and show it does NOT track $g_c(k)$ as computed here, along whichever directions $g_c(k)$ is actually monotonic.** This would not falsify anything asserted here (which explicitly declines that claim) but would close the distinct, harder question this finding leaves open.
5. **Exhibit a direction other than $(2,1,0)$ where the decreasing trend also fails**, or conversely a principled reason $(111)$/$(3,1,1)$ are the "well-behaved" class and $(2,1,0)$ is the exception. Neither is established here — the three directions checked are a sample, not a classification.

---

## Provenance

- Module: `src/casim/engine/gauge/photon_bound_state_finite_k.py` (`gauge` sector, `exactness=quantitative`, registered in `_SPINE`, D11), plus an additive `threshold=` parameter on `photon_bound_state.critical_coupling`/`.threshold_wavefunction` (default unchanged; no existing test or result is affected — verified: `casim test --id F169-photon-bound-state` reproduces its own pre-existing, unrelated result-drift status exactly, not a new failure, confirmed independently on review by diffing the drift against HEAD and tracing it to C3/`true_threshold`, not C4/`critical_coupling`).
- Test record: `F401-photon-bound-state-finite-k`, `kind: assertion`, `tier: gate`, entry `check_all`, 5/5 PASS, **one declared control, verified RED** (`perturb_k0_threshold=break`, comparing $k{=}0$ agreement against a deliberately wrong reference). The axis identity (A1) is re-derived independently of the module in the test file — re-typed from `dimensionality.bloch_vector`, not imported.
- Runner: `tests/runners/run_f401_photon_bound_state_finite_k.py` → `test-results/F401_photon_bound_state_finite_k.json`.
- Reads: F169 (the artifact this repairs, and the C3-note this finding's scope respects), F397 (the closed-form $T(k)$/$\varepsilon(k)$ this builds on), F168/F250 (why the physical photon rides $\Omega_\text{even}$, not $T(k)$, at finite $k$ — the reason this finding's scope is bounded), F291 (`dimensionality.bloch_vector`, reused for the axis-identity proof).
- **Supersedes nothing.** F169, F397, F168, F250 are left bit-unchanged; F169's own C2/C4-note is not edited (its own diagnostic still runs against the unchanged default `threshold="grid"` behavior) — this finding is a documented extension, per the finding/ledger split this project already uses.
