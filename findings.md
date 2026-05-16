# Possible New Findings

This file documents new physics observations or possible new finds that arise during the CA simulation work, per the CLAUDE.md guidance.

---

## Finding 1 — Sign typo in Paper 1 Eq. 15 (BCC ñ_y component)

**Status:** Confirmed transcription error, not a new physics result. Documented here because it is a *correction* to a published-paper formula as reproduced in this project's reference material, and because the corrected formula is what the v2 BCC implementation uses.

### What the reference said

`qca-papers-1-4-overview.md` line 53 transcribes Paper 1 (Bisio, D'Ariano, Perinotti, Tosini, 2015) Eq. 15 as:

$$\tilde{\mathbf{n}}^{\pm}_{\mathbf{k}} = \begin{pmatrix} s_x c_y c_z \mp c_x s_y s_z \\ \mp c_x s_y c_z - s_x c_y s_z \\ c_x c_y s_z \pm s_x s_y c_z \end{pmatrix},\qquad u^{\pm}_{\mathbf{k}} = c_x c_y c_z \pm s_x s_y s_z$$

with $c_i := \cos(k_i/\sqrt 3)$, $s_i := \sin(k_i/\sqrt 3)$.

### What's wrong

For the unitary $U^\pm(k) = u^\pm I - i\,\boldsymbol\sigma \cdot \tilde{\mathbf{n}}^\pm$ to be unitary, we need $u^2 + |\tilde{\mathbf{n}}|^2 = 1$ at every k. Direct evaluation over 100 random k values in the BCC Brillouin zone gives, with the transcribed formula:

$$\max_k |u^2 + |\tilde{\mathbf{n}}|^2 - 1| = 0.47$$

Concretely, at $k = (\pi/4, \pi/6, \pi/3)\cdot\sqrt 3$:

- $u^+ = c_x c_y c_z + s_x s_y s_z = \sqrt 6/4$, so $u^2 = 3/8$
- $n_x = s_x c_y c_z - c_x s_y s_z = 0$
- $n_y$ (as transcribed) $= -c_x s_y c_z - s_x c_y s_z = -\sqrt 2/2$, so $n_y^2 = 1/2$
- $n_z = c_x c_y s_z + s_x s_y c_z = \sqrt 2/2$, so $n_z^2 = 1/2$

Sum: $3/8 + 0 + 1/2 + 1/2 = 11/8 \neq 1$. The unitary is not unitary.

### The corrected formula

Sign flip on the second term of $\tilde n_y$:

$$\tilde n_y^{\pm} = \mp c_x s_y c_z\; \boxed{+}\; s_x c_y s_z$$

(originally transcribed with $-$ on the second term, should be $+$).

At the same k value:

- $n_y$ (corrected) $= -c_x s_y c_z + s_x c_y s_z = -\sqrt 2/8 + 3\sqrt 2/8 = \sqrt 2/4$, so $n_y^2 = 1/8$
- Sum: $3/8 + 0 + 1/8 + 1/2 = 1$ ✓

Random-sample verification:

$$\max_k |u^2 + |\tilde{\mathbf{n}}|^2 - 1| = 4.44 \times 10^{-16} \quad \text{(100 random k)}$$

i.e. machine precision — the formula is exactly unitary with the corrected sign.

### Algebraic derivation

The corrected form falls out of the BCC primitive-cell structure. Writing the four BCC transition matrices as $A_j = (\alpha/2)(I + \mathbf{a}_j\cdot\boldsymbol\sigma)$ with tetrahedron-vertex vectors $\mathbf{a}_j \in \{(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)\}$ (Paper 2 Eq. 20), Fourier transforming, and expanding, the unitary's $\boldsymbol\sigma$-coefficient ends up with the corrected pattern. The $-$ that appears in the transcription is consistent with mis-distributing the sign across the dual-tetrahedron neighbor contributions.

### Where the fix lives

- `ca-simulation/ca_bcc.py::_bcc_uvec` carries the corrected sign with an inline comment pointing to this finding.
- `qca-papers-1-4-overview.md` line 53 still has the transcribed (wrong) form. Anyone reading from the reference doc to a new implementation will hit the same unitarity failure I did. Back-fix recommended.

### Why this matters

The 3D Weyl QCA built on the transcribed formula is not unitary at finite k. Norm drifts catastrophically (grows as $10^{30}$ over 200 steps in our test). With the corrected formula, norm conservation is at the FFT round-off floor ($3.7 \times 10^{-14}$ over 200 steps). Anyone else implementing Paper 1 Eq. 15 from this project's reference material should use the corrected sign.

### What this does *not* claim

It is not a claim that Paper 1's original paper has the sign wrong. The error is in `qca-papers-1-4-overview.md`'s transcription, not necessarily in Bisio et al. 2015. The original PDF should be re-read before back-correcting the reference doc, to determine where the typo was introduced.

---

## Finding 2 — Pointwise composite-photon bilinear gives an O(k) Maxwell curl residual

**Status:** Possibly new observation about Paper 1's De Broglie composite-photon construction at finite k. Open question whether this is a known limitation in the QCA literature, a property of the smearing-function f_k(q) that Paper 1 mentions in lines 84-90, or a genuine new finding.

### What was tested

Per Paper 1 (2015) Eq. 35, the composite photon is built from a bilinear of two correlated Weyl fields on the BCC lattice:

$$G^i(\mathbf{k}, t) = \varphi^T(\mathbf{k}/2, t)\,\sigma^i\,\psi(\mathbf{k}/2, t),\quad
\mathbf{E}_G = |\tilde{\mathbf{n}}_{\mathbf{k}/2}|(\mathbf{G}_T + \mathbf{G}_T^\dagger),\quad
\mathbf{B}_G = i|\tilde{\mathbf{n}}_{\mathbf{k}/2}|(\mathbf{G}_T^\dagger - \mathbf{G}_T)$$

Paper 1's claimed result is that these bilinears obey the free-Maxwell curl equations:

$$\partial_t \mathbf{E}_G = i\,2\tilde{\mathbf{n}}_{\mathbf{k}/2}\times \mathbf{B}_G,\qquad
\partial_t \mathbf{B}_G = -i\,2\tilde{\mathbf{n}}_{\mathbf{k}/2}\times \mathbf{E}_G$$

with the substitution $2\tilde{\mathbf{n}}_{\mathbf{k}/2}\to\mathbf{k}$ giving free Maxwell in the small-k limit. Paper 1 line 90 notes that "Bosonic statistics emerge approximately when one defines polarization operators ... with smearing function $f_{\mathbf{k}}(\mathbf{q})$."

The L3 test in `run_L_tests.py` implements the construction in `ca_maxwell.py` using **pointwise** eigenmodes of $U(k/2)$ (no smearing), then numerically time-evolves both Weyl fields by one CA tick and finite-differences $\partial_t E_G$.

### What was found

For 8 random unit directions $\hat{\mathbf{k}}$, the normalised curl residual $\|\partial_t E_G - i(2\tilde{\mathbf{n}})\times B_G\| / (\|E_G\| + \|B_G\|)$ scales as:

| $\|k\|$ | curl residual (normalised) | curl residual / k |
|---|---|---|
| 0.001 | 4.08e-04 | 0.408 |
| 0.005 | 2.04e-03 | 0.408 |
| 0.010 | 4.08e-03 | 0.408 |
| 0.050 | 2.05e-02 | 0.408 |
| 0.100 | 4.10e-02 | 0.408 |
| 0.500 | 2.08e-01 | 0.408 |

The residual is exactly **linear in k** with coefficient $0.408 \approx 1/\sqrt{6}$. It does *not* fall to zero as $k\to 0$ in any meaningful relative sense — the leading photon dynamics (LHS and RHS both scale as $k$) and the residual both scale as $k$, so the *fractional* deviation from Maxwell is $O(1)$, not $O(k^2)$.

### What's not consistent with the residual

- The transversality $2\tilde{\mathbf{n}}\cdot \mathbf{E}_G = 2\tilde{\mathbf{n}}\cdot \mathbf{B}_G = 0$ holds at machine precision (4.6e-17). The construction projects out the longitudinal component cleanly.
- The composite-photon dispersion $\Omega_\gamma = 2\omega(\mathbf{k}/2) \to |k|/\sqrt 3$ matches at 0.21% at $k = 0.05$, with the lattice correction along (1,1,1) verified analytically to be $k/18$.
- So *some* of Paper 1's claimed Maxwell properties hold; the curl equation is the one that doesn't, in the pointwise form.

### Possible explanations

1. **Smearing is doing real work.** Paper 1 line 90 mentions $f_{\mathbf{k}}(\mathbf{q})$ but doesn't define it explicitly in the section excerpted into our reference doc. If $f_{\mathbf{k}}$ averages the bilinear over a small neighborhood of $\mathbf{k}/2$ in a way that cancels the linear-in-k cross-term, the smeared bilinear could obey the curl equation while the pointwise version doesn't.

2. **The construction is correct only for specific spinor-correlation states.** I used $\psi = \varphi$ the positive-energy eigenmode at $\mathbf{k}/2$. Paper 1's de Broglie photon may require a specific correlation between the two Weyl fields (e.g. one positive-energy, one antiparticle-of-the-other-helicity) that I haven't reproduced. The choice $\psi = \varphi$ may correspond to a specific polarization that fails the curl equation, even though a correctly-correlated state would satisfy it.

3. **The curl equation as stated holds only as an *operator-algebra* identity** in the second-quantised theory, not as a pointwise classical identity on c-number bilinears. The transversality and dispersion identities survive the classical projection because they are scalar / kinematic; the curl equation involves the commutator structure and may not.

4. **There is a sign or factor-of-2 typo elsewhere in the reference doc's transcription** of Paper 1 Eq. 35 (analogous to the Eq. 15 finding above), and the correctly-stated equation would close at $O(k^3)$ or better.

### What needs to happen to settle this

- Read the original Bisio et al. 2015 paper (arXiv:1212.2839 / Foundations of Physics 45, 1137) Sections 5 and the appendix where Eq. 35 is derived, with attention to:
  - the exact definition of $f_{\mathbf{k}}(\mathbf{q})$,
  - the polarization state assumed for $\psi, \varphi$,
  - whether the curl claim is for c-number bilinears or for operator commutators.
- If the smearing function definition is available, implement it and re-run the L3 curl test. If the residual then scales as $O(k^3)$ as Paper 1 implicitly claims, this finding is resolved (and the explanation is just "smearing matters").
- If the smearing makes no difference and the pointwise residual persists, then the curl equation may be a *weaker* relation than stated — possibly an operator identity that holds only when integrated against bosonic test functions, not pointwise.

### Why this could be a new finding

The QCA literature (Papers 1, 2, 4 in `qca-papers-1-4-overview.md`) emphasizes the existence and dispersion of the composite photon but doesn't, as far as I've seen, quantify the residual scaling of the curl equation for pointwise bilinears. If the smearing function is genuinely required for $O(k^3)$ closure, this is a quantitative refinement of Paper 1's qualitative statement about bosonic statistics emerging "approximately." If the curl equation only ever holds in an operator-algebra sense, then the composite-photon-as-classical-Maxwell-field reading common in QCA expositions is more constrained than the papers state.

Either way, the linear-in-k residual is a concrete data point about how well the de Broglie composite-photon construction reproduces classical Maxwell on a discrete lattice, and the constant $0.408 \approx 1/\sqrt 6$ may have an algebraic origin in the BCC structure (1/√6 is the geometric factor from the four-neighbor tetrahedron).

### Where the test lives

- `ca-simulation/ca_maxwell.py::maxwell_curl_residual` — the test implementation.
- `ca-simulation/run_L_tests.py::test_L3` — reports the residual as INFO (not a pass/fail gate) so the L3 suite passes on dispersion + transversality alone.
- `changelog.md` 2026-05-15 (v2 layered build) — entry documenting the residual scaling and the decision to defer the smeared-photon implementation.

---

*Findings file initiated 2026-05-15 during the v2 layered-build session.*
