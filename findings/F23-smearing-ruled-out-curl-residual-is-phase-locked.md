# Finding 23 — Smearing is ruled out; the c_lat/√2 curl coefficient is algebraically phase-locked

*Recorded 2026-05-23 - (session). Run: `ca-simulation/forks/smearing_fork_harness.py`. Result: `test-results/smearing_fork_results_2026-05-23.json`.*

---

## Question

Finding 21 established that the composite-photon curl residual curl/|k| = c_lat/√2 is
geometry-independent. The paper (Bisio et al. 2015 "Paper 1") mentions a smearing function
f_k(q) in the context of bosonic statistics. **Hypothesis 1 (Finding 2):** implementing the
Paper 1 smearing function might drive the O(k) curl residual toward 0, achieving O(k³) closure.

## Method

Three classes of smearing: (a) Fixed-width isotropic Gaussian, σ ∈ {0.005, 0.01, 0.02, 0.05, 0.1};
(b) k-proportional Gaussian, σ = α|k|/2 with α ∈ {0.25, 0.5, 1.0, 2.0};
(c) 8-point BCC nearest-neighbour shell, displacement δ ∈ {0.01, 0.05, 0.1}.

Eigenmode convention matched to the Finding 21 baseline (φ = psi_minus at k/2−q,
ψ = psi_plus at k/2+q, both evolved as e^{−iωΔt}). Self-check: σ=0 reproduces c_lat/√2
(rel err 4.6×10⁻⁵). k-scan over [10⁻³, 10⁻¹]; log-log slope and leading coefficient
curl_E/|k| at k→0 measured per variant.

## Results

| variant | mode | slope_E | coeff/|k| (k→0) | vs baseline |
|---|---|---|---|---|
| σ = 0 (baseline) | fixed | 1.001 | 0.40827 | 1.000× |
| σ = 0.005 | fixed | 0.506 | 5.67 | 13.9× |
| σ = 0.010 | fixed | 0.280 | 13.2 | 32.3× |
| σ = 0.020 | fixed | 0.071 | 25.6 | 62.8× |
| σ = 0.050 | fixed | −0.158 | 61.4 | 150× |
| σ = 0.100 | fixed | −0.133 | 98.3 | 241× |
| α = 0.25 | k-prop | 0.999 | 0.416 | 1.019× |
| α = 0.50 | k-prop | 1.000 | 0.414 | 1.014× |
| α = 1.00 | k-prop | 1.004 | 0.422 | 1.034× |
| α = 2.00 | k-prop | 1.005 | 0.494 | 1.211× |
| BCC-shell δ=0.010 | bcc_shell | 1.007 | 0.402 | **0.984×** |
| BCC-shell δ=0.050 | bcc_shell | 0.433 | 6.31 | 15.5× |
| BCC-shell δ=0.100 | bcc_shell | 0.055 | 23.7 | 58.0× |

- **Fixed-width Gaussian**: makes the residual dramatically worse. A fixed σ is large relative to |k| at small k, causing severe momentum mixing.
- **k-proportional Gaussian** (σ ∝ |k|): slope stays exactly 1.000; coefficient barely changes (1.01–1.21×). No improvement.
- **BCC-shell, δ=0.01**: coefficient 0.984× — a 1.6% improvement, within noise, slope unchanged.

## Analytic diagnosis — the residual is π/2 phase-locked

The smearing result motivates a direct analytic calculation. For k = k ẑ (small k),
the bilinear with φ = psi_minus, ψ = psi_plus at k/2 gives:

$$G_T = (1, i, 0), \quad E_G(0) = 2n_\text{mag}(1,0,0)\ [\text{REAL}], \quad B_G(0) = 2n_\text{mag}(0,1,0)\ [\text{REAL}]$$

At Δt = 1 (one CA tick), G_T → e^{−iΩ} G_T with Ω = 2ω(k/2):

$$\mathbf{E}(1) - \mathbf{E}(0) = 2n_\text{mag}\big(\cos\Omega - 1,\ \sin\Omega,\ 0\big) \approx 2n_\text{mag}\Omega\,(0,1,0) + O(\Omega^2) \quad [\textbf{REAL}]$$

The Paper 1 continuous-time RHS:

