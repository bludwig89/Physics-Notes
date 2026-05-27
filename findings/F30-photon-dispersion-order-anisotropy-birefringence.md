# Finding 30 — The photon-dispersion LIV order is anisotropic; the linear term is chiral (birefringent), not a net time-of-flight effect

**Date:** 2026-05-24 - 17:31
**Status:** Confirmed — Tier 1 exact (sympy series, exact rational coefficients) + Tier 2 high-precision numeric (mpmath log-log slopes)
**Script:** `model-tests/test_F30_dispersion_order.py`
**Results:** `test-results/F30_dispersion_order.json`, `test-results/F30_dispersion_order_summary.md`

---

## Why this finding exists

The project carried a direct contradiction about the leading correction to the photon dispersion $\Omega(\mathbf{k}) = 2\,\omega_\text{BCC}(\mathbf{k}/2)$:

- **F25 / F26 / F28** stated the correction is **quadratic** in $k$: $\delta v_\phi/c \approx -\Omega^2/6 \approx -c_\text{lat}^2 k^2/6$ — i.e. an $n=2$ (quadratic-in-energy) LIV effect, which F28 found to be ~15 decades below any current bound and effectively unfalsifiable.
- **`roadmap-f26-rotation.md`** (Phase 3/4, written one day later) stated the correction along the BCC body diagonal is **linear**: $\delta v_\phi/c \approx -k/18$ — i.e. an $n=1$ (linear-in-energy) effect, which would be *already excluded* by GRB 090510 if it were a net time-of-flight effect.

These imply opposite experimental fates. This finding settles it from the exact dispersion.

---

## The dispersion under test

The BCC Weyl bands are (Paper 1 Eq. 15, `ca_bcc.bcc_dispersion`):

$$\omega^\pm(\mathbf{k}) = \arccos\!\big(c_x c_y c_z \pm s_x s_y s_z\big),\qquad c_i=\cos(k_i/\sqrt3),\ s_i=\sin(k_i/\sqrt3),$$

and the composite (bilinear) photon is $\Omega^\pm(\mathbf{k}) = 2\,\omega^\pm(\mathbf{k}/2)$, with $c_\text{lat} = 1/\sqrt3$. The $\pm$ is the **chirality / Weyl-band** label; the chiral piece is the determinant term $\det = s_x s_y s_z$.

We Taylor-expand $\Omega^\pm$ along three symmetry directions (sympy, exact rationals) and confirm each exponent with a 50-digit mpmath log-log slope of the residual $|\Omega-c_\text{lat}k|$ (the float64 slope is corrupted by catastrophic cancellation; high precision is required).

---

## Result 1 — The correction order is direction-dependent (single chirality, sign $+$)

| Direction | $\Omega^+(k)$ exact series | leading correction to $\Omega$ | $\delta v_\phi/c$ | $n_\text{LIV}$ | numeric slope |
|---|---|---|---|---|---|
| $(1,0,0)$ axis | $\dfrac{k}{\sqrt3}$ | none | $0$ | — | (residual $\equiv 0$) |
| $(1,1,0)$ face-diag | $\dfrac{k}{\sqrt3} - \dfrac{\sqrt3\,k^3}{864} - \dots$ | $-\dfrac{\sqrt3}{864}k^3$ | $-\dfrac{k^2}{288}$ | **2** | $3.0000$ |
| $(1,1,1)$ body-diag | $\dfrac{k}{\sqrt3} - \dfrac{\sqrt3\,k^2}{54} - \dfrac{\sqrt3\,k^3}{486} - \dots$ | $-\dfrac{\sqrt3}{54}k^2$ | $-\dfrac{k}{18}$ | **1** | $2.0020$ |

The BCC vacuum is **anisotropic**: the speed of light is exactly $c_\text{lat}=1/\sqrt3$ along the cube axes (no LIV at any order), picks up a quadratic correction along face diagonals, and a **linear** correction $-k/18$ along body diagonals. The roadmap's $-k/18$ is therefore correct *for a single chirality branch*; the F25/F26/F28 "$-\Omega^2/6$ everywhere" claim was an artifact of assuming an isotropic 1-D arccos dispersion.

