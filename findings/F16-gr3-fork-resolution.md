# Finding 16 — GR-3 factor-2 redshift is resolvable by all three Finding 14.5 forks; GR-4 (Mercury) is the discriminator

*Recorded 2026-05-21 - 15:08. Harness: `ca-simulation/forks/gr3_fork_harness.py`. Raw output: `test-results/gr3_fork_comparison.{json,md}`.*

## Background

Finding 14.5 established that the Paper 6 isotropic-$c$ ansatz
$c(x) = c_0/(1 - 2\phi/c_0^2)$ over-predicts the Pound–Rebka
gravitational redshift by **exactly a factor of 2**: the lattice gives
$\Delta\nu/\nu = 2\,\Delta\phi/c^2$ where measured GR requires
$\Delta\nu/\nu = \Delta\phi/c^2$. The same single scalar that delivers
the correct factor-4 light deflection (GR-1) and correct Shapiro delay
(GR-2) cannot also give the factor-1 redshift, because it perturbs
$g_{00}$ and $g_{ii}$ together. Three candidate resolutions were proposed:

- **Fork A — separate phase-tick field.** Keep Paper-6 $c(x)$ for spatial
  propagation; route redshift through an independent clock field
  $\tau(x) = 1 + \phi/c_0^2$ that does not feed the propagator. (Bimetric-style.)
- **Fork B — anisotropic metric.** Abandon the single-$c$ ansatz; carry
  $g_{00} = -(1+2\phi/c_0^2)$ and $g_{ii} = (1-2\phi/c_0^2)$ separately, with
  $c_\gamma = c_0\sqrt{|g_{00}|/g_{ii}}$ and $\tau = \sqrt{|g_{00}|}$. (Isotropic-Schwarzschild by construction.)
- **Fork C — restricted-$c$ propagator.** One potential, two coupling
  exponents: photons see $2\phi$ (full Paper-6), matter sees $\phi$
  (halved), so $\tau = c_\text{matter}/c_0 = 1 + \phi/c^2$. (Scalar-tensor / Brans–Dicke style.)

## Method

The harness builds one shared open-BC Newtonian potential
($L=128$, $M=1$, $\sigma=3$, $G_N=5\times10^{-4}$, $c_0=0.5$;
$\phi\in[-1.32\times10^{-4}, -4.51\times10^{-6}]$) and runs the same four
GR observables on each fork:

- **GR-1** eikonal deflection coefficient $K = \Delta\theta\, b\, c_0^2/(GM)$.
- **GR-2** Shapiro excess ratio $\Delta t_\text{lat}/\Delta t_\text{GR}$.
- **GR-3** Pound–Rebka ratio$_{GR} = (\Delta\nu/\nu)_\text{lat} / (\Delta\phi/c_0^2)$, averaged over (near,far) pairs $\{(6,16),(8,22),(10,28),(12,30)\}$.
- **GR-4** 1PN Mercury perihelion advance via velocity-Verlet ($GM=0.003$, $a=1$, $e=0.3$, 6 orbits), reported as $\Delta\omega_\text{lat}/\Delta\omega_\text{GR}$, with the linearised metric couplings $(\alpha_A,\alpha_B)$ extracted from each fork's `metric()`.

## Results

| Fork | GR-1 $K$ | GR-2 ratio | GR-3 ratio$_{GR}$ (mean ± std) | GR-4 $\Delta\omega_\text{lat}/\Delta\omega_\text{GR}$ | GR-4 $\Delta\omega_\text{pred}/\Delta\omega_\text{GR}$ | $\alpha_A$ | $\alpha_B$ |
|---|---|---|---|---|---|---|---|
| baseline_paper6 | −3.8495 | 1.0016 | 1.9991 ± 2.3e-4 | 2.0033 | 1.0000 | 1.000 | 1.000 |
| fork_A_phase_tick | −3.8495 | 1.0016 | 1.0001 ± 2.3e-5 | 2.0033 | 1.0000 | 1.000 | 1.000 |
| fork_B_anisotropic | −3.8511 | 1.0018 | 1.0002 ± 6.3e-5 | 2.0033 | 1.0000 | 1.000 | 1.000 |
| fork_C_restricted_c | −3.8495 | 1.0016 | 0.9998 ± 5.7e-5 | 1.0006 | 0.5833 | 0.500 | 0.500 |

