---
id: CL288
title: A model-internal rho+omega narrow-resonance VMD estimate captures ~10.2% of the data-driven hadronic Delta alpha(M_Z), reusing the model's existing couplings
slug: hadronic-vmd-rho-omega-delta-alpha
tier: supporting
kind: derivation
status: open
domain: [SM, QCD]
exactness: quantitative
findings: [F334, F103, F128, F240]
tests: [F334-hadronic-vmd-estimate]
modules: [casim.engine.interactions.running_alpha_lattice_bound]
constants: []
supersessions: []
reviews: []
rolls_up_to: CL280
falsifier: stated
first_issued: 2026-08-30
last_verified: 2026-08-30
provenance: authored
review_state: authored
confidence: medium
---

# CL288 — A first model-internal handle on the hadronic vacuum-polarization piece

## Statement

Using the model's own KSRF vector-meson output ($g_{\rho\pi\pi}=6.011$, F103/F240, itself built
from F123's externally-anchored $f_\pi$ and F128's adopted $\rho$–$\omega$ degeneracy) and the
model's own quark-charge assignment ($Q_u=2/3,\,Q_d=-1/3$, F41/F42), a narrow-resonance
vector-meson-dominance (VMD) calculation — introducing **no new external input beyond what those
prior findings already carry** — gives $\Delta\alpha_{\rho+\omega}(M_Z^2)=2.820\times10^{-3}$, which
is $10.2\%$ of the data-driven $\Delta\alpha_\text{had}^{(5)}(M_Z^2)=(276.0\pm1.0)\times10^{-4}$
(Davier–Hoecker–Malaescu–Zhang 2020, used only as a comparison anchor). Feeding this into rubric
row B9's electroweak leg (F322 §7) closes $10.2\%$ of the gap between the model's leptonic-only
$\alpha^{-1}(M_Z)$ and the PDG value, moving the $\sin^2\theta_W(M_Z)$ residual from $+0.450\%$ to
$+0.427\%$ — the same $10.2\%$ ratio stated two ways (F334 §4), not two independent results.

## What it extends

Extends the Standard Model's treatment of hadronic vacuum polarization — which is *always* an
external, data-driven input (no local perturbative QFT calculation reaches the needed precision;
even nonperturbative lattice QCD is an active, difficult program for the real theory) — by
deriving a genuine, if small, piece of it from the model's own field content rather than
importing it wholesale. This does not claim to replace the data-driven determination; it is a
zero-free-parameter partial derivation of one piece of an otherwise entirely external quantity.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F334-hadronic-vmd-rho-omega-delta-alpha-estimate.md` | Full derivation (§2), the honest self-check of the universality posit against PDG $\Gamma(\rho\to e^+e^-)$ (§3), and the EW-leg effect (§4) | quantitative |
| `tests/registry/interactions.yaml` id `F334-hadronic-vmd-estimate` | 6/6 checks PASS, 2/2 D9/H2 controls verified red-and-only-there | quantitative |
| `test-results/F334_hadronic_vmd_estimate.json` | Full numeric record | — |
| `findings/F103-p3-dynamical-pion-goldstone.md`, `findings/F240-omega-coupling-from-vector-sector.md` | The $g_{\rho\pi\pi}$ KSRF output and the universality posit this reuses (not re-derived here) | inherited |

## Falsifier

A genuinely nonperturbative computation of the model's own electromagnetic current–current
correlator (a lattice-QCD-style calculation on the model's own quark/gluon dynamics, not
attempted in F334) that returns a $\rho+\omega$-region contribution to $\Delta\alpha_\text{had}(M_Z)$
outside roughly $[1\times10^{-3},\,6\times10^{-3}]$ — the range spanned by this finding's bare
estimate and its own §3 quench correction — would falsify this narrow-resonance VMD estimate as
a reasonable proxy for that piece of the model's own spectral content, and would need the
discrepancy explained rather than absorbed. **This falsifier is checkable in principle, not in
practice today**: the model's own lattice-correlator machinery does not yet compute this
current–current spectral function (F334 §6), so the range above is a named target with no
near-term test, not a check that can be run now.

## Status & history

`status: open`: the evidence is genuinely incomplete by construction — this captures only the
$\rho$ and $\omega$ channels, no $\phi$, no multi-hadron continuum, no heavy-quark continuum, and
the narrow-width approximation is a known underestimate for the physically broad $\rho$ (§3 of
the finding measures this directly, quench $0.828$, rather than asserting a clean result). The
gap is named precisely in F334 §6 rather than left implicit. This card should be revisited if a
future finding extends the VMD chain to $\phi$ or attempts the full lattice-correlator route.

**2026-08-30** — reviewed against F334's attack-and-fix pass (verdict OVERSTATED): statement and
falsifier reworded to drop the "zero imported couplings" overclaim (the KSRF chain reuses F123's
externally-anchored $f_\pi$ and F128's adopted $m_\rho$) and to flag that the falsifier is not yet
practically testable. See `findings/F334-hadronic-vmd-rho-omega-delta-alpha-estimate.md` §
"Reviewed & corrected" for the full attack list and fixes.

## Sources

- `findings/F334-hadronic-vmd-rho-omega-delta-alpha-estimate.md`
- `docs/claims/CL280-running-alpha-leptonic-lattice-bounded-and-two-loop.md` (the card this rolls up to — B9's running-alpha headline result)
- Davier, Hoecker, Malaescu, Zhang, *A new evaluation of the hadronic vacuum polarisation contributions to the muon anomalous magnetic moment and to $\alpha(m_Z^2)$*, Eur. Phys. J. C 80 (2020) 241
