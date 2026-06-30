# F171 — Slow light / EIT does not distinguish the rotation-rate picture from phase velocity: they are isomorphic, and the front always stays luminal

**Date:** 2026-06-29 - 18:40
**Numbering:** initially drafted as F170, but a concurrent session had already taken F170 (`F170-lepton-colour-scale-link`); renumbered to **F171** per the CLAUDE.md concurrent-session caution.
**Status:** Confirmed — 4/4 checks PASS. The central result (the model's real-(E,B)-rotation propagator and the standard complex-phase propagator give the *identical* field) is machine-precision exact (residual ≤4×10⁻¹⁶). Honest verdict: slow light is a **consistency anchor + ontology test, not a numerical discriminator** in the linear regime.
**Track:** 1.b of the "real-world device" programme (Paper XII synthesis, `papers/Paper-12-Unification-Rotation-Currency.md`).
**Module:** `ca-simulation/ca_slowlight.py`
**Script:** `tests/findings/test_F171_slowlight.py` (~3 s, numpy only)
**Results:** `test-results/F171_slowlight.json`
**Cross-references:** [[F26-speed-of-light-as-rotation-rate]] (c_lat = dΩ/d\|k\|, the rotation-rate definition under test), [[F69-paired-spinor-photon]] (Ω_pair = ω⁺(k/2)+ω⁻(k/2)), [[F28-grb-dispersion-test]] (the O(k³) lattice/LIV term, ~15 decades below reach), [[F30-photon-dispersion-order-anisotropy-birefringence]], [[F17-poynting-energy-conservation]] (energy transport = group, not phase). External: Hau–Harris–Dutton–Behroozi Nature **397**, 594 (1999); Wang–Kuzmich–Dogariu Nature **406**, 277 (2000) / PRA **63**, 053806 (2001); Fleischhauer–Imamoglu–Marangos RMP **77**, 633 (2005).

---

## The question

The model's defining claim (F26, CLAUDE.md decision 2) is that the speed of light is **not** the propagation rate of a complex phase through space, but the angular rotation rate of the real (**E**, **B**) vector pair per unit wavenumber, c_lat = dΩ/d\|k\|. Track 1.b asks whether a strongly dispersive medium — electromagnetically induced transparency (EIT) slow light, and gain-assisted anomalous "fast light" — can experimentally **distinguish** the rotation-rate description from the textbook phase-velocity description.

The honest answer, established here: **no, not in the linear regime.** The two descriptions are isomorphic (ℂ ↔ SO(2)) and produce the same real field to machine precision, so they reproduce every measured slow-light and fast-light number identically. The model's distinctive content is (i) interpretational — phase velocity transports nothing, the real-field *front* is the invariant — and (ii) the O(k³) lattice term, which slow light does **not** enhance.

## Construction

`ca_slowlight.py` builds two standard linear susceptibilities and propagates a Gaussian pulse two ways:

- **Standard (phase-velocity) propagator** `propagate_phase`: the complex analytic signal advanced by the frequency-domain transfer H(ω) = exp(−i Re β(ω) L)·exp(−Im β(ω) L), β = n(ω)ω/c. This is textbook Maxwell-in-medium.
- **Model (rotation-rate) propagator** `propagate_rotation`: the physical state is the *real* (E, B) pair, advanced per Fourier mode by a real 2×2 rotation R(Φ), Φ = −Re β(ω) L, with amplitude exp(−Im β L). Built explicitly from the real rotation rather than assuming the equivalence.

Two media: a 3-level Λ **EIT** susceptibility (normal/slow) and a **gain-doublet** susceptibility (Wang mechanism: two Raman gain lines → transparent anomalous dispersion → negative group velocity).

## Checks (4/4)

| # | Check | Result | Tier |
|---|---|---|---|
| S1 | **Normal EIT.** (a) calibrate to the Hau anchor: v_g = **16.99998 m/s** (n_g = 1.76×10⁷, slowdown 1.76×10⁷); (b) propagate at n_g = +311 over a 6 cm cell — the model and phase propagators agree to **3.3×10⁻¹⁶**, and the measured group delay +62.26 ns matches L/v_g = +62.24 ns (rel. err **2×10⁻⁴**) | PASS | machine + quantitative |
| S2 | **Anomalous gain doublet.** Calibrate to the Wang anchor: v_g = **−c/309.9** (negative); the pulse **peak advances** by −62.26 ns (exits before it enters), matching the spectral group delay −62.03 ns; model vs phase agree to **4.1×10⁻¹⁶** | PASS | machine + quantitative |
| S3 | **Front velocity.** n(ω→∞) → 1 in both media (1.0000000 / 1.0000000), so the turn-on **front is luminal (v_front = c) regardless of the sign of v_g** | PASS | machine |
| S4 | **Lattice O(k³) term.** Fractional deviation of Ω_pair(k) from linear ≈ (a·k)² = **1.3×10⁻⁵⁴** at λ = 589 nm with the F107 cell, and it is **set by the vacuum wavenumber, not n_g** — slow light does not enhance it | PASS | order-of-magnitude |

## What this means

**S1 (the core result): the descriptions are the same object.** A complex phase e^{iΦ} and a real SO(2) rotation R(Φ) of the (E, B) pair are isomorphic. The model's "rotation rate" reproduces the standard slowly-varying-envelope result exactly — including the famous 17 m/s slowdown — because it *is* Maxwell-in-medium written in the real-pair basis. This is the necessary consistency anchor: any viable reading of the photon must reduce to Maxwell here, and it does, to machine precision.

**S2 (the ontology test): negative group velocity is reproduced, and the model's reading is the clean one.** Both descriptions give the same pulse advance (peak out before peak in, −62 ns over 6 cm — the Wang effect). In the phase-velocity language one must then *append* the caveat "but v_g is not the signal velocity." In the rotation-rate language the caveat is structural: v_p and v_g are bookkeeping derived from the real-field rotation, and the only thing that actually transports is the (E, B) front. This is an interpretational gain, not a different laboratory number.

**S3 (the invariant): the front never beats c.** Every physical resonant/gain response has χ → 0 at high frequency, so n(∞) → 1 and the Sommerfeld front moves at exactly c in both the slow and the fast medium. This is the model's "phase/group velocity transport nothing" stated as a measurable invariant — and it coincides with standard relativistic optics (Sommerfeld–Brillouin).

**S4 (where a real discriminator would live, and why slow light isn't it): the O(k³) lattice term.** The genuinely model-specific prediction is the cubic deviation of Ω_pair(k) = ω⁺(k/2)+ω⁻(k/2) from the linear rate. At optical wavelengths it is ≈ (a/λ)² ~ 10⁻⁵⁴, and crucially it is fixed by the **vacuum** wavenumber a·k, not by the group index — a slow-light medium steepens dn/dω but leaves a·k untouched, so it provides **no enhancement**. The lattice signal stays ~15 decades below reach (consistent with F28), and slow light does not rescue it.

## Verdict

Track 1.b is a **negative-but-clarifying** result, exactly as anticipated when it was scoped: slow light / EIT confirms that the rotation-rate photon reduces to Maxwell-in-medium (machine-precision consistency, reproducing Hau 17 m/s and Wang −c/310), and sharpens the model's claim that phase velocity is non-transporting (front = c, S3) — but it makes **no distinct laboratory prediction** in this regime. A genuine discriminator must target either (a) the O(k³) lattice term by some route that is *not* suppressed by (a/λ)² (slow light is not such a route), or (b) the strong-field / polarimetry channels (F28/FA01 time-of-flight, FA02 vacuum birefringence) where the model's even, non-birefringent photon departs from strong-field QED.

## Open / next

- **Front-velocity step-function test.** S3 uses n(∞)→1; a direct Sommerfeld precursor simulation (sharp turn-on through the gain doublet) would show the front arriving at c while the smooth peak advances — the sharpest visual of "v_g carries nothing."
- **Stored-light / dark-state mapping.** EIT stores the photon in an atomic coherence (Liu–Dutton–Behroozi–Hau 2001). Whether the model's (E, B) rotation has a clean "frozen rotation" description during storage is a follow-up, not a discriminator.
- This finding does not feed a falsification brief (it confirms a reduction, not a sharp prediction); the device-relevant sharp tests remain FA01/FA02.

## Files
- Module: `ca-simulation/ca_slowlight.py`
- Test: `tests/findings/test_F171_slowlight.py`
- Results: `test-results/F171_slowlight.json`
