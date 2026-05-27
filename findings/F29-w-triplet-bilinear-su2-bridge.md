# F29 — W-triplet bilinear bridges F26 (photon rotation law) to F27 (chiral SU(2))

**Date:** 2026-05-23 - 19:30
**Files:**
- `model-tests/test_su2_photon_bridge.py` — 8-test suite
- `test-results/F29_su2_photon_bridge.json` — numerical results
**Linked findings:** F26 (rotation law), F27 (chiral SU(2)), F17 (Poynting energy)

---

## Motivation

F26 reframes the photon as the (E, B) pair rotating at angular rate
$\Omega(k) = 2\,\omega_\text{BCC}(k/2)$, with $c_\text{lat} = 1/\sqrt 3$ as the
small-$k$ slope. F27 derives chiral SU(2)$_L$ as a local gauge symmetry of
the complex-mass coupling. Until now, the two sectors lived in different
modules with no tested bridge: the photon is built from singlet Weyl
spinors; the SU(2) acts on the isospin doublet.

**Question.** If we extend the photon bilinear to isospin doublets and form
the natural **triplet** analog using $\tau^a$ on the isospin index, does
that "W-triplet" object obey the same rotation law (F26) as the photon,
and is the construction SU(2)-clean (F27)?

---

## Construction

Let $\psi_\text{doublet} = (\psi^\nu, \psi^e)$, each a 2-spinor on the
BCC lattice. Define two doublet bilinears at $k/2$:

**Singlet (photon analog):**

$$G_H^i(k) = \sum_\alpha (\phi^\alpha)^\dagger\,\sigma^i\,\psi^\alpha$$

**Triplet (W analog):**

$$W_H^{a,i}(k) = \sum_{\alpha,\beta} (\tau^a)_{\alpha\beta}\,(\phi^\alpha)^\dagger\,\sigma^i\,\psi^\beta$$

Both use **Hermitian** conjugation $\phi^\dagger$ instead of the Paper 1
transpose $\phi^T$. (The transpose form fails SU(2) invariance because
$V^T V \ne I$ for $V \in \mathrm{SU}(2)$ — see Extra test.)

The W-triplet $E^a, B^a$ fields then follow Paper 1 Eq. 35 form per $a$:

$$E^a = |n_{k/2}|\,(W_T^a + (W_T^a)^\dagger),\quad B^a = i|n_{k/2}|\,((W_T^a)^\dagger - W_T^a)$$

---

## Test Suite Results (8/8 PASS, 0.025 s total)

| # | Test | Residual | Notes |
|---|---|---|---|
| A1 | $\Omega(k)$ invariant under SU(2) on doublet | $5.59\times 10^{-15}$ | Machine precision |
| B1 | Hermitian singlet $G_H^i$ is SU(2)-invariant | $2.24\times 10^{-16}$ | Exact |
| B2 | Triplet rotates as adjoint: $W^a \to R^{ab}(V) W^b$ | $3.08\times 10^{-16}$ | Exact |
| B3 | $\sum_a \|W^a\|^2$ is SU(2)-invariant | $6.66\times 10^{-16}$ | Exact |
| B4 | Triplet transversality at small $k$ | $c_\text{lat}\,k$ | Same as photon |
| B5 | Per-component rotation law energy conservation | $0.0$ | Exact |
| B5b | Triplet rotation energy conserved before AND after SU(2) | $7.18\times 10^{-16}$ / $1.45\times 10^{-16}$ | Exact |
| Extra | Transpose form $G_T^i$ NOT SU(2)-invariant | max deviation $4.18$ | Structural |

---

## Key Results

### 1. Each W-triplet component obeys the photon rotation law (F26)

For each isospin $a \in \{1,2,3\}$, the pair $(E^a, B^a)$ rotates under

$$\begin{pmatrix} E^a_\text{new} \\ B^a_\text{new} \end{pmatrix} = \begin{pmatrix} \cos\Omega & \sin\Omega \\ -\sin\Omega & \cos\Omega \end{pmatrix} \begin{pmatrix} E^a \\ B^a \end{pmatrix},\quad \Omega(k) = 2\omega_\text{BCC}(k/2)$$

with **exactly conserved** magnitude $\|E^a\|^2 + \|B^a\|^2$ (residual 0.0,
test B5). Each $W^a$ is a Lorentz-vector photon-like field with identical
dispersion.

### 2. W-triplet transversality matches photon exactly

Residual scales as $c_\text{lat}\,|k|$ (test B4):

