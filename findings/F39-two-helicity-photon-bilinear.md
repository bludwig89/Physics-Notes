# F39 — Two-Helicity Composite Photon at the Bilinear Level (FG-6)

*2026-05-26 - 03:15 — Closes the structural gap that F29's W-triplet bridge built the composite photon from `sign='+'` Weyl eigenmodes only. The new construction in `ca_maxwell.py` builds the photon bilinear from BOTH BCC chirality branches, and the resulting (E, B) field manifests the two-helicity structure that F37 established at the field level: under chiral propagation, $F^+(k) = E + iB$ tracks $\Omega^+(k)$ and $F^-(k) = E - iB$ tracks $\Omega^-(k)$. The (1,1,1) birefringence reproduces F30's closed form $-\sqrt3/27\!\cdot\!k^2$ to $4.5\times10^{-5}$ relative.*

Cross-references: [F26 photon rotation law](F26-speed-of-light-as-rotation-rate.md); [F27 chiral SU(2) mass mechanism](F27-complex-mass-chiral-su2.md); [F29 W-triplet SU(2) bridge](F29-w-triplet-bilinear-su2-bridge.md) (the bridge this finding extends); [F30 dispersion anisotropy and birefringence](F30-photon-dispersion-order-anisotropy-birefringence.md); [F37 RS / BCC chirality correspondence](F37-rs-bcc-chirality-helicity.md); [first-gen-completeness-review.md](../first-gen-completeness-review.md) §3 item 4 and §5.1; [exactness-inventory.md](../exactness-inventory.md) entries #92–95; test script [`model-tests/test_FG6_two_helicity_photon.py`](../model-tests/test_FG6_two_helicity_photon.py); results [`test-results/FG6_two_helicity_photon.json`](../test-results/FG6_two_helicity_photon.json).

---

## 1. Why this matters

F29 demonstrated that the composite photon bilinear and the chiral SU(2) doublet structure fit together — but only along one BCC branch (`sign='+'`). F37 then proved at the (E, B) field level that the two BCC branches $\Omega^\pm$ correspond to the two photon helicities $F^\pm = E\pm i\mathbf B$, and added a chiral propagation step that rotates them independently. What was missing was the bridge from spinor to field on BOTH branches: a bilinear construction that builds (E, B) from both chirality branches simultaneously, so the resulting photon carries a complete two-helicity state from its underlying Weyl content.

This finding closes that bridge. It introduces a small set of helpers in `ca_maxwell.py`, runs a 10-test suite confirming the construction matches the previously-derived field-level behaviour, and reproduces the F30 birefringence directly from the dispersion.