---

## Result 2 — The linear term is **chiral**: it cancels in unpolarised light, surviving only as birefringence

Decomposing each direction into the chirality-even part $\tfrac12(\Omega^+ + \Omega^-)$ (what unpolarised time-of-flight sees) and the chirality-odd part $\tfrac12(\Omega^+ - \Omega^-)$ (the birefringent splitting):

| Direction | unpolarised time-of-flight (even) | birefringence (odd) |
|---|---|---|
| $(1,0,0)$ | no correction | $0$ |
| $(1,1,0)$ | $\delta v/c \sim k^2$ — **n=2** | $0$ |
| $(1,1,1)$ | $\delta v/c \sim k^2$ — **n=2** | $\delta v/c \sim k^1$ — **n=1** |

Along $(1,1,1)$ the two chiralities split with **opposite sign**: $\Omega^+ = c_\text{lat}k - \tfrac{\sqrt3}{54}k^2$ (subluminal), $\Omega^- = c_\text{lat}k + \tfrac{\sqrt3}{54}k^2$ (superluminal), so

$$\Omega^+ - \Omega^- = -\frac{\sqrt3}{27}k^2 \quad\Longrightarrow\quad \frac{\Delta v_\phi}{c}\Big|_\text{birefringence} = -\frac{k}{9}\ \ \text{(linear in }k).$$

When the two helicities are equally populated, **the linear terms cancel** and the net (unpolarised) dispersion is quadratic ($n=2$) along *every* direction. The linear $-k/18$ does not disappear — it migrates into a **polarisation-dependent** velocity splitting.

---

## Resolution of the discrepancy

Both prior statements describe real features of different observables, and conflating them caused the contradiction:

1. **F28's "$n=2$, ~15 decades below sensitivity, effectively unfalsifiable" conclusion stands — but for a subtler reason than stated.** The net unpolarised photon time-of-flight is quadratic not because the fundamental dispersion is quadratic, but because the linear chiral terms cancel between the two helicities. The chirality-even dispersion is $\delta v/c = -k^2/162$ along $(1,1,1)$, genuinely $n=2$.

2. **The roadmap's linear $-k/18$ is the correct single-chirality value.** It is physical, but it manifests as **vacuum birefringence**, not as a net arrival-time shift.

3. **A new, much sharper prediction emerges:** *linear-in-energy vacuum birefringence, maximal along BCC body diagonals and exactly zero along the cube axes.* Birefringence (energy-dependent rotation of the polarisation plane of distant sources) is constrained far more tightly than time-of-flight — typically many orders of magnitude beyond the Planck scale for $n=1$. This, not GRB time-of-flight, is the decisive test of F26.

---

## Critical open item — is the birefringence physically realised?

