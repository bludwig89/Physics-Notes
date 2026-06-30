# F183 — The black hole under the F178 gravity sector: the canonical object is exact Schwarzschild/Kerr (horizon, GR shadow 3√3 M, Hawking radiation, photon-sphere ringdown), with one genuinely new feature — a lattice-regulated core in place of the point singularity

**Date:** 2026-06-30 - 03:15
**Numbering:** max existing F-number was F182 (`F182-friedmann-pressure-cosmology`, same session); this is **F183** (re-checked per CLAUDE.md).
**Status:** Confirmed — 8/8 checks PASS. Schwarzschild/Kerr closed forms are exact (analytic, matched to a numeric photon-sphere solve and to GR formulae); the lattice-core radius is a quantitative prediction; the F114 contrast is the supersession ledger. This is the strong-field build-out of [[F178-gravity-full-tensor-adoption]] and the replacement for the (now superseded) [[F114-dielectric-black-hole]].
**Module:** `ca-simulation/ca_blackhole.py`
**Script:** `tests/findings/test_F183_blackhole.py` (~1 s; numpy only)
**Results:** `test-results/F183_blackhole.json`
**Cross-references:** [[F178-gravity-full-tensor-adoption]] (the decision), [[F181-covariant-interior-kernel-battery]] (the two-function interior the collapse settles into), [[F114-dielectric-black-hole]] (**superseded** — the horizon-free dielectric BH), [[F164-cosmological-constant-120-orders-and-candidate-cancellations]] (the lattice cutoff `a` that regulates the core), [[F107-canonical-a-adoption-L4-grb-gate]] (the canonical cell). Papers: `Paper-07-Gravity.md` §4 (re-issued), `Paper-08` (the dielectric-BH paper, now reframed). External: Schwarzschild 1916; Kerr 1963; Bardeen 1973 (shadow); Oppenheimer–Snyder 1939 (collapse); Cardoso, Miranda, Berti, Witek, Zanchin 2009 (photon-sphere/QNM correspondence); Berti–Cardoso–Will (tabulated QNMs); EHT 2019/2022 (M87\*, Sgr A\*).

---

## What changed

Under F178 the canonical strong-field law is $G_{\mu\nu}=(8\pi G/c^4)T_{\mu\nu}$, so the exact vacuum black hole is **Schwarzschild** (Kerr with spin) — *with a genuine event horizon*. This replaces the F114 "dielectric black hole" (the horizon-free frozen object of the exponential metric $K=e^{2u}$), which is now understood as an artifact of treating the PPN-order representation as fundamental. This finding computes the canonical object's observables and identifies the one place the BCC lattice substrate still departs from GR.

## Checks (8/8)

| # | Check | Result | Tier |
|---|---|---|---|
| S1 | Schwarzschild closed forms: horizon $2M$, photon sphere $3M$, shadow $b_c=3\sqrt3\,M=5.196M$, ISCO $6M$, $\kappa=1/4M$; numeric photon-sphere/critical-impact solve agrees to $<10^{-3}$ | PASS | exact + numeric |
| S2 | **Hawking sector present**: $T_H=\hbar c^3/(8\pi GMk_B)=6.17\times10^{-8}$ K at $1\,M_\odot$; lifetime $2.10\times10^{67}$ yr; $r_s=2.95$ km; $T\propto M^{-1}$, lifetime $\propto M^3$ | PASS | quantitative |
| Q1 | Eikonal **ringdown** tied to the photon sphere: $\Omega_c=\lambda=1/(3\sqrt3\,M)$ exactly; eikonal real part $(\ell+\tfrac12)\Omega_c$ converges monotonically to the tabulated GR fundamental (error $28.8\%\to3.2\%$ for $\ell=2\to6$); damping $(n+\tfrac12)\lambda=0.0962$ vs tabulated $0.0890$ ($8.2\%$) | PASS | quantitative |
| K1 | Kerr ($a=0.9M$): horizons $1.436M,\ 0.564M$; equatorial ergosphere $2M$; frame-drag $\Omega_H=0.313/M$; ISCO prograde $2.32M<6M<$ retrograde $8.72M$; $a\to0$ reduces to Schwarzschild | PASS | exact |
| K2 | Kerr shadow (Bardeen): $a=0.3M$ nearly circular (height $10.39M\approx2\cdot3\sqrt3 M$, asymmetry $0.994$); $a=0.9M$ equatorial displaced & flattened on the prograde side (offset $1.99M$, asymmetry $0.928$) | PASS | quantitative |
| C1 | Oppenheimer–Snyder collapse: a dust ball ($R_0=10M$) **forms a horizon** and reaches $R=0$ in **finite proper time** $\tau=\pi\sqrt{R_0^3/8M}=35.12M$; horizon crossing ($33.70M$) precedes the singularity | PASS | exact |
| L1 | **Lattice-regulated core (new, non-GR)**: the Kretschmann curvature $K=48M^2/r^6$ reaches the BCC cell scale $1/a^4$ at $r_{\rm core}=(48(GM/c^2)^2a^4)^{1/6}=4.9\times10^{-22}$ m for $1\,M_\odot$, with $a<r_{\rm core}\ll r_h$ and $r_{\rm core}\propto M^{1/3}$ | PASS | quantitative |
| X1 | F114 contrast: horizon **appears** ($2M$, was none); shadow exactly $3\sqrt3\,M$ ($0\%$ vs GR, was $+4.63\%$); Hawking **present** (was absent) | PASS | ledger |