A subtle but useful by-product: the test demonstrates that the chiral propagator decouples helicities by *eigenstate*, not by spinor provenance — a single-branch bilinear at +k, when planted into the real-space lattice and propagated, has its $F^+$ component evolving at $\Omega^+$ and its $F^-$ component at $\Omega^-$. The provenance (which branch's Weyl spinor built the bilinear) does not change the propagation. This justifies the language used in the completeness review: the *photon* is genuinely a two-helicity object even when the underlying bilinear is single-branch.

---

## 2. Construction

The new module-level functions added to `ca_maxwell.py`:

| Helper | Signature | Returns |
|---|---|---|
| `EM_bilinears_branch` | `(psi, phi, kx, ky, kz, sign)` | `(E, B, n_half)` for the branch `sign`. |
| `EM_bilinears_two_helicity` | `(psi_pl, phi_pl, psi_mn, phi_mn, kx, ky, kz, α_pl=1, α_mn=1)` | Combined `(E, B, {'+': {...}, '-': {...}})`. |
| `riemann_silberstein_decomp` | `(E, B)` | `(F_plus, F_minus) = (E+iB, E-iB)`. |
| `triplet_bilinear_branch` | `(psi_iso, phi_iso, kx, ky, kz, sign)` | `(E_W, B_W, W, n_half)` triplet per branch. |
| `triplet_bilinear_two_helicity` | `(psi_iso_pl, phi_iso_pl, psi_iso_mn, phi_iso_mn, kx, ky, kz, α_pl, α_mn)` | Combined $(E^a, B^a)$ + per-branch dict. |

The branch-aware singlet bilinear evaluates

$$
G^i(k, \mathrm{sign}) = \phi^T\,\sigma^i\,\psi\,\big|_{k/2,\ \mathrm{sign}},\quad
E_\sigma(k) = \lvert n_\sigma(k/2)\rvert\,(G_T + G_T^*),\quad
B_\sigma(k) = i\,\lvert n_\sigma(k/2)\rvert\,(G_T^* - G_T),
$$

where $n_\sigma(k/2)$ is the BCC structure vector on branch $\sigma\in\{+,-\}$ and $G_T$ is the transverse projection of $G$ against $\hat n_\sigma$. The two-helicity assembler is the linear superposition

$$
E(k) = \alpha_+\,E_+(k) + \alpha_-\,E_-(k),\qquad
B(k) = \alpha_+\,B_+(k) + \alpha_-\,B_-(k),
$$

with arbitrary complex weights $\alpha_\pm$. The Riemann-Silberstein decomposition $F^\pm = E\pm iB$ projects the result onto helicity eigenstates of the field-space rotation.

The W-triplet helpers parallel the singlet, with the bilinear

$$
W_H^{a,i}(k,\sigma) = \sum_{\alpha\beta} (\tau^a)_{\alpha\beta}\,(\phi^\alpha)^\dagger\sigma^i\psi^\beta\,\big|_{k/2,\ \sigma}
$$

(the Hermitian SU(2)-clean variant from F29) and the same Paper 1 Eq. 35 promotion to $(E^a, B^a)$ per isospin component.

---

## 3. Test suite (`test_FG6_two_helicity_photon.py`, 10/10 PASS)

All ten ran in 0.30 s total. Residuals:

| # | Test | Residual | Tier |
|---|---|---|---|
| FG6.1 | Per-branch (E, B) is nonzero and transverse to its own $2 n_\sigma$ | $3.4\times10^{-17}$ | Exact-by-construction (post-projection) |
| FG6.2 | Two-helicity assembler is linear in the branch weights $\alpha_\pm$ | $0.0$ | Algebraic exact |
| FG6.3 | Both helicities $F^\pm$ present in the combined photon (min ratio = 1.0 = linearly polarized) | $1.0$ | Structural (single-branch bilinear is linearly polarized) |
| FG6.4 | Per-branch singlet SU(2) invariance (F29-B1 extended to sign='-') | $3.4\times10^{-16}$ | Machine precision |
| **FG6.5** | **Chiral propagation: $F^+(k)\to e^{-i\Omega^+(k)}F^+(k)$ and $F^-(k)\to e^{+i\Omega^-(k)}F^-(k)$ per tick, across single-branch + combined initial states (12 cases)** | $1.5\times10^{-15}$ over 10 ticks | Machine precision |
| **FG6.6** | **Birefringence $\Delta\Omega(k\hat n_{111}) = -(\sqrt3/27)k^2 + O(k^4)$ (F30 closed form)** | $4.5\times10^{-5}$ relative on 65-point LSQ fit | Quantitative |
| FG6.7 | Per-branch triplet adjoint $W^a \to R^{ab}(V)W^b$ (F29-B2 extended) | $2.6\times10^{-16}$ | Machine precision |
| FG6.8 | Combined-state triplet magnitude $\sum_a\|W^a\|^2$ SU(2)-invariant | $4.4\times10^{-16}$ | Machine precision |
| FG6.9 | Per-branch raw triplet transversality $2 n_\sigma\!\cdot\!W^{a,\sigma}_T \to 0$ (F29-B4 extended) | $2.9\times10^{-2}$ at $k=0.05$ = $c_\text{lat}\!\cdot\!k$ | F29-B4 scaling |
| FG6.10 | Riemann-Silberstein identity $E = (F^+ + F^-)/2$, $B = (F^+ - F^-)/(2i)$ | $0.0$ | Algebraic exact |

The two headline results are FG6.5 and FG6.6.

**FG6.5 (chiral dispersion per helicity).** For each test mode at lattice index $(k_i, k_j, k_k)$ in an $L=16$ lattice — including the body-diagonal mode $(1,1,1)$ — the test builds three initial states: (a) $(E, B)$ from a single `sign='+'` bilinear, (b) from a single `sign='-'` bilinear, and (c) from the combined two-helicity assembler. It plants each as a single Fourier mode with the Hermitian-symmetric partner at $-k$, runs 10 ticks of `w_propagation_step_spectral`, and verifies that the F^+ Fourier amplitude has acquired phase $e^{-i\Omega^+(k)\cdot 10}$ and F^- has acquired phase $e^{+i\Omega^-(k)\cdot 10}$. All 12 cases (4 modes × 3 states) match to $1.5\times10^{-15}$ relative — well below the $10^{-10}$ target inherited from F37.1/F37.2.

**FG6.6 (F30 birefringence).** Direct dispersion evaluation along $k\parallel(1,1,1)$ gives $\Delta\Omega(k) = 2\bigl[\omega_+(k/2)-\omega_-(k/2)\bigr]$. A 200-point sweep over $k\in[0.005, 0.30]$ followed by a $c\cdot k^2$ fit on $k<0.10$ returns $c_\text{meas} = -0.064153$ vs the closed form $c_\text{exact} = -\sqrt3/27 = -0.0641500299\ldots$, a $4.5\times10^{-5}$ relative error — at the same precision F37.3 hit. This is the *intrinsic* birefringence at the lattice level; the question of confronting it with polarisation data is observational and remains open (see §5).

---

## 4. What this adds to F37 (and why FG-6 is not redundant)

F37 established at the field level — i.e., starting from a real-space $(E, B)$ field manually constructed in a pure-F^± state — that the chiral propagator decouples the helicities at $\Omega^\pm$. F37 did not close the bridge from the underlying Weyl-spinor bilinear: the F29 bridge that built $(E, B)$ from the underlying spinors only used one BCC branch.

What FG-6 adds:

1. **A bilinear construction that uses both branches.** `EM_bilinears_two_helicity` produces (E, B) from `sign='+'` AND `sign='-'` spinors with arbitrary complex weights. The single-branch `EM_bilinears_branch` remains available as the per-helicity ingredient.

2. **Evidence that the chiral propagator separates helicities by eigenstate, not by spinor provenance.** FG6.5's "single-branch initial state" cases plant a (E, B) built entirely from one branch (e.g. `sign='+'`) and observe that the F^- component of the resulting field still rotates at $\Omega^-$, not at $\Omega^+$. This is structurally important: it justifies treating the photon as a two-helicity object even when the bilinear provenance is mixed or single-branch.

3. **A bilinear-anchored confirmation of F30 birefringence.** F37.3 measured ΔΩ at the propagator level. FG6.6 reproduces it via direct dispersion of the two branches at $k/2$, which is the dispersion seen by the bilinear's spinor inputs. The same coefficient $-\sqrt3/27$ falls out at the same precision, confirming the bilinear inherits the right anisotropy.

4. **F29 B1–B4 extended to the second branch.** Per-branch SU(2) singlet invariance, triplet adjoint rotation, and the $c_\text{lat}\!\cdot\!|k|$ raw triplet transversality scaling all hold identically on `sign='-'`. The combined-state triplet $\sum_a\|W^a\|^2$ SU(2)-invariance is also exact.

---

## 5. What FG-6 does NOT close

1. **The composite photon vs. the U(1)-gauge photon are still two distinct objects in the code.** The completeness review §2.2 row for the photon notes that `ca_maxwell.py`'s composite bilinear and the photon used for minimal coupling inside `ca_dirac` are not unified. FG-6 closes the helicity structure of the composite photon but does not address that unification.

2. **Experimental confrontation with polarisation data.** The intrinsic birefringence $\Delta\Omega = -(\sqrt3/27) k^2$ is reproduced algebraically; mapping it to a measurable astrophysical signal (vacuum-birefringence bounds at GeV/TeV energies, GRB polarization rotation, etc.) is a Tier-B observational task and remains open. The completeness review §3 item 4 noted this; FG-6 closes the model-side half.

3. **Two-helicity W-triplet propagation under SU(2) gauging.** The W^a fields built here propagate under the same F26 rotation law per component (F29-B5), but a dynamical, fully-gauged $W$ propagator that distinguishes the two helicities is the existing roadmap item — `w_propagation_step_chiral` already does this for the W field; cross-coupling to the bilinear $W^a$ here is straightforward but not separately tested.

---

## 6. Files

- Module code: [`ca-simulation/ca_maxwell.py`](../ca-simulation/ca_maxwell.py) (new functions `EM_bilinears_branch`, `EM_bilinears_two_helicity`, `riemann_silberstein_decomp`, `triplet_bilinear_branch`, `triplet_bilinear_two_helicity`, plus factored-out `_TAU_ISO`, `_singlet_bilinear_H`, `_triplet_bilinear_H`).
- Test script: [`model-tests/test_FG6_two_helicity_photon.py`](../model-tests/test_FG6_two_helicity_photon.py)
- Results JSON: [`test-results/FG6_two_helicity_photon.json`](../test-results/FG6_two_helicity_photon.json)
- Inventory entries: #92 (linearity), #93 (per-helicity dispersion), #94 (F30 coefficient), #95 (RS identity).
- Review updates: §0 dated note, §2.2 photon row, §3 item 4 → ✅ closed, §5.1 FG-6 row, §7 sequencing item 4.

---

*End of finding.*
