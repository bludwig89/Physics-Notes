# F189 — Compact-binary inspiral and GW phasing: GW150914 chirp mass 28.1 M⊙, ISCO 67.6 Hz, ~0.19 s in band — standard quadrupole chirp on the F178 sector (scenario S6)

**Date:** 2026-06-30 - 04:35
**Numbering:** **F189** (re-checked).
**Status:** Confirmed — 3/3 checks PASS. Leading-order (0PN/quadrupole) phasing; quantitative.
**Module:** `ca-simulation/ca_inspiral.py`
**Script:** `tests/findings/test_F189_inspiral.py`
**Results:** `test-results/F189_inspiral.json`
**Cross-references:** [[F180-gw-speed]] (graviton speed $c_{\rm grav}=c_{\rm lat}=c_{\rm photon}$, the propagation half of the GW sector), [[F183-blackhole-under-full-tensor]] (the ISCO and the post-merger ringdown F187), [[F178-gravity-full-tensor-adoption]]. External: GW150914 (Abbott et al. 2016): $\mathcal M_c\approx28.6\,M_\odot$, ~0.2 s from 35 Hz to merger.

---

Scenario S6. The two-body GW sector. With the graviton speed already fixed (F180), this builds the quadrupole inspiral: the chirp-mass-driven frequency sweep $df/dt=\tfrac{96}{5}\pi^{8/3}\mathcal M_c^{5/3}f^{11/3}$, the time to merger, and the GW150914-like waveform.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| I1 | GW150914 ($m_1=36,\ m_2=29\,M_\odot$): chirp mass $\mathcal M_c=28.1\,M_\odot$, ISCO GW frequency $67.6$ Hz, time from 35 Hz to merger $0.19$ s — matching the observed event | PASS |
| I2 | Chirp scaling: $df/dt\propto f^{11/3}$ (doubling $f$ multiplies the rate by $2^{11/3}$) to machine precision | PASS |
| I3 | Chirp-mass formula: equal masses give $\mathcal M_c=m/2^{1/5}$ exactly | PASS |

## Result

The inspiral is standard GR: the recovered chirp mass ($28.1\,M_\odot$), ISCO frequency ($\sim68$ Hz), and in-band duration ($\sim0.19$ s) reproduce GW150914. Together with F180 (propagation at $c_{\rm lat}$) and F187 (the ringdown), the model now spans the full inspiral–merger–ringdown picture with GR-consistent predictions, the merger frequency anchored to the F183 ISCO.

## Open / next
- Higher-PN phasing (1PN–3.5PN) and spin terms for parameter-estimation-level waveforms.
- Stitch inspiral (F189) → merger/ISCO (F183) → ringdown (F187) into one waveform.

## Files
- Module: `ca-simulation/ca_inspiral.py` · Test: `tests/findings/test_F189_inspiral.py` · Results: `test-results/F189_inspiral.json`