**Overall 8/8 PASS.**

## The new characteristics (relative to F114)

| feature | F114 dielectric BH (superseded) | F183 canonical BH (Schwarzschild/Kerr) |
|---|---|---|
| event horizon | none (horizon-free frozen object) | **present**, $r_h=2M$ (Kerr $M+\sqrt{M^2-a^2}$) |
| photon sphere | $2\sqrt e\,M=3.297M$ | $3M$ |
| shadow $b_c$ | $2e\,M=5.437M$ ($+4.63\%$ vs GR) | $3\sqrt3\,M=5.196M$ (**GR-exact**) |
| deep redshift | finite ($1+z=e$ at the throat) | infinite at the horizon |
| Hawking radiation | absent (no horizon) | **present**, $T_H\propto M^{-1}$ |
| ringdown | GW echoes (horizonless) | **QNM** set by the photon sphere ($\Omega_c,\lambda$) |
| rotation | — | full Kerr: ergosphere, frame-drag $\Omega_H$, spin-dependent shadow |
| singularity | wormhole-like throat (no trapped surface) | **lattice-regulated core** at $r_{\rm core}\sim(r_g^2a^4)^{1/6}$ |
| information | trivially unitary (nothing sealed) | horizon present; unitarity preserved by the exactly-unitary substrate via the lattice core / microstates |

The net trade is the same as F178's: the model surrenders the dielectric's distinctive strong-field phenomenology (horizon-free shadow, no Hawking, echoes) and adopts the full GR black hole — which is what every current observation (EHT shadow consistent with $3\sqrt3$, LIGO/Virgo ringdown consistent with Kerr QNMs, no echoes detected at significance) actually supports. The EHT $+4.63\%$ enlargement that F114 offered as an ngEHT target is **withdrawn**: the model now predicts the GR shadow.

## The one genuinely new feature: a lattice-regulated core

The only place the canonical BH departs from textbook GR is at the center. GR's $r=0$ curvature singularity ($K=48M^2/r^6\to\infty$) cannot be reached on the BCC lattice: curvature saturates when it meets the cell scale $1/a^4$, at
$$r_{\rm core}=\big(48\,(GM/c^2)^2\,a^4\big)^{1/6}\propto M^{1/3}.$$
For a solar-mass hole this is $\sim5\times10^{-22}$ m — far inside the $3$ km horizon but $\sim10^{12}$ cells across, so it is a genuine extended core, not a single cell. This is the model's substrate-level **singularity resolution**: the black hole has a horizon and rings down exactly like Kerr, but its interior terminates in a finite-curvature Planck-scale core consistent with the exactly-unitary cellular automaton (no true information-destroying singularity). This is the natural home for the F114 "internal lattice microstates" idea and the model's answer to the information question.

## Open / next

- **Kerr interior / collapse to a spinning core** on the two-function (→ off-diagonal $g_{t\phi}$) kernel of F181.
- **QNM beyond eikonal:** a direct Regge–Wheeler/Teukolsky solve on the lattice to confirm the GR overtone spectrum (and bound any lattice-core-induced echo amplitude — the model predicts it is exponentially small, not absent in principle).
- **Core microstate counting** → the area–entropy law $S=A/4$ from lattice degrees of freedom (the F114 thermodynamic debt, now with a horizon to anchor it).
- **EHT/ngEHT:** quote the GR shadow (withdraw the F114 $+4.63\%$) and the Kerr spin-shadow relation as the model's prediction.

## Files
- Module: `ca-simulation/ca_blackhole.py`
- Test: `tests/findings/test_F183_blackhole.py`
- Results: `test-results/F183_blackhole.json`
- Scenario catalog: `docs/roadmaps/gravity-sector-scenarios-2026-06-30.md`
