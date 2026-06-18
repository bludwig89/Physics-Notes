# F129 — Block-spin RG for the free paired-photon: c_lat is an exact RG fixed point and the lattice-artifact (LIV) operators are irrelevant ($\lambda_n=b^{-n}$), so a coarse photon simulation reproduces the fine one

**Date:** 2026-06-11
**Status:** Confirmed — 5/5 checks PASS. Part A is **Tier-1 exact** (sympy, symbolic in $b$); T1/T2/K/RS/V are **machine-precision** (FFT/round-off floor). This is the free-photon half of Phase 1 of `docs/roadmaps/roadmap-scale-to-real-space.md`; the gauge + gravity + confinement half is [[F130-blockspin-gauge-gravity]] (`ca_blockspin.py`).
**Script:** `tests/findings/test_F129_blockspin_free_photon.py`
**Results:** `test-results/F129_blockspin_free_photon.json`, `..._summary.md`
**Cross-references:** [[F26-speed-of-light-as-rotation-rate]] (the rotation rule), [[F30-photon-dispersion-order-anisotropy-birefringence]] (the LIV operator $-k^2/162$), [[F105-axial-photon-exactly-dispersionless]] (on-axis exactness), [[F69-paired-spinor-photon]] / [[F107-canonical-a-adopted]] (even law, cell size), [[F130-blockspin-gauge-gravity]] (gauge/gravity/confinement sectors + the shared `ca_blockspin.py` kernel).

---

## 1. Why this finding exists

The scale audit (`roadmap-scale-to-real-space.md` §0): the canonical cell is
$a=6.598\,\ell_P=1.07\times10^{-34}$ m, so a literal real-space fill is ~45 decades
short of a single proton. "Analogous to real space" can therefore only mean a
tractable lattice in which **one coarse cell stands in for $b^d$ physical cells**,
provided the rotation rule's physical content survives the coarse-graining. This
finding proves that survival for the free paired-photon (even-law) sector and
verifies it on the actual propagator: a coarse simulation on $b^d\times$ fewer cells
reproduces the fine simulation to the FFT floor for all resolved (IR) content.

## 2. The block-spin transformation $\mathcal R_b$

Kadanoff block average + space/time rescaling by $b$. For a periodic field on the
fine lattice (spacing 1):

$$(\mathcal R_b f)(X)=b^{-d}\!\!\sum_{r\in[0,b)^d}\! f(bX+r),\qquad a\to ba,\ \ \tau\to b\tau .$$

Two facts make it phase-clean (proved/used below):

1. **Phase-preserving.** The block average is convolution with a real, even box
   kernel; its Fourier multiplier $D_b(k)=\dfrac{\sin(bk/2)}{b\,\sin(k/2)}$ is a
   **real** scalar ($\le1$, $=1$ at $k=0$). A real multiplier modulates amplitude
   only — it cannot touch the phase $e^{-i\Omega t}$, so the dispersion of the
   surviving modes is untouched.
2. **Anti-alias (test K).** $D_b$ has **exact zeros** at the decimation fold points
   $k=2\pi m/b\ (m=1\dots b-1)$ — precisely the modes that would alias onto a
   surviving coarse mode. Verified: $\max|D_b(\text{fold})|=1.7\times10^{-16}$ over
   $b=2\dots5$.

Hence the coarse rule, in coarse units, is the **renormalised dispersion**

$$\boxed{\ \Omega_\text{coarse}(\kappa)=b\,\Omega(\kappa/b)\ }\qquad(\kappa\in\text{coarse BZ}),$$

the $b$ prefactor being the time-rescale (one coarse tick $=b$ fine ticks).

## 3. The two RG theorems

For any analytic $\Omega(\kappa)=\sum_n a_n\kappa^n$, the block map gives (Part A, sympy, exact, symbolic in $b$):

$$[\kappa^n]\,\Omega_\text{coarse}=a_n\,b^{\,1-n}.$$