The composite photon in `ca_maxwell.py` is currently built from a **single chirality branch** (`weyl_eigenmodes_3d_bcc(..., sign='+')`; the photon's $\psi,\phi$ are the $+\omega$ and $-\omega$ eigenmodes of the *same* `sign='+'` unitary — `maxwell_curl_residual`, lines 226–235). As coded, the model photon therefore carries the single-chirality linear dispersion $-k/18$.

Whether the **physical** photon is birefringent depends on an identification not yet established in the code:

> Do the two physical photon helicities (the two circular polarisations / the $\mathbf{F}=\mathbf{E}\pm i\mathbf{B}$ Riemann–Silberstein eigenstates) correspond to the two BCC chirality branches $\Omega^+$ and $\Omega^-$?

- If **yes**, F26 predicts linear vacuum birefringence — a strong, possibly already-excluded signal that must be confronted with GRB/AGN polarisation bounds.
- If **no** (e.g. both helicities live in one branch, or the physical photon is the chirality-even combination by construction), the net effect is $n=2$ and F26 remains safe, but then the single-branch code is modelling only half the photon.

Either way, the current single-branch construction is incomplete for dispersion phenomenology. **Next step:** extend the composite-photon construction to both branches (`sign='+'` and `sign='-'`) and read off how the two physical polarisations inherit $\Omega^\pm$.

---

## Magnitudes (Planck-tick assumption)

With tick $=t_P$ and spacing $=\ell_P$, the dimensionless lattice wavenumber maps as $k=\sqrt3\,E/E_P$ (from $E=\hbar\Omega/\tau$, $\Omega=c_\text{lat}k$).

- **Single-chirality group velocity along $(1,1,1)$:** $\delta v_g/c = -k/9 = -\tfrac{\sqrt3}{9}(E/E_P) \approx -0.1925\,(E/E_P)$, i.e. an effective linear scale $E_{\text{QG},1}\approx 3\sqrt3\,E_P \approx 5.2\,E_P$. This sits *below* the Fermi-LAT GRB 090510 bound ($E_{\text{QG},1}\gtrsim 7.6\,E_P$) — so if this were a net time-of-flight effect it would be excluded. It is not (it cancels in unpolarised light), which is exactly why the distinction in Result 2 matters.
- **A coarser-than-Planck tick makes the linear effect worse, not better** ($k=\sqrt3\,\tau E/\hbar$ grows with $\tau$), so the linear term cannot be tuned away by choosing a larger tick — only the chiral cancellation protects the net time-of-flight.
- **Net (unpolarised) effect** is the quadratic $E_{\text{QG},2}\sim\sqrt2\,E_P$ of F28 — untestable by foreseeable time-of-flight (see [[F28-grb-dispersion-test]]).

---

## What is exact vs numeric

| Result | Tier |
|---|---|
| $\Omega^+_{(1,0,0)} = k/\sqrt3$ exactly (no LIV on axis) | Tier 1 exact (sympy) |
| Leading coeffs $-\sqrt3/864\,k^3$ (110), $-\sqrt3/54\,k^2$ (111) | Tier 1 exact (sympy, exact rationals) |
| Chirality-even $n=2$ along all directions; chirality-odd $n=1$ on $(1,1,1)$ | Tier 1 exact (sympy decomposition) |
| Birefringence $\Omega^+-\Omega^- = -\sqrt3\,k^2/27$ on $(1,1,1)$ | Tier 1 exact (sympy) |
| Log-log slopes $3.0000$ (110), $2.0020$ (111) | Tier 2 numeric (mpmath, 50 dps) |

---

## Supersedes / refines

- **F25, F26** — the statement "$\delta v_\phi/c \approx -\Omega^2/6$" is corrected: that is not the leading correction along $(1,1,1)$ (which is linear, $-k/18$) and the quadratic appears only as the chirality-even average. Their core results (exact real rotation; $c_\text{lat}=d\Omega/d|\mathbf{k}|$; energy conservation geometric) are unchanged.
- **F28** — verdict (quadratic, untestable by time-of-flight) is upheld for the *unpolarised* observable, now with the correct mechanism (chiral cancellation), and is reclassified as the time-of-flight channel only; the birefringence channel is the new sharp test.
- **roadmap-f26-rotation.md** — the $-k/18$ value is confirmed as the exact single-chirality body-diagonal correction.

---

## Cross-references

- [[F26-speed-of-light-as-rotation-rate]]: the rotation reframing this tests
- [[F25-real-rotation-exact-discrete-time-maxwell]]: exact rotation underlying $\Omega(\mathbf{k})$
- [[F28-grb-dispersion-test]]: time-of-flight bounds (the unpolarised channel)
- [[F22-velocity-addition-deformed-formula]]: the analogous massive arccos nonlinearity
- `model-tests/test_F30_dispersion_order.py`, `ca-simulation/ca_bcc.py::bcc_dispersion`, `ca-simulation/ca_maxwell.py::maxwell_curl_residual` (single-branch photon, lines 226–235)
