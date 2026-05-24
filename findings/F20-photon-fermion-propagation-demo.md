# Finding 20 — Photon and fermions demonstrably propagate across the BCC lattice

*Recorded 2026-05-22 - 13:42. Run: `model-tests/run_propagation_demo.py`. Result: `test-results/propagation_demo_2026-05-22.json`. Figure: `test-results/figures/propagation_demo.png`.*

## Question

Can a photon *exist naturally and move across* the lattice, and do the basic
fermions propagate as localized excitations? Prior evidence was momentum-space
(dispersion, transversality, energy gates). This finding adds the missing
**real-space** demonstration: launch wavepackets and watch them traverse an
$L^3$ lattice, measuring group velocity from the energy-density centroid.

## Method

Three packets on a $64^3$ BCC lattice, each seeded as a Gaussian envelope
(compact along $\hat x$, wide transverse: $\sigma=(6,10,10)$) times a plane wave
at mean momentum $k_0 = 0.8\,\hat x$, propagated 44 CA ticks. Centroid
$\bar x(t)=\sum_x x\,\rho(x)/\sum_x \rho(x)$ tracked every 2 ticks; group velocity
is the least-squares slope $d\bar x/dt$.

1. **Massless Weyl fermion** — `ca_bcc.weyl_step_3d_bcc`, seeded with the $+$-helicity eigenspinor of $U(k_0)$.
2. **Massive Dirac fermion** ($m=0.3$) — `ca_dirac_bcc.dirac_step_3d_bcc_splitstep`, seeded with the **positive-energy 4-spinor eigenmode** of $D_k$ (an $\eta$-only seed mixes $\pm$energy modes → zitterbewegung smears $v_g$; the eigenmode seed removes it).
3. **Composite photon** — two correlated Weyl fields $\psi,\varphi$, each a packet at $k_0/2$, propagated independently; tracked via the pointwise bilinear energy density $\sum_i |G^i(x)|^2$, $G^i=\varphi^T\sigma^i\psi$.

## Results

| Packet | measured $v_g$ (cells/tick) | predicted | rel. err | cells traversed |
|---|---|---|---|---|
| Weyl fermion | 0.5752 | $1/\sqrt3 = 0.5774$ | **0.37%** | 25.2 |
| Dirac $m=0.3$ | 0.4667 | $d\omega/dk = 0.4717$ | **1.06%** | 20.5 |
| Composite photon | 0.5530 | $1/\sqrt3 = 0.5774$ | 4.2% | 24.4 |

Momentum-space gates (re-confirmed this run): photon dispersion residual
$2.1\times10^{-3}$; transversality $4.6\times10^{-17}$; Poynting energy drift
(with $c^2$, 200 steps) $4.8\times10^{-14}$. Wall time 7.5 s.

## Interpretation

1. **All three excitations traverse the lattice at the emergent light speed.** The massless Weyl packet and the composite photon both move at $\approx 1/\sqrt3 = c_\text{lat}$; the massive Dirac packet correctly moves *subluminally* at $0.81\,c_\text{lat}$, matching its analytic group velocity $d\omega/dk$ to 1%.

2. **The photon "exists and moves" end-to-end.** It is a composite (bilinear of two Weyl fields), it propagates as a localized energy packet, it is transverse to machine precision, and it conserves Poynting energy during the motion. This is the real-space companion to the momentum-space gates of [[finding-17-poynting-energy-conservation]] and [[F18-mohr-c5-c6-build]].

3. **The photon's 4.2% velocity deficit is a finite-packet artifact, not physics.** The pointwise bilinear narrows the real-space packet (product of two Gaussians → width $\sigma/\sqrt2$), broadening its transverse-$k$ content; off-axis BCC modes have $\partial\omega/\partial k_x < 1/\sqrt3$. Widening the transverse envelope from $\sigma_\perp=6\to10$ moved the deficit $6.2\%\to4.2\%$ — the predicted direction, confirming the diagnosis. Along a coordinate axis the BCC Weyl dispersion is *exactly* linear ($\omega=k_x/\sqrt3$), so the on-axis group velocity has no curvature; the residual is entirely from the transverse tails.

## Caveats

- The photon velocity is a demonstration-grade number (few-percent), limited by packet width vs lattice size, not a precision gate. The precision claims for the photon remain the momentum-space gates (transversality, dispersion, Poynting), which are at machine precision.
- The Dirac seed requires the positive-energy 4-spinor eigenmode; the naive $\eta$-only seed gives an 8.4% velocity error from zitterbewegung — recorded here to save the next person the bug hunt.

## Cross-references

- Real-space companion to [[finding-17-poynting-energy-conservation]], [[F18-mohr-c5-c6-build]].
- Fermion substrate: `ca_bcc.py` (Weyl), `ca_dirac_bcc.py` (Dirac); composite photon: `ca_maxwell.py`.
- Curl-equation follow-up: [[F21-curl-residual-geometry-independence]].