## What this shows

1. **All three forks resolve GR-3.** The Pound–Rebka ratio drops from the
   baseline factor-2 (1.9991) to ≈1 in every candidate (A: 1.0001,
   B: 1.0002, C: 0.9998). Decoupling the clock readout from the spatial
   propagator — by *any* of the three mechanisms — removes the factor 2.
   The factor-2 problem is therefore a feature of the *single-scalar
   coupling*, not an unavoidable lattice limitation.

2. **GR-1 and GR-2 survive untouched.** $|K|\approx3.85$ and the Shapiro
   ratio $\approx1.002$ are identical across all four columns, because the
   photon line integral depends only on $c_\gamma$, which all forks keep at
   the Paper-6 form. (Fork B's $c_\gamma = c_0\sqrt{A/B}$ differs from the
   others only at second order in $\phi$, the source of the tiny
   $|K|=3.8511$ vs $3.8495$ shift.) No fix costs the deflection or Shapiro pass.

3. **GR-4 (Mercury) is the experimental discriminator.** Forks A and B keep
   the full Schwarzschild matter coupling ($\alpha_A=\alpha_B=1$) and are
   observationally degenerate with the baseline ($\Delta\omega/\Delta\omega_\text{GR}=2.0033$).
   **Fork C halves the matter coupling** ($\alpha_A=\alpha_B=0.5$) and
   therefore **predicts half the perihelion advance**: $1.0006$, i.e.
   $C/\text{baseline} = 0.4995 \approx \tfrac12$.

   This is the falsifiable difference. A Mercury-class measurement at
   lattice precision would select restricted-$c$ (Fork C, half advance)
   against phase-tick / anisotropic (Forks A & B, full advance). Since the
   *real* Mercury perihelion advance matches full GR, this result
   **disfavours Fork C** on the physics: a halved advance contradicts the
   observed 43″/century. Forks A and B remain viable.

## Caveat — two GR-4 conventions

- **Absolute scale.** Baseline reads $\Delta\omega_\text{lat}/\Delta\omega_\text{GR}=2.0033$
  rather than $\approx1$ because `gr4_mercury_advance` uses the
  per-half-orbit ×2 integration convention noted in the harness header.
  Only the *relative* column is meaningful: C is exactly half of A/B/baseline.

- **Closed form vs integration for Fork C.** The 1PN closed form
  $\Delta\omega \propto (2\alpha_A + 2\alpha_B - \alpha_A\alpha_B)$ gives, for
  $\alpha_A=\alpha_B=0.5$, a factor $1.75$, hence ratio $1.75/3 = 0.5833$
  (the `pred` column). The velocity-Verlet perihelion-difference measurement
  gives $0.4995$ instead, because that observable tracks the (halved) metric
  *amplitude* and does not pick up the $\alpha_A\alpha_B$ cross term at the
  precision/horizon of a 6-orbit run. Both agree that C is **suppressed
  relative to A/B**; the exact suppression factor (½ vs $1.75/3$) is the open
  numerical detail. *This is a candidate for a follow-up exact check —
  integrate Fork C to more orbits / higher $L$ and confirm whether the
  measured ratio converges toward 0.5833.*

## Status against the theory's bar

Per the project standard (a theory must reproduce existing measurements and
either explain them better or extend them): GR-3 alone does not select a
fork, since A, B, C all reproduce the redshift. **GR-4 selects against C**
(it would mis-predict Mercury) and leaves **Forks A and B as the surviving
candidates** — both reproduce GR-1, GR-2, GR-3, and GR-4 simultaneously.
Distinguishing A from B requires an observable sensitive to the
*photon-vs-matter metric split* (e.g. a setting where bimetric A and
genuinely-anisotropic B diverge); none of GR-1…GR-4 separates them.

## Cross-references

- Predecessor: Finding 14.5 (GR-3 factor-2 falsification of Paper 6 $c(x)$).
- GR-4 baseline calibration: Finding 14.12 (Mercury 1PN at 1.5%).
- Tracking: `lattice-vs-spacetime-tests.md` GR-3 / GR-4 rows; `ca-reference.md` GR-3 cross-fork entry.
- Code: `ca-simulation/forks/{gr3_fork_harness,gr3_fork_baseline,gr3_fork_A_phase_tick,gr3_fork_B_anisotropic,gr3_fork_C_restricted_c}.py`.
