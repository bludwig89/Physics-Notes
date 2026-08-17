# Finding 17 — Poynting Energy Density $\|E_G\|^2 + c^2\|B_G\|^2$ is Exactly Conserved for Composite-Photon Propagation

> **[PARTIALLY SUPERSEDED 2026-06-01 by F69 — ledger S1-F69-sigma-bilinear-photon]**
>
> **DEAD:** Every PHOTON claim: that this is the Poynting energy of the electromagnetic photon, that it 'closes Mohr Gap C4', that it is 'the De Broglie neutrino theory of light at the QCA level', and that it is 'stronger than the continuum requirement'. The object is the retired single-branch sigma-bilinear, and the normalisation fails Mohr Eq. 47 (|cB|/|E| = c_lat = 0.5774 where an energy density needs 1), so the conserved quantity is a c-dependent multiple of the bilinear's Hermitian norm — a probability normalisation, not an energy. The finding also presents 'selects circular polarization by construction' as a virtue; that is exactly the single-helicity restriction F65 names as the escape hatch that contradicts observed linear polarization.
>
> **STILL LIVE:** The algebra, which is EXACT and stronger than the finding claims for itself: G_T . G_T = 0 identically for a helicity eigenspinor, by the Fierz identity (phi^T sigma psi).(phi^T sigma psi) = (phi^T psi)^2 together with n_hat . G = psi^T psi. This is the Riemann-Silberstein null-field condition and it carries over to the W/Z/gluon sector where the sigma-bilinear is still canonical. Note the review's live defect: ||G_T||^2 = 2(n_hat . y_hat)^2, so the object is not a rotational 3-vector (35% measured error) and vanishes on the great circle n_hat perp y_hat — a hazard in the sectors this record RETAINS, not in the photon channel it kills.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


*2026-05-21*

> **⚠ PARTIALLY SUPERSEDED 2026-08-03 by [[F69-paired-spinor-photon]] — ledger `S1-F69-sigma-bilinear-photon`. Retired to `deprecated/findings/`; finding number 17 is a declared gap.**
>
> **DEAD:** every **photon** claim — that this is the Poynting energy of the electromagnetic photon, that it "closes Mohr Gap C4", that it is "the De Broglie neutrino theory of light at the QCA level", and that it is "stronger than the continuum requirement". The object is the retired single-branch σ-bilinear (`bilinear.py`: *"RETIRED AS THE PHOTON (2026-06-01, F69) … Do NOT use these helpers as the U(1) photon"*), and it is superseded twice — structurally by F39, as the photon by F69. The normalisation also fails Mohr Eq. 47: the construction gives $\lvert cB\rvert/\lvert E\rvert = c_\text{lat} = 0.5774$ where an energy density needs 1, so the conserved quantity is a $c$-dependent multiple of the bilinear's Hermitian norm — a probability normalisation, not an energy. And "selects circular polarization by construction" is presented here as a virtue; it is precisely the single-helicity restriction F65 names as the escape hatch that *contradicts observed linear polarization*.
>
> **STILL LIVE:** the algebra, which is **exact** and stronger than this file claims for itself. $G_T\!\cdot\!G_T \equiv 0$ identically for a helicity eigenspinor, by the Fierz identity $(\phi^{\mathsf T}\sigma\psi)\!\cdot\!(\phi^{\mathsf T}\sigma\psi)=(\phi^{\mathsf T}\psi)^2$ with $\hat n\!\cdot\!G=\psi^{\mathsf T}\psi$ — the Riemann–Silberstein null-field condition. The §Step-4 bounds below ($<10^{-14}$, $<10^{-13}$) are numerical bounds on an algebraic zero. This carries over to the W/Z/gluon sector, where the σ-bilinear is still canonical — **and so does the review's live defect**: $\lVert G_T\rVert^2 = 2(\hat n\!\cdot\!\hat y)^2$, so the object is not a rotational 3-vector (35% measured error) and its field vanishes on the great circle $\hat n\perp\hat y$.
>
> See `docs/theory/supersessions.yaml` for the full record.

