# F398 — Pryce's 1938 exact-Bose-commutation objection, tested against the F69/F169 paired photon: an exact closed-form deficit that vanishes as the BZ grid is refined toward the continuum threshold equation

**Date:** 2026-09-23 - 17:45
**Status:** Confirmed — 4/4 gate legs PASS (two exact/machine, two quantitative), two independent declared negative controls verified sound (each reddens exactly its own leg, no spill).
**Reviewed:** 2026-09-23 — **CONFIRMED-NARROWER** ([independent review](../docs/reviews/F398-review-2026-09-23.md)) — Result 1 (the exact identity) fully confirmed by a third, independent implementation; Result 2's $L^{-2}$ exponent independently re-derived blind; the original single-point $(L{=}10,100)$ numerical demonstration was found fragile (robust in only 12/30 nearby anchor pairs) and fixed in this same session with a resonance-robust lower-envelope estimator (now robust in 30/30), per the "Grid commensurability noise" section below.
**Module:** `src/casim/engine/gauge/photon_pryce_commutator.py`
**Test record:** `F398-pryce-composite-commutator` (gate, quantitative)
**Results:** `test-results/F398_pryce_composite_commutator.json`
**Claim:** CL310
**Cross-references:** [[F69-paired-spinor-photon]] (the pairing this tests), [[F169-photon-interacting-two-body-wavefunction]] (the threshold wavefunction this operator is built from), [[F217-field-native-fermion-entanglement]]/[[F218-algorithm-through-the-engine]] (the model's other exact second-quantized Fock-space constructions, site-based rather than momentum-based), [[F168-paired-photon-binding-gauge-protected]]; `docs/theory/notebook-reconstruction-correlation-queue.md` row NB-007 (this finding is the answer to that row); `docs/theory/notebook-v2/index.md` §5 Prompt A.

---

## The question

The notebook (pp.5–6) proposes the photon as two spin-½ objects "that only occur as a pair," a genuine, self-contained 2007 idea that is independently the same structural move as the historical "neutrino theory of light" line (de Broglie 1932, Jordan, revived by W. A. Perkins). The correlation queue's own sharpest technical content on this row is Pryce's 1938 result: **exact canonical Bose commutation is impossible for a composite built from two fermionic constituents.** Any such construction must rely on *approximate* boson behavior — the same sense in which a Cooper pair, a deuteron, or a pion is "approximately" a boson, not exactly one. The model's own photon (F69, decision 5) makes exactly this kind of claim ("only occurs as a pair"), and F169 supplies its explicit relative-momentum bound-state wavefunction. Neither finding checks Pryce's objection against the model's own construction. This finding does.

## Construction

At total photon momentum $\mathbf k$, F169 builds the marginally-bound (threshold) relative-momentum wavefunction $\psi_{\mathbf k}(p) \propto 1/(E_0(p;\mathbf k)-T(\mathbf k))$, with $E_0(p;\mathbf k)=\omega^+(\mathbf k/2+p)+\omega^-(\mathbf k/2-p)$ the free two-body dispersion (one constituent per BCC chiral branch), normalized on an $L^3$ relative-momentum grid. This finding builds the composite creation operator directly on that wavefunction,

$$a_{\mathbf k}^\dagger \;=\; \sum_p \psi_{\mathbf k}(p)\; b^\dagger_{+,\,\mathbf k/2+p}\, b^\dagger_{-,\,\mathbf k/2-p},$$

on a **genuine, exact, brute-force fermionic Fock space** — not a mean-field approximation, not a bosonization ansatz. Fock states are represented as sets of occupied global mode indices with canonical Jordan–Wigner sign bookkeeping (the same discipline F217/F218 use for the model's site-based Hubbard chain, here applied to momentum-space modes instead), so applying $a^\dagger_{\mathbf k}$ zero, one, or two times to the vacuum produces exact many-body states whose norms can be read off without approximation.

## Result 1 — an exact closed-form identity

Verified by direct construction (residual $8.9\times10^{-16}$ against the brute-force Fock computation, at two independent small grids $L=3,4$ — the project's own "two independent solve routes" standard, cf. F74/F122):

$$\boxed{\;\big\|(a_{\mathbf k}^\dagger)^2\lvert 0\rangle\big\|^2 \;=\; 2\left(1-\sum_p\psi_{\mathbf k}(p)^4\right)\;}$$

For an ideal boson, $\|(a^\dagger)^2|0\rangle\|^2=2!=2$ exactly. The deficit from that value, $\Delta_2\equiv2\sum_p\psi(p)^4$, is controlled entirely by the wavefunction's **inverse participation ratio** $\mathrm{IPR}[\psi]=1/\sum_p\psi(p)^4$ — how many relative-momentum modes the bound-state wavefunction effectively spans. This is Pryce's physics made exact and quantitative for this specific construction: the deficit is not a free parameter or an estimate, it is a closed-form function of the photon's own already-derived bound-state wavefunction. The single-photon norm $\langle0|a_{\mathbf k}a_{\mathbf k}^\dagger|0\rangle=\sum_p\psi(p)^2=1$ exactly, for any normalized real $\psi$ — no Pauli blocking is visible at one-photon occupation, as expected (the vacuum has nothing to block against); the effect only appears from two composite quanta up, exactly where Pryce's objection bites.

## Result 2 — the deficit vanishes as the grid is refined toward the continuum threshold equation

$L$ here is **not** a real-space volume/dilute-limit parameter (increasing it does not make the physical bound state more spread out); it is the momentum-space resolution of the *same* already-normalizable ($\sum\psi^2=1$, Watson-finite, F169 C1/C2) continuum wavefunction. The scaling with $L$ is nonetheless derivable and was checked in both raw and normalized form:

- **Raw $\sum_p u(p)^2$ (unnormalized, $u\equiv1/(E_0-T)$) is bulk/continuum-dominated**, growing as $\propto L^3$: the ratio $\sum u^2/L^3$ measured $0.2763$ at $L=10$ and $0.2754$ at $L=100$ — stable to $0.3\%$ (leg `bulk_norm_is_L3`). This is the ordinary Riemann-sum-to-integral statement of Watson finiteness — $E_0\sim c|p|$ is gapless but the $3$-D measure $p^2\,dp$ tames the $1/E_0^2$ singularity, so the sum is dominated by the smooth bulk of the Brillouin zone, not by the handful of points nearest $p=0$.
- **Raw $\sum_p u(p)^4$ is dominated by the innermost few nonzero grid points**, growing as $\propto L^4$: the *continuum* integral $\int d^3p/E_0(p)^4\sim\int dp/p^2$ genuinely diverges at $p\to0$ (a stronger singularity that the $3$-D measure does not tame), so only the grid's own finite spacing regularizes it — the nearest-neighbor grid point sits at $|p|\sim2\pi/L$, contributing $u^4\sim L^4$ from an $O(1)$-sized handful of points, which is checked directly (`u4/L^4` measured $0.046$–$0.10$ across $L=10\ldots140$, same order of magnitude, dominated by discreteness rather than smoothly convergent).
- **The ratio therefore falls as $\sum\psi(p)^4=\sum u^4/(\sum u^2)^2\sim L^4/L^6=L^{-2}$.** Measured with the resonance-robust lower-envelope estimator described below: $\Delta_2/2=\sum\psi^4=4.605\times10^{-3}$ at $L=10$ and $5.424\times10^{-5}$ at $L=100$, ratio $84.9$ — the same order as the $(100/10)^2=100$ prediction (leg `deficit_shrinks_with_L`, checked against a $[20,200]$ band, verified in the review below to hold across every nearby anchor choice, not just this one pair).

**Pauli blocking between two composite photons built from this specific marginally-bound wavefunction vanishes as the momentum-space resolution is refined toward the exact continuum threshold equation.** Pryce's objection is real (Result 1's exact deficit is never zero at finite $L$) but does not obstruct approximate Bose statistics for this construction in the fine-resolution limit — the deficit is a genuine, computable, vanishing correction, not an O(1) structural failure. **Independent confirmation:** the mandatory attack-and-fix review (below) included a from-scratch blind derivation that reproduced both the exact identity and, independently, the $L^{-2}$ exponent by pure dimensional power-counting — the same argument given here, arrived at without seeing this finding.

## Grid commensurability noise, and the fix the attack-and-fix review forced

**Original version of this section (superseded by the review, kept here for the record — see the review's attack 12 and recommendation 1):** a dense sweep showed real, non-monotonic spikes at specific $L$, and asserted the two original gate-check $L$ values ($10$, $100$) had been "directly verified clean of this artifact before being fixed as the record's parameters." **That claim was correct in substance (the values had in fact been checked) but was not auditable** — no artifact in the repository backed it, and the review's own systematic neighbour scan found that a *raw single-point* ratio at nearby $(L_\text{lo},L_\text{hi})$ pairs lands inside the then-current $[30,400]$ band only **12 of 30 times** (`tests/runners/pryce-commutator/run_F398_robustness_scan.py`, `raw_ratios`) — the original check was closer to a fortunate draw than a robust confirmation, exactly the review's central finding.

**Fix, applied in this session under the review's recommendation 1 (not deferred to a future session, since this is the same session that built the finding — CLAUDE.md's `/finding` step-7 discipline).** A resonance can only *add* spurious weight to $\sum\psi^4$ (a near-degenerate grid point inflates it; nothing makes it fall below the generic, non-resonant value) — so the **minimum over a small window of $L$ around the target** (`deficit_robust_min`/`bulk_robust_min`, half-window $4$, i.e. 9 grid points) is a principled lower-envelope estimator of the true trend, not an ad hoc smoothing. Re-running the same neighbour scan with this estimator: the deficit ratio lands in $[47.5,86.7]$ and the gate's $[20,200]$ band holds for **all 30 of 30** tested $(L_\text{lo},L_\text{hi})$ pairs in $[8,13]\times[95,105]$; the bulk-ratio-of-ratios lands in $[0.75,1.00]$ (diagnostic, no band). The full per-$L$ scan for the two committed gate anchors is stored directly in `test-results/F398_pryce_composite_commutator.json` (`deficit_scan_lo/hi`, `bulk_scan_lo/hi`); the neighbourhood-wide audit trail is `tests/runners/pryce-commutator/run_F398_robustness_scan.py` → `tests/runners/test-results/F398_robustness_scan.json`. Both controls (below) re-verified sound after the fix.

Full detail: `docs/reviews/F398-review-2026-09-23.md`.

## Verified negative controls (two, each isolated)

1. **`pairing="shared"`** (every relative-momentum term forced to share the same fixed `–` constituent mode instead of its own momentum-conserving partner $-p$): breaks the disjoint-mode assumption Result 1's Wick-combinatorics identity depends on. Reddens **only** `closed_form_matches_fock` (residual jumps from $8.9\times10^{-16}$ to $1.94$); the other three legs — which do not depend on which specific bijection pairs the `+`/`–` constituents — stay green, exactly as expected.
2. **`wavefunction="uniform"`** (a generic normalized pair wavefunction with no near-threshold singularity, $\psi(p)=1/\sqrt N$ for all occupied $p$): gives $\sum\psi^4=1/N\sim L^{-3}$, a genuinely *different*, faster decay than the physical $L^{-2}$ law — measured ratio $1001$ at the same $(L=10,100)$ pair, matching the $L^{-3}$ prediction $(100/10)^3=1000$ almost exactly and landing well outside the physical law's $[30,400]$ band. Reddens **only** `deficit_shrinks_with_L`; the other three legs stay green.

Both controls confirmed sound via `make can-fail` and `make control` (journalled in `test-results/can-fail.json`, `test-results/control-soundness.json`).

## What this closes, and what remains open

**Closes** correlation-queue row NB-007's Pryce half: the model's paired-spinor photon does not claim, and does not need, exact Bose commutation — it is a genuine composite of two on-shell fermionic constituents, and the deviation from ideal-boson behavior is a computable, vanishing (not structural) correction, in exactly the sense the historical de Broglie/Jordan/Perkins literature always required of this class of construction. This is a *confirmation that the construction is honest*, not a new prediction distinguishing it from a fundamental photon.

**Attribution note added by the attack-and-fix review (attack 11):** Result 1's closed-form identity is standard composite-boson ("coboson") machinery — see Combescot & Betbeder-Matibet's coboson formalism (e.g. arXiv:1002.1182) and the "bosonic-character normalization" $\chi_M=\langle0|C^MC^{\dagger M}|0\rangle/M!$ (here $\chi_2=1-\sum_p\psi(p)^4$) standard in Cooper-pair/exciton treatments — not a new mathematical result, and this finding did not originally cite it. What is genuinely this finding's own contribution is Result 2: applying that known deviation formula to this model's own already-derived (F169) threshold wavefunction, and deriving + measuring its momentum-grid-resolution scaling ($\sim L^{-2}$), a direction (grid-resolution refinement of one fixed, marginally-bound wavefunction, as opposed to the standard density/dilute-limit scaling) the review found no prior-art match for.

**What this does *not* address, honestly stated:**

- **Only the specific observable Pryce's own 1938 calculation addresses** — whether the fixed operator $a_{\mathbf k}^\dagger$ built from a *single, frozen* wavefunction shape satisfies $[a,a^\dagger]\to1$ — is computed here. It is not the same question as "do many real photons in a laser mode behave ideally," which would require building the genuine many-composite variational ground state (the wavefunction itself could reorganize as occupation grows), a substantially larger undertaking not attempted.
- **This is a $\mathbf k=0$ calculation.** F169's threshold wavefunction is exact (not a grid artifact) only at $\mathbf k=0$ (its own C2/C4-note); repeating this at finite $\mathbf k$ would inherit that module's own documented, undischarged finite-$k$ grid-threshold artifact rather than adding a new one.
- **No claim is made about the *rate* at which real multi-photon states (a laser, a coherent state) would show any residual non-bosonic signature.** That would require connecting this deficit to an actual observable — outside this finding's scope.

## Files

- Module: `src/casim/engine/gauge/photon_pryce_commutator.py` (`fock_two_photon_norm`, `deficit_closed_form`, `two_photon_norm_closed_form`, `bulk_normalization_ratio`, `deficit_at`, `check_pryce_composite_commutator`)
- Test record: `F398-pryce-composite-commutator` (`tests/registry/gauge.yaml`)
- Results: `test-results/F398_pryce_composite_commutator.json`