- **T1 — $c_\text{lat}$ is a fixed point.** $n=1$: coefficient $\to a_1$ (eigenvalue $b^0=1$). The $k\to0$ slope is invariant, so the physical speed $c=(a/\tau)\,a_1$ is unchanged for every $b$. Instantiated on the true even-law body-diagonal series, $a_1=1/\sqrt3$ exactly.
- **T2 — lattice-artifact (LIV) operators are irrelevant.** $n\ge2$: eigenvalue $b^{\,1-n}<1$. In the velocity form $v(\kappa)/c=1+\sum_{m\ge2}g_m\kappa^m$ this is $g_m^{(b)}=b^{-m}g_m$ (eigenvalue $b^{-m}$). The leading even-law operator is the F30 body-diagonal term: $a_3=-\dfrac{1}{162\sqrt3}$ (matches F30's $\delta v_\phi/c=-k^2/162$), eigenvalue $b^{-2}$. The continuum law $\Omega=c_\text{lat}|k|$ is the **attractive IR fixed point**.

**Measured (machine precision):**

| check | result |
|---|---|
| T1 $b\cdot c_\text{coarse}(b)$, $b=1\dots5$, axis & body diag | all $=0.57735026919$ (=$1/\sqrt3$) |
| T2 eigenvalue, $b=2,3,4,5$ (body diag) | $0.2500,\ 0.1111,\ 0.0625,\ 0.0400$ = $b^{-2}$ |
| T2 leading $g_2$ (body diag) | $-6.17284\times10^{-3}$ = $-1/162$ |
| K $\max\lvert D_b(\text{fold})\rvert$ | $1.7\times10^{-16}$ |

## 4. The simulation-level result (RS) — a coarse run *is* the fine run

The theorems are about the dispersion; the payoff is about runs. On an actual
$(\mathbf E,\mathbf B)$ photon field we verify the RG **commutes with the
propagator**:

$$\mathcal R_b\circ(\text{evolve}_\text{fine})^{bN}\ =\ (\text{evolve}_\text{coarse})^{N}\circ\mathcal R_b ,$$

where $\text{evolve}_\text{coarse}$ uses $\Omega_\text{coarse}=b\,\Omega(\cdot/b)$ on
the coarse grid. For band-limited fields:

| $b$ | lattice | fine ticks vs coarse ticks | rel. residual |
|---|---|---|---|
| 2 | $24^3\to12^3$ | 16 vs 8 | $5.5\times10^{-15}$ |
| 3 | $24^3\to8^3$ | 24 vs 8 | $1.3\times10^{-14}$ |

The coarse simulation, on $b^3\times$ fewer cells and $b\times$ fewer ticks, is the
fine simulation restricted to resolved modes — to the FFT floor. **V (genuine
evolution):** a planted on-axis mode's measured rotation rate $\Omega/|k|$ is
$0.577350269189631$ (fine) and $0.577350269189626$ (coarse, $b=2$) — $c_\text{lat}$
invariant under $\mathcal R_b$ to $1\times10^{-14}$, not merely as a dispersion slope
but in a real propagation.

## 5. What this licenses, and what it does not

**Licenses.** For the free even-law photon, a coarse lattice is a faithful stand-in:
errors are the irrelevant $O((ka)^2)$ operator, suppressed by $b^{-2}$ per blocking
step. This is the Phase-1 gate for "running at a scale analogous to real space" — the
substitution at the heart of the roadmap is legitimate in this sector.

**Does not (yet).** (i) Only the even (real $\mathbf E,\mathbf B$) channel; the
$W$/Weyl **chiral** per-branch propagators need a block-aware renormalised step
(Phase 4 open item; numpy/scipy chiral caveat applies). (ii) Confinement is a
**relevant** direction ($\lambda_\sigma=b$), handled in F130-C1 — the photon LIV
irrelevance does not carry over to the string tension. (iii) Bound-state spectra
under $\mathcal R_b$ are F131/F132.

## 6. Exact vs numeric

| Result | Tier |
|---|---|
| coefficient eigenvalue $a_n b^{1-n}$; $c_\text{lat}$ invariant; $a_3=-1/(162\sqrt3)$ | Tier 1 exact (sympy, symbolic $b$) |
| T1 $c_\text{lat}=1/\sqrt3$ for $b=1\dots5$ | machine precision ($<10^{-9}$) |
| T2 eigenvalue $=b^{-2}$; $g_2=-1/162$ | machine precision |
| K anti-alias zeros | $1.7\times10^{-16}$ |
| RS coarse-run faithfulness | $5.5\times10^{-15}$–$1.3\times10^{-14}$ |
| V measured $c_\text{lat}$ fine vs coarse | agree to $1\times10^{-14}$ |