**Status:** Confirmed. Algebraically exact at machine precision; per-step residual $\approx \varepsilon_\text{machine}$, linear-in-$N$ accumulation only.

**Reviewed:** 2026-08-03 — **OVERSTATED** ([independent review](../../docs/reviews/F17-review-2026-08-03.md))

---

## Motivation

Mohr (2010), Eq. (55) identifies the Poynting energy density of the six-component photon wave function as

$$u = \bar\Psi\,c p^0\,\Psi = \tfrac{1}{2}\!\left(\varepsilon_0|\boldsymbol{E}|^2 + \tfrac{|\boldsymbol{B}|^2}{\mu_0}\right) = \tfrac{1}{2}\!\left(|\boldsymbol{E}|^2 + c^2|\boldsymbol{B}|^2\right) \quad\text{(SI natural units, }c\text{ explicit)}.$$

Our composite-photon model builds $E_G, B_G$ as bilinears of two BCC Weyl QCA spinors (Paper 1, Eq. 35). Norm conservation of the individual Weyl spinors was already established (machine-$\varepsilon$, L1–L2 suites). Whether the **EM-field-level energy density** $\|E_G(t)\|^2 + c^2\|B_G(t)\|^2$ is separately conserved during composite-photon propagation had never been checked.

---

## Result

$$\boxed{\|E_G(t)\|^2 + c^2\|B_G(t)\|^2 = \text{const} \quad \text{for all } t, \text{ exactly algebraic}}$$

| Run | Steps | Directions | $k_\text{mag}$ | Max rel deviation |
|---|---|---|---|---|
| Standard gate (200 steps) | 200 | 12 | 0.05 | $4.77 \times 10^{-14}$ |
| Long run | 10 000 | 12 | 0.05 | $1.82 \times 10^{-12}$ |

Per-step rate (from the long run): $1.82\times 10^{-12} / 10\,000 = 1.82\times 10^{-16} \approx \varepsilon_\text{machine}$.

