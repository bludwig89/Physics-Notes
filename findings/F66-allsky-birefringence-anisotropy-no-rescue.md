# F66 — The BCC birefringence anisotropy does NOT rescue a Planck-scale cell: linear vacuum birefringence excludes a≈6.2×10⁻³⁵ m

**Date:** 2026-06-01 - 02:40
**Status:** Confirmed — the anisotropy gives only an O(1) all-sky suppression, ~14 orders short of what the polarization bound requires. The escape hatch (i) of F65 is closed.
**Script:** `model-tests/test_F66_allsky_birefringence_anisotropy.py` (self-contained, numpy only; uses the exact BCC dispersion).
**Cross-references:** [[F65-helicity-chirality-map-confirmed]] (birefringence is physical), [[F30-photon-dispersion-order-anisotropy-birefringence]] (anisotropy), [[F64-em-connection-gravity]] (the cell size a), `si-units-options.md`.

---

## The question

F65 established that the model's linear vacuum birefringence is a genuine physical prediction, and that at the F64 cell size $a\approx6.2\times10^{-35}$ m the body-diagonal effect overshoots the GRB-polarimetry bound by ~14 decades. The one remaining escape (F65 hatch i) was the **anisotropy**: birefringence is exactly zero along the cube axes and on the coordinate planes, maximal along body diagonals. Could a fixed lattice orientation suppress the signal for real (generic-sky-position) sources by the ~$10^{14}$ needed? F66 answers no.

## The directional law [verified, rel err 9.7×10⁻⁴ at k=10⁻³]

To leading order in small $k$ the chiral splitting is

$$\Delta\Omega(k,\hat n)=\Omega^+-\Omega^-=-\frac{k^2}{3}\,n_x n_y n_z,$$

reproducing the F30 body-diagonal coefficient $-\sqrt3/27$ at $\hat n=(1,1,1)/\sqrt3$ and giving **exactly zero on any coordinate plane** (any $n_i=0$), in particular on cube axes *and* face diagonals. The whole directional dependence is the single factor $n_x n_y n_z$.

## Mapping to the standard dim-5 parameter

In Myers–Pospelov form $v_\pm=c(1\pm\eta E/E_\text{Pl})$,

$$\eta(\hat n)=\frac{a/\ell_P}{2\sqrt3}\,|n_x n_y n_z|,\qquad \eta_\text{max}=\frac{a/\ell_P}{18}=0.212\ \ (\text{body diagonal, }a=3.81\,\ell_P).$$

The observational bound from energy-resolved GRB polarimetry is $\eta\lesssim10^{-15}$–$10^{-16}$ (Laurent 2011 / Toma 2012 / Kislat; high-$z$ optical polarimetry for the anisotropic SME $d{=}5$ coefficients).

## All-sky result [4×10⁶ Monte-Carlo directions]

- **Typical suppression is O(1), not $10^{-14}$.** The suppression factor $f=3\sqrt3\,|n_xn_yn_z|\in[0,1]$ has sky **median $f=0.37$** (10th/90th percentiles 0.048 / 0.85). A typical source sees $\eta\sim8\times10^{-2}$ — i.e. an overshoot of the bound by $\sim8\times10^{13}$.
- **Protected sky fraction is ~$10^{-14}$–$10^{-13}$.** The fraction of the sky with $\eta<10^{-15}$ is $\approx6\times10^{-14}$ (near-coordinate-plane analytic) / $\approx1\times10^{-13}$ (MC power-law extrapolation, $P(f<\tau)\propto\tau^{0.93}$). Only a $\sim10^{-15}$-rad-thin band around the three coordinate planes evades the bound.
- **Real sources wash out even at generic (suppressed) directions.** Accumulated helicity phase slip $\Delta\phi=|\Delta\Omega|\cdot L/(c\tau)$: GRB 041219A (~200 keV, ~Gpc) gives $\Delta\phi\sim10^{12}$–$10^{14}$ rad; a 100 keV GRB at $z\sim1$, $\sim10^{14}$; even an optical ($\sim$2 eV) high-$z$ source gives $\sim10^{4}$–$10^{5}$. All $\gg1$ → complete depolarization.

## Verdict

The anisotropy provides only an **O(1)** rescue. A single polarized GRB or AGN at a generic sky position (any line of sight not aligned to within $\sim10^{-15}$ rad of a lattice coordinate plane) suffices to exclude $a\approx6.2\times10^{-35}$ m; with $N$ independent polarized sources the joint survival probability is $\sim(10^{-13})^N$. Since many highly polarized high-energy sources are observed across the sky, **the model is falsified at the F64 one-generation cell size** — barring an implausible fine-tuning of the cosmic lattice axes to every observed line of sight (itself an isotropy-violating prediction already constrained by all-sky SME polarimetry).

## What this means for the model (not a dead end)

The chain is now tight and the tension is localized to one assumption, not the framework: (rotation photon F25/F26) + (two-branch Weyl bilinear F29/F39) + (helicity↔chirality forced, F65) + (cell size from the G-match, F64) ⟹ excluded linear birefringence. Live ways forward, in order of how much they preserve:

1. **The physical photon is the chirality-even bilinear, not a generic two-branch superposition.** If the real U(1) photon is built so that both helicities ride $\Omega_\text{even}$ (the F30 "n=2, unobservable" channel), birefringence vanishes. This contradicts the F65 test *as the photon is currently constructed* (generic linear polarization populates both branches), so it requires a principled projection in `ca_maxwell.py` — and must be reconciled with the composite-vs-U(1) photon non-unification flagged in F39 §5.1. This is the most likely escape and the highest-value next investigation.
2. **The cell is much larger than the G-match value** (the linear birefringence $\eta\propto a$, so $\eta<10^{-15}$ needs $a\lesssim10^{-14}\ell_P$ — far below Planck, which the lattice cannot be). This direction is essentially closed: making $a$ smaller than $\ell_P$ is not available, and larger $a$ worsens it.
3. **Genuinely falsified, and the rotation-photon construction (F26) needs revision** so that the EM field is not the two-branch Weyl bilinear.

The cleanest decisive test is therefore now option 1: determine whether the model's *gauge* photon (the one minimally coupled in `ca_dirac`) is forced to the even combination, independent of the composite bilinear.

## Files
- Test: `model-tests/test_F66_allsky_birefringence_anisotropy.py`
- Uses `ca_bcc` dispersion; builds on F65 / F30 / F64.