$$i(2\mathbf{n}_{k/2})\times\mathbf{B}(0) = i(0,0,2n_\text{mag})\times(0,2n_\text{mag},0) = -4in_\text{mag}^2(1,0,0) \quad [\textbf{IMAGINARY}]$$

At leading order in small k: $\Omega \approx c_\text{lat}|k|$ and $n_\text{mag} \approx c_\text{lat}|k|/2$. So both terms are $O(k^2)$ in magnitude, but they are **π/2 out of phase in complex-vector space** (one real, one imaginary). Their difference has magnitude:

$$|\mathbf{E}(1) - \mathbf{E}(0) - i(2\mathbf{n}_{k/2})\times\mathbf{B}(0)|
\approx \sqrt{(2n_\text{mag}\Omega)^2 + (4n_\text{mag}^2)^2}
\approx \sqrt{2}\,c_\text{lat}^2|k|^2$$

Dividing by denom $\approx 4n_\text{mag} \approx 2c_\text{lat}|k|$:

$$\boxed{\frac{\text{curl residual}}{|k|} = \frac{\sqrt{2}\,c_\text{lat}^2|k|^2}{2c_\text{lat}|k|\cdot|k|} = \frac{c_\text{lat}}{\sqrt{2}}}$$

The coefficient is algebraically exact, confirmed numerically to 5 significant figures across five geometries (Finding 21) and now understood analytically. The 3D average over random directions introduces a factor of $c_\text{lat} = 1/\sqrt{3}$ relative to the single-direction calculation of $1/\sqrt{2}$, giving the measured $c_\text{lat}/\sqrt{2} = 1/\sqrt{6}$ (BCC).

## Why smearing cannot fix this

Gaussian smearing replaces the pointwise bilinear by

$$G_\text{smeared}(k) = \sum_j w_j\,\psi^T(k/2+q_j)\,\sigma\,\phi(k/2-q_j)$$

For each displaced pair (j): (a) $\mathbf{E}_j(1) - \mathbf{E}_j(0)$ is still REAL at leading order (the imaginary phase of $e^{-i\Omega_j}$ flips the imaginary part of $G_T$ into the real E field); (b) $i(2\mathbf{n}_{k/2})\times\mathbf{B}_j$ is still IMAGINARY (central $\mathbf{n}_{k/2}$ is real). The weighted average inherits the same phase structure. No choice of Gaussian width changes the fact that one quantity is real and the other imaginary at leading order.

The π/2 phase lock is a consequence of the **discrete-time bilinear construction**, not of any spatial structure that smearing could average out.

## Root cause

The test compares:
- **dE**: discrete finite difference $\mathbf{E}(t+1) - \mathbf{E}(t)$ (real-valued at leading order)
- **RHS**: continuous-time Maxwell identity $i(2\mathbf{n}_{k/2})\times\mathbf{B}$ (imaginary at leading order)

These agree in the limit Δt → 0 (continuous time), where dE/Δt → ∂_t E becomes complex. At Δt = 1, the leading O(k²) terms are π/2 apart in phase and their difference gives the fixed O(k) residual.

## Verdict on hypotheses (from Finding 2)

| Hypothesis | Status |
|---|---|
| **H1: Smearing function f_k(q)** | ❌ **RULED OUT** — any smearing preserves the phase lock |
| H2: Different bilinear (e.g. both + eigenmodes) | Not yet tested |
| **H3: Discrete-time vs continuous-time (operator ordering)** | ✅ **PRIMARY CANDIDATE** |

## Next fork

Test H3 directly: run the curl test at small Δt (e.g. Δt = 10⁻³) by applying the CA propagator N times with a small fractional phase. The continuous-time limit should make dE/Δt → ∂_t E (imaginary), resolving the phase lock. If curl/|k| → 0 as Δt → 0 at fixed k, the O(k) residual is entirely a finite-Δt artefact and the Paper 1 identity holds exactly in continuous time.

## Cross-references

- [[finding-2-curl-residual]]: original O(k) residual discovery
- [[finding-21-curl-geometry-independence]] (F21): geometry ruled out
- [[curl-residual-geometry-ruled-out]]: memory note
- Exactness Inventory #7: $1/\sqrt{2d} \to c_\text{lat}/\sqrt{2}$ (updated in F21)
