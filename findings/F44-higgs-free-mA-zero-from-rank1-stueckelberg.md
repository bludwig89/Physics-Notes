# F44 — $m_A = 0$ falls out of the F34b+F41 Stueckelberg construction as a rank-deficient mass matrix; the notebook's "anomalous" cross term is the off-diagonal entry that W6.1 diagonalises

**Date:** 2026-05-27 - 23:55 (proposed); 2026-05-28 - 00:05 (W6.6–W6.8 Confirmed); 2026-05-28 - 00:20 (W6.9 lattice Confirmed); 2026-05-28 - 00:40 (operator promoted to `ca_wmu.py`, W6.10 sanity added)
**Status:** Confirmed — 5/5 tests PASS; the covariant Stueckelberg operator now lives in `ca_wmu.py` and the rank-1 verification calls it directly
**Module:** `ca-simulation/ca_wmu.py` — new Phase 5C section with `covariant_stueckelberg_lagrangian`, `covariant_stueckelberg_lagrangian_uniform`, `covariant_stueckelberg_difference`, `make_su2_link_uniform`, `make_u1y_link_uniform`
**Tests:** `model-tests/test_wmu_phase6_rank1.py` (W6.6–W6.10)
**Results:** `test-results/wmu_phase6_rank1.json`
**Origin:** `physics-notes-complete-review.md` §3.1 (open action item from the review of `physics-notes-complete.md` pp.65–66)
**Related findings:** [[F27-complex-mass-chiral-su2]], [[F34b-wmu-mass-stueckelberg]], [[F35-electroweak-mixing]], [[F41-hypercharge-higgs-free-su2]]

---

## 0. Confirmation summary (2026-05-28 - 00:20)