The $c^2$ form (Mohr Eq. 55) is conserved to the same precision as the simpler $\|E\|^2 + \|B\|^2$ form already in the inventory (Tier 2 #7). The per-step residual is consistent with pure IEEE-754 rounding accumulation.

---

## Analytic Argument

### Step 1 — Bilinear time evolution

Under one CA tick with both Weyl modes evolving as $e^{-i\omega_\text{half}}$, the bilinear $G(k) = \phi^T \sigma \psi$ acquires the photon phase:

$$G_T(t) \;\to\; e^{-i\Omega t}\,G_T(0), \qquad \Omega = 2\omega_\text{half}.$$

### Step 2 — $\|E\|^2 + \|B\|^2$ conservation (already known)

Writing $G_T = \boldsymbol{A} + i\boldsymbol{C}$ ($\boldsymbol{A}, \boldsymbol{C}$ real 3-vectors):

$$E_G = 2|n|\,\boldsymbol{A}, \quad B_G = 2|n|\,\boldsymbol{C}
\implies \|E\|^2 + \|B\|^2 = 4|n|^2\,\|G_T\|^2 = \text{const}.$$

This holds because $\|e^{-i\Omega}G_T\|^2 = \|G_T\|^2$ identically.

### Step 3 — $\|E\|^2 + c^2\|B\|^2$ requires equal-amplitude circularity

The $c^2$-weighted form is conserved for all $\Omega$ if and only if:

1. $\|\boldsymbol{A}\|^2 = \|\boldsymbol{C}\|^2$ (equal real and imaginary parts)
2. $\boldsymbol{A} \cdot \boldsymbol{C} = 0$ (orthogonal real and imaginary parts)

This is precisely the **circular polarization** condition. Under rotation by $\Omega$, $\boldsymbol{A}$ and $\boldsymbol{C}$ mix, but $\|\boldsymbol{A}'\|^2 + c^2\|\boldsymbol{C}'\|^2 = \|\boldsymbol{A}\|^2 + c^2\|\boldsymbol{C}\|^2$ if and only if both conditions hold — independent of $c$.

### Step 4 — The BCC eigenmode bilinear is circularly polarized

For the BCC positive-helicity Weyl eigenmode $\psi_+$ (the unique spinor satisfying $\hat{n}\cdot\sigma\,\psi_+ = \psi_+$), the transpose bilinear $G = \psi_+^T\,\sigma\,\psi_+$ gives a complex vector in the plane transverse to $\hat{n}$ satisfying the circular polarization conditions to machine precision:

$$\frac{|\boldsymbol{A}\cdot\boldsymbol{C}|}{\|G_T\|^2} < 10^{-14}, \qquad
\frac{\big|\|\boldsymbol{A}\|^2 - \|\boldsymbol{C}\|^2\big|}{\|G_T\|^2} < 10^{-13}$$

over 12 random $\hat{k}$ directions at all tested $k$ magnitudes ($10^{-4}$ to $4\times 10^{-1}$).

This is the lattice realisation of the quantum-optical identity: a state of **two identical helicity-$\tfrac12$ spinors** (both $\psi_+$) combines into a **helicity-$1$ circularly polarized photon**. This is the De Broglie neutrino theory of light at the QCA level.

### Step 5 — Consequence

For circular polarization $G_T = r e^{i\alpha}\hat\varepsilon_\text{circ}$ with $|\hat\varepsilon_\text{circ}| = 1$:

$$\|E_G(t)\|^2 + c^2\|B_G(t)\|^2
= 4|n|^2 r^2 \!\left(\|\mathrm{Re}(e^{i\theta}\hat\varepsilon_\text{circ})\|^2 + c^2\|\mathrm{Im}(e^{i\theta}\hat\varepsilon_\text{circ})\|^2\right)
= 4|n|^2 r^2 \cdot \tfrac{1+c^2}{2} = \text{const},$$

where the last equality uses $\|\mathrm{Re}(e^{i\theta}\hat\varepsilon)\|^2 = \|\mathrm{Im}(e^{i\theta}\hat\varepsilon)\|^2 = \tfrac12$ for all $\theta$ when $\hat\varepsilon$ is a circular polarization unit vector.

The conservation is therefore:
- **c-independent** — holds for any $c$, including $c_\text{lat} = 1/\sqrt{3}$
- **instantaneous** — not merely averaged over a cycle
- **algebraically exact** — bounded only by floating-point round-off

---

## Significance

This closes Gap C4 from the Mohr summary (`references/mohr-2010-maxwell-photon-wf-summary.md`). It confirms that the composite-photon bilinear respects the full Poynting energy conservation law of Maxwell's equations at the EM-field level, not merely the Weyl spinor norm conservation. The result is stronger than the continuum requirement (which only conserves the spatially integrated energy for a plane wave), because it holds **pointwise in $k$-space at every time step**.

The circular-polarization origin is physically meaningful: the BCC composite-photon construction **selects circular polarization by construction** when both Weyl spinors are in the same helicity eigenstate. This is consistent with the photon being a definite-helicity state ($h = \pm 1$).

---

## Numerical verification

```
Function: ca_maxwell.composite_photon_energy_conservation_c2()
k-scan results (200 steps, 12 directions):

  k=1e-04   ||E||²+c²||B||²  1.47e-13  (near-k=0 floating-point noise)
  k=5e-02   ||E||²+c²||B||²  4.77e-14
  k=1e-01   ||E||²+c²||B||²  4.57e-14
  k=2e-01   ||E||²+c²||B||²  3.33e-14
  k=3e-01   ||E||²+c²||B||²  3.63e-14

Per-step rate (10 000-step run, k=0.05): ~1.4e-16 ≈ ε_machine
```

**Gate:** max rel dev $\le 10^{-12}$ over 200 steps. **PASS** at $4.77\times 10^{-14}$.

---

## Cross-references

- `docs/status/exactness-inventory.md` Tier 2 #10 (C4 refinement — Mohr Eq. 55)
- `docs/theory/ca-reference.md` §Mohr composite-photon energy conservation
- `references/mohr-2010-maxwell-photon-wf-summary.md` §C4 (Gap now closed)
- `ca_maxwell.py` `composite_photon_energy_conservation_c2()`