| $k$ | W triplet residual | $c_\text{lat}\,k$ |
|---|---|---|
| 0.005 | $2.887\times 10^{-3}$ | $2.887\times 10^{-3}$ |
| 0.01  | $5.775\times 10^{-3}$ | $5.774\times 10^{-3}$ |
| 0.02  | $1.155\times 10^{-2}$ | $1.155\times 10^{-2}$ |
| 0.05  | $2.891\times 10^{-2}$ | $2.887\times 10^{-2}$ |
| 0.10  | $5.788\times 10^{-2}$ | $5.774\times 10^{-2}$ |

This is the **same** F2/F26 linearisation residual the photon has — a
structural property of the rotation law at $\Delta t = 1$, not a defect.
The bridge is exact at this level: the W-triplet behaves identically
to the photon in the rotation-law sense.

### 3. SU(2) acts cleanly on the bilinear sector

- $G_H$ (singlet) is **exactly** SU(2)-invariant (B1).
- $W^a$ (triplet) **exactly** rotates as the adjoint of $V \in \mathrm{SU}(2)$
  with $R^{ab}(V) = \tfrac{1}{2}\mathrm{tr}(\tau^a V \tau^b V^\dagger)$ (B2).
- The total triplet magnitude $\sum_a \|W^a\|^2$ is **exactly**
  SU(2)-invariant (B3).
- The rotation-law energy conservation survives the SU(2) transform
  on the underlying spinors (B5b).

### 4. F26 dispersion $\Omega(k)$ is preserved under SU(2) on the doublet

A1 confirms that mixing $\nu \leftrightarrow e$ via random
$V \in \mathrm{SU}(2)$ leaves $\Omega(k) = 2\omega_\text{BCC}(k/2)$
unchanged at machine precision. The BCC kinetic step is
block-diagonal in isospin, so $V$ commutes with it by construction
— the test confirms this numerically and exposes no hidden coupling.

### 5. The Paper 1 transpose form is NOT SU(2)-clean

The Extra test shows max-deviation $4.18$ (O(1)) for
$G_T^i = \sum_\alpha (\phi^\alpha)^T \sigma^i \psi^\alpha$
under random $V \in \mathrm{SU}(2)$. This is because $V^T V \ne I$
for $V \in \mathrm{SU}(2)$. Use the Hermitian form when bridging to
the doublet structure; the transpose form remains valid as a U(1)
construction but is not SU(2)-gauge-clean.

---

## What This Adds to the Model

1. **The bridge is verified.** F26's rotation law and F27's chiral SU(2)
   are not just separately consistent — they fit together: the W-triplet
   built on F27's doublet inherits F26's rotation law per component,
   and SU(2) acts adjointly on the triplet without breaking any
   propagation property.

2. **A new bilinear sector is available** for testing the gauge structure
   of the SM analog: $W^a$ rotates with the same $\Omega(k)$ as the
   photon, so propagation tests (e.g. Poynting energy, F17; rotation
   law, F25) port over per-$a$ without re-derivation.

3. **The Hermitian variant is identified as the SU(2)-clean choice**,
   distinct from Paper 1's transpose form. This is a structural finding
   independent of the W-triplet test itself.

---

## Known Limitations

- These are kinematic tests at the bilinear level. They do **not**
  introduce $W_\mu$ as a dynamical gauge boson — the kinetic step is
  still SU(2)-gauge-broken in absence of $W_\mu$, identical to F27's
  known limitation.
- All triplet propagation tests apply the rotation law analytically;
  a full spectral-propagation test (analogous to T51 for the photon)
  on a real-space (E^a, B^a) field would extend this.
- The Weinberg mixing with hypercharge $U(1)_Y$ is not addressed — the
  W^3-photon mixing remains a separate item.

---

## Exactness Inventory Additions

Added to Tier 1 (exact algebraic / machine-precision identities):
- W^a triplet adjoint rotation under SU(2): residual $3.08\times 10^{-16}$
- Triplet magnitude $\sum_a \|W^a\|^2$ SU(2)-invariance: residual $6.66\times 10^{-16}$
- Per-component rotation-law energy conservation: residual $0.0$
- Hermitian singlet SU(2)-invariance: residual $2.24\times 10^{-16}$

---

## Cross-references

- `findings/F26-speed-of-light-as-rotation-rate.md` — the rotation law
  the triplet inherits.
- `findings/F27-complex-mass-chiral-su2.md` — the chiral SU(2) the
  triplet decomposes under.
- `findings/F17-poynting-energy-conservation.md` — the energy conservation
  per W^a component.
- `reference-research/mohr-2010-maxwell-photon-wf-summary.md` §C.2 — the
  longitudinal-photon discussion which informs the per-component structure.
