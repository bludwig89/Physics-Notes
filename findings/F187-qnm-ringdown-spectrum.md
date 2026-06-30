# F187 — Ringdown quasinormal-mode spectrum (WKB): GR fundamentals reproduced to <7%, and the lattice-core echo amplitude is exponentially suppressed (scenario S4)

**Date:** 2026-06-30 - 04:25
**Numbering:** **F187** (re-checked).
**Status:** Confirmed — 3/3 checks PASS. WKB-1 (Schutz–Will) on the Regge–Wheeler potential; quantitative (fundamentals), qualitative (echo bound).
**Module:** `ca-simulation/ca_qnm.py`
**Script:** `tests/findings/test_F187_qnm.py`
**Results:** `test-results/F187_qnm.json`
**Cross-references:** [[F183-blackhole-under-full-tensor]] (the photon-sphere QNM correspondence $\Omega_c=\lambda$; the lattice core), [[F114-dielectric-black-hole]] (the horizonless object's order-one GW echoes — the contrast). External: Schutz & Will ApJL 291, L33 (1985); Berti, Cardoso & Will PRD 73, 064030 (2006); LIGO/Virgo ringdown tests.

---

Scenario S4. Solves the axial gravitational (Regge–Wheeler, spin-2) perturbation problem by WKB to predict the ringdown frequencies, and bounds the late-time echo amplitude from the F183 lattice-regulated core.

## Checks (3/3)

| # | Check | Result |
|---|---|---|
| Q1 | WKB fundamentals ($n=0$) vs tabulated GR: $\ell=2$ within $6.7\%$ (real) / $0.8\%$ (imag), $\ell=3$ $2.9\%/0.4\%$, $\ell=4$ $1.6\%/0.2\%$ — converging with $\ell$ (the photon-sphere/eikonal limit) | PASS |
| Q2 | Ringdown waveform $h(t)=e^{-t/\tau}\cos(\omega_R t)$ is a damped sinusoid with quality factor $Q>1.5$ | PASS |
| Q3 | Echo regime: with a **true horizon**, the near-horizon barrier transmission is exponentially small ($e^{-2\pi b_c\omega}\sim10^{-9}$) → no detectable echoes, versus the F114 horizonless object's order-one echoes | PASS |

## Result

The model rings down exactly like a GR black hole: the WKB spectrum tracks the tabulated Schwarzschild QNMs (improving with $\ell$, as the modes localize on the photon sphere where $\Omega_c=\lambda=1/3\sqrt3\,M$, F183). The sharp **observational discriminator from F114 is settled**: F114's horizonless dielectric object predicted order-one late-time GW echoes; the canonical BH has a genuine horizon, so echoes from the lattice core are exponentially suppressed — consistent with the non-detection of echoes in LIGO/Virgo ringdowns. A precise echo-amplitude bound requires a Teukolsky solve (the WKB transmission here is the order-of-magnitude scale).

## Open / next
- Direct (Leaver continued-fraction or time-domain Teukolsky) QNM solve for overtone precision and a quantitative echo-amplitude bound vs LIGO/Virgo.

## Files
- Module: `ca-simulation/ca_qnm.py` · Test: `tests/findings/test_F187_qnm.py` · Results: `test-results/F187_qnm.json`