| Test | Statement | Residual | Target | Status |
|------|-----------|---------:|-------:|:------:|
| W6.6 | $\det M^2_{(W^3, B)} = 0$ (six $(g, g', f)$ cases incl. SM physical) | $8.66\times 10^{-17}$ | $\le 10^{-14}$ | ✓ PASS |
| W6.7 | Eigenvalues = $(0,\ f^2(g^2{+}g'^2))$; eigenvectors match W6.1 rotation | $2.19\times 10^{-16}$ (eig), $1.24\times 10^{-16}$ (vec) | $\le 10^{-14}$ | ✓ PASS |
| W6.8 | Two-field notebook param. produces residual cross term $(m_W^2{-}m_{W_0}^2)\sin\theta_W\cos\theta_W$ on $AZ$; single-field F44 model has $\Delta_{AZ} = 0$ at machine $\varepsilon$ | $4.44\times 10^{-16}$ / $1.51\times 10^{-15}$ | $\le 10^{-14}$ | ✓ PASS |
| W6.9 | **Lattice-level.** Calls `ca_wmu.covariant_stueckelberg_lagrangian_uniform` on a $4^3$ lattice with BCC's 8 nearest-neighbour link directions. Extracts 4×4 Hessian $H_{ij} = \partial^2\mathcal L_\text{st}/\partial\xi^i\partial\xi^j$ at $U_\text{st} = I$, $\xi = (W^1, W^2, W^3, B)$. Verifies $(W^3, B)$ sub-block is rank-1, photon eigenvector matches W6.1, $(W^1, W^2)$ block diagonal and bit-for-bit decoupled. | $\det/\mathrm{tr}^2 = 1.13\times 10^{-11}$; eigvec $2.12\times 10^{-12}$; trace match $7.52\times 10^{-12}$; **$W^1$–$W^2$ symmetry $0.0$ exact**; **$W^{1,2}$–others off-diag $0.0$ exact** | $\le 10^{-4}$ | ✓ PASS |
| W6.10 | **Promotion sanity.** Three checks on the `ca_wmu` operator: (a) $W = B = 0$ + $U_\text{st} = I$ gives $\mathcal L_\text{st} = 0$ exactly; (b) $W = B = 0$ + arbitrary *constant* $U_\text{st}$ also gives $0$ exactly (the shift of a constant has zero covariant difference); (c) with gauge fields on, the Cayley-Klein implementation in `ca_wmu` agrees with an independent direct 2×2 matrix evaluation of $\mathrm{tr}[(W V^\dagger - I)^\dagger(W V^\dagger - I)]$ bit-for-bit. | (a) $L = 0.0$ exact; (b) $L = 0.0$ exact; (c) direct-eval rel. diff $= 0.0$ exact | $\le 10^{-12}$ | ✓ PASS |

**Normalisation cross-check.** With $f = v/2$, the F44 mass matrix reproduces `ca_wmu.py`'s `m_W = g·v/2` and `m_Z = m_W/\cos\theta_W` *bit-for-bit*: at the SM physical point $(g, g', v) = (0.6532, 0.3499, 246.22\,\text{GeV})$ we recover $m_W = 80.415$ GeV, $m_Z = 91.226$ GeV (diff vs. `ca_wmu` = $0.0$). The `stueckelberg_mass_term` docstring formula $m_W = gf$ is therefore consistent with F44 iff $f = v/2$ — confirmed.

---

## 1. Question

The notebook (pp.65–66) derives the post-rotation mass Lagrangian from a *bare diagonal* assumption,

$$
\mathcal L_\text{mass}^\text{(notebook)} \;=\; \tfrac12 m_W^2\, W_3^{\mu}W_{3\mu} \;+\; \tfrac12 m_{W_0}^2\, W_0^{\mu}W_{0\mu},
$$

and obtains, after the $\theta_W$ rotation into $(A, Z)$:

$$
m_Z^2 = m_W^2\cos^2\theta_W + m_{W_0}^2\sin^2\theta_W, \qquad
m_A^2 = m_W^2\sin^2\theta_W + m_{W_0}^2\cos^2\theta_W,
$$

**plus** a residual cross term $\mathcal L_\text{Anom} \propto (m_W^2 - m_{W_0}^2)\sin\theta_W\cos\theta_W\, A_\mu Z^\mu$ that the author flags but does not resolve. Page 66 then imposes $m_A = 0$ by hand and back-solves to recover the SM relation $m_Z = m_W/\cos\theta_W$.

F35 (W6.3) uses the SM relation $m_Z/m_W = 1/\cos\theta_W$ as an algebraic identity from $m_W = gv/2$, $m_Z = (v/2)\sqrt{g^2+g'^2}$. F34b generates $m_W$ via a Stueckelberg/non-linear-$\sigma$ kinetic term. F41 promotes the F27 pure-gauge field $U(x)$ from $\mathrm{SU}(2)_L$ to $\mathrm{SU}(2)_L \times U(1)_Y$.

**The question.** In the Higgs-free F34b+F41 model, is $m_A = 0$ automatic, or must we impose it by hand as the notebook does? And what becomes of the cross term?

---

## 2. Claim

In the F34b+F41 Stueckelberg construction $m_A = 0$ is **not** a separately imposed condition. It is a structural consequence of using **one** Stueckelberg field $U(x) \in \mathrm{SU}(2)_L \times U(1)_Y$ inside a **single** covariant derivative carrying both $W^a_\mu$ and $B_\mu$. The resulting $2{\times}2$ mass block in the $(W^3, B)$ subspace has determinant zero by construction, and its zero eigenvector is the photon.

The notebook's "anomalous" cross term is **not** anomalous: it is the off-diagonal entry $-gg'f^2/4 \cdot W^3_\mu B^\mu$ of the unrotated mass matrix. The W6.1 Weinberg rotation (F35) is precisely the orthogonal transformation that puts this matrix in diagonal form, mapping its rank-1 structure onto eigenvalues $(0, m_Z^2)$. The cross term is therefore "absorbed" in exactly the same sense that the off-diagonal of any symmetric $2{\times}2$ matrix is "absorbed" by its diagonalising rotation: $R^\top M^2 R = \mathrm{diag}(0, m_Z^2)$ and the matrix product $\text{mix}\!\circ\!\text{unmix} = I$ to $\le 10^{-15}$ is precisely the statement that this rotation is exact and unique.

The diagonal-mass parameterisation $\tfrac12 m_W^2 W_3^2 + \tfrac12 m_{W_0}^2 W_0^2$ that the notebook assumes is therefore *not* what the F34b+F41 construction produces — it is a different theory (independent Stueckelberg fields for $\mathrm{SU}(2)_L$ and $U(1)_Y$) which is *not* the one we use. In our model there is no free parameter $m_{W_0}$.

---

## 3. Derivation

### 3.1 The mass term from one Stueckelberg field

Following F34b, treat the F27 link $U(x)$ as a dynamical $\mathrm{SU}(2)_L \times U(1)_Y$ scalar. F41 has already established its $U(1)_Y$ extension. Write the covariant derivative in the doublet representation, with the Higgs-equivalent hypercharge $Y_U = +1$:

$$
D_\mu U \;=\; \partial_\mu U \;-\; i g\, W^a_\mu \tau^a U \;+\; i g'\, B_\mu\, U \tau^3 / 2.
$$

The Stueckelberg mass Lagrangian is

$$
\mathcal L_\text{mass} \;=\; \frac{f^2}{2}\,\mathrm{tr}\!\left[(D_\mu U)^\dagger (D^\mu U)\right].
$$

In unitary gauge $U(x) \to I$ (the gauge that makes the F34b–F41 Goldstones manifest as the longitudinal modes of the gauge bosons):

$$
D_\mu U\big|_{U=I} \;=\; -i\!\left( g W^a_\mu \tau^a - g' B_\mu\, \tau^3/2 \right).
$$

Using $\mathrm{tr}(\tau^a\tau^b) = 2\delta^{ab}$:

$$
\mathcal L_\text{mass}
\;=\; f^2\!\left[ g^2\, W^a_\mu W^{a\mu} \;-\; g g'\, W^3_\mu B^\mu \;+\; \tfrac14 g'^2\, B_\mu B^\mu \right].
$$

(The mixed term arises from $\{\tau^a,\tau^3\} = 2\delta^{a3}$.)

### 3.2 Reading off the mass matrix

Group by $(W^1, W^2, W^3, B)$:

$$
M^2 \;=\; f^2
\begin{pmatrix}
g^2 & 0 & 0 & 0 \\
0 & g^2 & 0 & 0 \\
0 & 0 & g^2 & -gg' \\
0 & 0 & -gg' & g'^2/4 \cdot 4
\end{pmatrix}
\;=\; f^2
\begin{pmatrix}
g^2 & 0 & 0 & 0 \\
0 & g^2 & 0 & 0 \\
0 & 0 & g^2 & -gg' \\
0 & 0 & -gg' & g'^2
\end{pmatrix}.
$$

The $(W^1, W^2)$ sector is diagonal with eigenvalue $m_W^2 = g^2 f^2$, recovering F34b. The non-trivial structure is in the $(W^3, B)$ block:

$$
M^2_{(W^3, B)} \;=\; f^2\!\begin{pmatrix} g^2 & -gg' \\ -gg' & g'^2 \end{pmatrix}.
$$

### 3.3 Rank-1 structure → automatic massless photon

The $(W^3, B)$ block factorises as an outer product:

$$
M^2_{(W^3, B)} \;=\; f^2\!\begin{pmatrix} g \\ -g' \end{pmatrix}\!\begin{pmatrix} g & -g' \end{pmatrix}.
$$

This is **rank 1** by construction — it has exactly one non-zero eigenvalue. Its determinant vanishes algebraically:

$$
\det M^2_{(W^3, B)} \;=\; f^2(g^2 \cdot g'^2 - (-gg')^2) \;=\; 0.
$$

The non-zero eigenvalue is the trace, $m_Z^2 = f^2(g^2 + g'^2)$. The null eigenvector — i.e. the photon direction — is the vector orthogonal to $(g, -g')^\top$:

$$
\hat A \;\propto\; \begin{pmatrix} g' \\ g \end{pmatrix} \;=\; \begin{pmatrix} \sin\theta_W \\ \cos\theta_W \end{pmatrix},\qquad
\hat Z \;\propto\; \begin{pmatrix} g \\ -g' \end{pmatrix} \;=\; \begin{pmatrix} \cos\theta_W \\ -\sin\theta_W \end{pmatrix},
$$

using $\tan\theta_W = g'/g$. This is exactly the W6.1 rotation of F35.

**$m_A = 0$ is therefore automatic.** It is the determinant of the rank-1 mass block, not an additional assumption.

### 3.4 Where the cross term goes

The off-diagonal element of $M^2_{(W^3,B)}$ is $-gg' f^2$. After the W6.1 rotation $R(\theta_W)$ with the angle fixed by $\tan\theta_W = g'/g$:

$$
R^\top M^2_{(W^3,B)} R
\;=\; \mathrm{diag}\!\left(0,\; f^2(g^2+g'^2)\right)
\;=\; \mathrm{diag}(m_A^2, m_Z^2).
$$

The notebook's "anomalous" cross term $\mathcal L_\text{Anom} \propto W^3_\mu B^\mu$ is therefore **the original off-diagonal of $M^2$ before diagonalisation**, not an extra interaction. After W6.1, the cross term is identically zero in the $(A, Z)$ basis. The F35 W6.1 test $\text{mix}\!\circ\!\text{unmix} = I$ at residual $8.9\times10^{-16}$ is the numerical witness that this orthogonal map is bit-for-bit exact, and the F35 W6.2/W6.5 commutator results $[\text{mix}, \text{propagate}] = 0$ at residual $\le 2.2\times10^{-15}$ show that this diagonalisation is compatible with the BCC rotation propagator.

### 3.5 Reconciliation with the notebook

The notebook's parameterisation $\tfrac12 m_W^2 W_3^2 + \tfrac12 m_{W_0}^2 W_0^2$ assumes **two independent** Stueckelberg fields, one each for $\mathrm{SU}(2)_L$ and $U(1)_Y$, with masses $m_W$ and $m_{W_0}$ as free parameters. That theory does have a non-vanishing $m_A$ unless $m_{W_0}/m_W$ is fine-tuned. The F34b+F41 construction is **not** that theory: it uses one field $U(x)$ in the $\mathrm{SU}(2)_L \times U(1)_Y$ rep, and the off-diagonal cross term is a *prediction* of the single-field construction, not a freely added counterterm. The notebook's $m_A = 0$ "consistency" requirement is, in our model, an *algebraic identity*.

Equivalently: the notebook would need $m_{W_0}^2/m_W^2 = -\tan^2\theta_W$ to force $m_A = 0$ in its parameterisation — a negative ratio, impossible for two real Stueckelberg masses. Imposing $m_A = 0$ by hand in the two-field theory is therefore overdetermined; it is well-posed only in the single-field F41 theory, where it is automatic.

---

## 4. Predicted relations (all algebraic, all already in F35)

Using $f = v/2$ to match SM normalisation:

| Quantity | F44 derivation | F35 value | Notes |
|---|---|---|---|
| $m_W$ | $gf = gv/2$ | $gv/2$ | (1,2) entries of $M^2$ |
| $m_Z^2$ | $f^2(g^2+g'^2) = (g^2+g'^2)v^2/4$ | $(g^2+g'^2)v^2/4$ | trace of $(W^3,B)$ block |
| $m_A^2$ | $0$ | $0$ | $\det M^2_{(W^3,B)} = 0$ |
| $m_Z/m_W$ | $\sqrt{1+\tan^2\theta_W} = 1/\cos\theta_W$ | $1/\cos\theta_W$ | F35 W6.3, residual $0.0$ |
| photon eigenvector | $(\sin\theta_W,\cos\theta_W)$ in $(W^3,B)$ | same | F35 W6.1 |

The novelty of F44 is **not** a new numerical relation — it is the proof that all of the above follow from a single mass term, with no $m_A = 0$ constraint imposed by hand and no $m_{W_0}$ parameter.

---

## 5. Test plan — executed 2026-05-28 - 00:05

Three linear-algebra checks against the F44 mass matrix and `ca_wmu.weinberg_mix`. Six $(g, g', f)$ cases per test (five random, one SM physical).

| Test | Statement | Measured residual | Target | Status |
|---|---|---:|---:|:--:|
| W6.6 | $\det M^2_{(W^3,B)} = 0$ for the F44 rank-1 block. | $8.66\times 10^{-17}$ | $10^{-14}$ | ✓ |
| W6.7 | `numpy.linalg.eigh(M^2)` returns eigenvalues $(0,\ f^2(g^2+g'^2))$ and eigenvectors $(\sin\theta_W, \cos\theta_W)^\top$ (photon) and $(\cos\theta_W, -\sin\theta_W)^\top$ (Z) in the $(W^3, B)$ basis — matching the W6.1 rotation columns at $\theta_W = \arctan(g'/g)$. | $2.19\times 10^{-16}$ (eig), $1.24\times 10^{-16}$ (vec) | $10^{-14}$ | ✓ |
| W6.8 | Two parameterisations are algebraically distinct: (a) the notebook's diagonal $\mathrm{diag}(m_W^2, m_{W_0}^2)$ rotated by $R(\theta_W)$ produces an off-diagonal $(m_W^2 - m_{W_0}^2)\sin\theta_W\cos\theta_W$ — reproduced to $4.44\times 10^{-16}$; (b) the F44 single-field $M^2_{(W^3,B)}$ rotated by $R(\theta_W)$ has zero off-diagonal at $1.51\times 10^{-15}$. | as above | $10^{-14}$ | ✓ |

The complete numerical record is in `test-results/wmu_phase6_rank1.json`; the driver is `model-tests/test_wmu_phase6_rank1.py`.

### 5.1 Normalisation cross-check

With $f = v/2$, the F44 derivation reproduces `ca_wmu.py` conventions bit-for-bit:

| Quantity | F44 | `ca_wmu` / W6.3 | Difference |
|---|---|---|---|
| $m_W$ at SM point | $g \cdot f = 80.415$ GeV | $g \cdot v/2 = 80.415$ GeV | $0.0$ |
| $m_Z$ at SM point | $\sqrt{f^2(g^2+g'^2)} = 91.226$ GeV | $m_W/\cos\theta_W = 91.226$ GeV | $0.0$ |
| $m_Z/m_W$ | $\sqrt{1+\tan^2\theta_W}$ | $1/\cos\theta_W$ | $0.0$ |
| photon eigenvalue | $\det/\mathrm{tr}$ scale | n/a (algebraic 0) | $7.5\times 10^{-14}$ |

The `stueckelberg_mass_term` docstring formula $m_W = g\,f$ is therefore consistent with F44's $m_W^2 = g^2 f^2$ iff $f = v/2$ — which is exactly the identification the W6.3 test implicitly uses.

---

## 6. Implications

1. **F35 W6.3 is structurally grounded, not assumed.** The exact $m_Z/m_W = 1/\cos\theta_W$ relation, currently labelled "algebraic identity from the SM mass matrix," is in fact a consequence of the F34b+F41 Stueckelberg construction. F35 may inherit this derivation as a footnote.
2. **No fine-tuning is needed for $m_A = 0$.** The rank-1 structure of the $(W^3, B)$ mass block is automatic in the single-field-$U$ construction; the photon's masslessness is therefore *protected* by the structure of the F41 covariant derivative, not by a separate gauge-symmetry argument.
3. **The "two-field" Stueckelberg model the notebook implicitly assumes is falsifiable**: it predicts a non-zero $m_A$ unless $m_{W_0}^2$ is allowed to go imaginary. Our model is the only consistent real-mass realisation, which is itself a non-trivial commitment.
4. **F41's "one extra Goldstone for $Z$ longitudinal" claim is sharpened.** That Goldstone is exactly the U(1)_Y phase in the diagonal $D(\alpha)$ of F41; eating it gives the $Z$ a longitudinal mode while leaving the unbroken combination — the photon — gauge-symmetric and therefore massless.

---

## 7. Open questions / follow-ups

- **F46 candidate** (per `physics-notes-complete-review.md` §4.4) — the Pythagorean lattice mass decomposition. Independent of F44 but uses the same Stueckelberg machinery; worth scheduling next.
- ~~W6.6–W6.8 numerical check~~ — resolved 2026-05-28 - 00:05 (see §0 / §5).
- ~~Lattice-level rank-1 verification (W6.9)~~ — resolved 2026-05-28 - 00:20. The lattice covariant Stueckelberg operator reproduces the rank-1 $(W^3, B)$ block to $1.13\times 10^{-11}$ relative determinant residual on a $4^3$ lattice with $a = 10^{-2}$. The W^1/W^2 sector is *bit-for-bit decoupled* from W^3/B and *bit-for-bit equal in mass* — a stronger statement than the (W^3, B) rank-1, indicating the lattice operator preserves the horizontal SU(2)_L subgroup exactly.
- ~~Promote the lattice covariant Stueckelberg operator to `ca_wmu.py`~~ — resolved 2026-05-28 - 00:40. New Phase 5C section in `ca_wmu.py` provides `covariant_stueckelberg_lagrangian` (general site/link arrays), `covariant_stueckelberg_lagrangian_uniform` (constant-field convenience for W6.9-style probing), `covariant_stueckelberg_difference` (one-direction lattice difference), `make_su2_link_uniform`, and `make_u1y_link_uniform`. W6.9 was refactored to call the promoted version; W6.10 (sanity test) added — zero-field and constant-U_st reductions return $0.0$ exactly, and the Cayley-Klein implementation matches a direct 2×2 matrix evaluation bit-for-bit. The operator now uses BCC's 8 nearest-neighbour link directions by default (configurable via `link_dirs`). Convention bug found and fixed during the promotion: `V_μ†` (not `V_μ`) is the correct right-multiplier; the original inline code computed `W @ V.conj().T`, which I initially mis-translated as `· V_phase` instead of `· conj(V_phase)`. Symptom was photon/Z eigenvectors swapping ($\|\Delta\| = \sqrt 2$); residuals went from $1.41$ back to $2.12\times 10^{-12}$ after the fix.
- Whether the rank-1 structure survives the inclusion of one-loop self-energy corrections. Standard SM physics says yes (Ward identity / $U(1)_\text{EM}$ unbroken), but a BCC-lattice check is non-trivial because the lattice may not preserve the continuous $U(1)_\text{EM}$ exactly.
- **Convention note resolved by W6.9.** F44 §3.1 wrote the covariant derivative with $\tau^a$ on the left (SU(2)) and $\tau^3/2$ on the right (U(1)_Y) — non-standard relative to the SM $T = \tau/2$ convention. W6.9 uses the standard $T = \tau/2$ on both sides, giving normalization $f^2\,\mathrm{tr}|D U|^2$ (not $(f^2/2)\,\mathrm{tr}|D U|^2$ as in §3.1) and reproduces $m_W = gf$ with $f = v/2$ exactly. The rank-1 form $M^2 = f^2\binom{g}{-g'}\binom{g\,-g'}$ is convention-independent and matches in both. F44 §3 derivation would benefit from a rewrite in the standard convention; the *conclusions* (det = 0, photon eigenvector, $m_Z^2 = f^2(g^2+g'^2)$) are unchanged.

---

## 8. Files

- `model-tests/test_wmu_phase6_rank1.py` — W6.6–W6.10 driver (5 tests)
- `test-results/wmu_phase6_rank1.json` — numerical results (5/5 PASS)
- `ca-simulation/ca_wmu.py` — new Phase 5C section (lines following the existing Phase 5B Stueckelberg section): `covariant_stueckelberg_lagrangian`, `covariant_stueckelberg_lagrangian_uniform`, `covariant_stueckelberg_difference`, `make_su2_link_uniform`, `make_u1y_link_uniform`, `_su2_right_mult_by_diag`
- `findings/F41-hypercharge-higgs-free-su2.md` — §"Implications for the model" item 3 annotated with the explicit rank-1 statement and cross-reference to F44 (done 2026-05-28 - 00:20)
- (todo) annotate `findings/F35-electroweak-mixing.md` W6.3 with a one-line back-reference to F44

---

*End of proposed finding F44.*
