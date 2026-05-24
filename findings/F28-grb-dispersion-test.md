# Finding 28 — F26 photon-dispersion prediction is consistent with all current LIV bounds, but below sensitivity by ~15 decades

**Date:** 2026-05-23 — 16:35
**Status:** Confirmed test result — F26 not excluded by any current photon time-of-flight experiment
**Script:** `model-tests/test_F28_grb_dispersion.py`
**Results:** `test-results/F27_grb_dispersion.json`, `test-results/F27_grb_dispersion_summary.md`

---

## What was tested

F26 predicts a quadratic-in-energy correction to the photon group velocity:

$$\frac{v_g(E)}{c} = 1 - \frac{1}{2}\left(\frac{E}{E_\text{Planck}}\right)^2$$

(assuming the lattice tick equals the Planck time). In the standard LIV
parameterisation $v/c = 1 - s_n(E/E_{\text{QG},n})^n$ this corresponds to:

$$E_{\text{QG},2}^{\,F26} = \sqrt{2}\,E_\text{Planck} \approx 1.73 \times 10^{19}\,\text{GeV}\quad\text{(subluminal, } n=2\text{)}$$

The test confronts this with three of the strongest current time-of-flight
constraints on photon LIV: Fermi-LAT, LHAASO, and MAGIC.

---

## Result

| Experiment | Best 95% CL $E_{\text{QG},2}$ (subluminal) | $\Delta t(F26)$ predicted | Δt sensitivity reached | Verdict |
|---|---|---|---|---|
| Fermi-LAT GRB 090510 | $1.3 \times 10^{11}$ GeV | $3.2 \times 10^{-18}$ s | $5.7 \times 10^{-2}$ s | not excluded, 16.2 dec below |
| LHAASO GRB 221009A | $7.0 \times 10^{11}$ GeV | $6.5 \times 10^{-14}$ s | $4.0 \times 10^{1}$ s | not excluded, 14.8 dec below |
| MAGIC Mrk 501 | $5.7 \times 10^{10}$ GeV | $8.0 \times 10^{-15}$ s | $7.4 \times 10^{2}$ s | not excluded, 17.0 dec below |

**No experiment can currently test F26's prediction.** F26 is consistent with
all three. The strongest constraint (LHAASO GRB 221009A) sits ~15 orders of
magnitude away from the predicted delay.

---

## Photon-energy threshold to make F26 testable

To bring the predicted $\Delta t$ up to the timing sensitivity already achieved
by each experiment requires a photon $\sim 10^7$–$10^8 \times$ more energetic
than the highest-energy photon currently observed from each source:

- GRB 090510 baseline: photon energy $\ge 4$ EeV
- GRB 221009A baseline: photon energy $\ge 320$ EeV
- Mrk 501 baseline: photon energy $\ge 3000$ EeV

These energies are above the GZK cutoff. Cosmological-baseline photons at
those energies would be absorbed on the CMB before reaching us. So under
the Planck-tick assumption, F26 is effectively *unfalsifiable* by photon
time-of-flight measurements with foreseeable technology.

---

## Why this matters

1. **F26 passes the standard QG-phenomenology gate.** It does not predict a
   linear LIV correction (which is already ruled out at $\gtrsim 10 E_\text{Planck}$
   by GRB 090510), only a quadratic one at Planck scale, where current limits
   are $\sim 10^{-8} E_\text{Planck}$.
2. **The lattice-tick assumption is now the testable knob.** If the underlying
   CA tick is not the Planck time but a coarser scale, the equivalent
   $E_{\text{QG},2}$ shifts proportionally. Current bounds put a lower limit
   on the tick rate (upper limit on tick duration):

   $$\tau_\text{lat} \lesssim \frac{1}{E_{\text{QG},2}^\text{limit}} \sim \frac{\hbar}{7 \times 10^{11}\,\text{GeV}} \approx 9 \times 10^{-37}\,\text{s}$$

   The Planck time is $5.4 \times 10^{-44}$ s, so any lattice tick between
   the Planck time and $\sim 10^{-37}$ s is allowed. A tick at $\sim 10^{-37}$ s
   (~$10^7 t_P$, roughly GUT-scale) is exactly at the LHAASO frontier and could
   be ruled out within a decade by the next generation of UHE photon detectors.
3. **Anything stronger than n=2** (e.g., n=1, which F26 forbids) is already
   excluded. F26's structural prediction — *exactly* quadratic at leading
   order, with sign and coefficient fixed — distinguishes it from generic
   linear-LIV quantum-gravity phenomenology. If a linear effect were ever
   observed, F26 would be wrong.

---

## Falsifiability summary

| Observation that would *falsify* F26 | Required experimental sensitivity |
|---|---|
| Linear ($n=1$) photon dispersion at any scale | Already excluded — supports F26 |
| Quadratic ($n=2$) superluminal dispersion | Current LHAASO bound enough |
| Quadratic subluminal at $E_\text{QG} < 7 \times 10^{11}$ GeV | Already excluded — supports F26 |
| Quadratic subluminal at $\sqrt{2}\,E_\text{Planck}$ | Needs ~$10^{20}$ eV photon from $z \sim 1$ |

---

## Cross-references

- [[F26-speed-of-light-as-rotation-rate]]: source of the prediction
- [[F25-real-rotation-exact-discrete-time-maxwell]]: exact rotation underlying the correction
- `model-tests/tests-priority/test_06_QG2_planck_LV.py`: prior BCC Weyl LV bound (linear, different sector)
- Vasileiou et al. 2013, PRD 87, 122001 (arXiv:1305.3463)
- Piran & Ouyang 2024 (arXiv:2308.03031)
- LHAASO Collab. 2024, PRL
- MAGIC Collab. 2008, Phys. Lett. B 668, 253
