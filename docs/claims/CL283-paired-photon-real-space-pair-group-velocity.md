---
id: CL283
title: 'The paired-spinor photon propagates in real space at a closed-form pair group velocity $\partial\Omega_\text{pair}/\partial k_i=\tfrac{c_\text{lat}}2[\hat g^+_i+\hat g^-_i](\mathbf k/2)$ — exactly $c_\text{lat}$ on a cubic axis, and matched by a finite-aperture packet to $7.8\times10^{-16}$'
slug: 'paired-photon-real-space-pair-group-velocity'
tier: supporting
kind: derivation
status: live
domain: [SR, QFT]
exactness: machine
findings: [F314, F69, F105, F20]
tests: [F314-pair-group-velocity-closed-form, F314-photon-packet-propagation]
modules: [casim.engine.gauge.photon_packet]
constants: [c_lat]
supersessions: []
reviews: []
rolls_up_to: CL002
falsifier: stated
first_issued: '2026-08-19'
last_verified: '2026-08-19'
provenance: authored
review_state: authored
confidence: high
---

# CL283 — The paired-spinor photon propagates in real space at its own closed-form pair group velocity

## Statement

The photon the model actually has — the paired-spinor photon of F67/F68/F69, evolved by its own
unmodified even law $\tilde F(\mathbf k)\to e^{-i\Omega_\text{pair}(\mathbf k)}\tilde F(\mathbf k)$
for $F\equiv\mathbf E+i\mathbf B$ — exists as a localised real-space packet, crosses a wrap-free
lattice while conserving its energy, and moves at the velocity its own dispersion predicts. That
velocity is a closed form:

$$\frac{\partial\Omega_\text{pair}}{\partial k_i}(\mathbf k)
=\frac{c_\text{lat}}{2}\Bigl[\hat g^+_i(\mathbf k/2)+\hat g^-_i(\mathbf k/2)\Bigr],
\qquad \hat g^s_i\equiv\frac{g^s_i}{\sqrt{1-(u^s)^2}},$$

with $u^s=c_xc_yc_z+s\,s_xs_ys_z$, $g^s_x=s_xc_yc_z-s\,c_xs_ys_z$ and cyclically, where
$c_i=\cos(k_ic_\text{lat})$ and $s_i=\sin(k_ic_\text{lat})$. The factor $\tfrac12$ is the chain
rule for two constituents each carrying half the total momentum.

On a coordinate axis the transverse cosines are $1$ and the transverse sines are $0$ — both
representable — so $u^\pm(\tfrac{k}{2}\hat x)=\cos(kc_\text{lat}/2)$ holds **bit-for-bit on both
branches**, hence $\Omega_\text{pair}(k\hat x)=k\,c_\text{lat}$ and
$\partial\Omega_\text{pair}/\partial k_x=c_\text{lat}$ at *every* $k$ in the zone, with zero
curvature.

A beam of finite transverse width therefore does **not** travel at $c_\text{lat}$: it travels at
the packet-weighted $\sum_{\mathbf k} w(\mathbf k)\,\partial\Omega_\text{pair}/\partial k_x$ with
$w=\lvert\tilde F\rvert^2/\sum\lvert\tilde F\rvert^2$ taken from the actual discrete seed. The
measured centroid drift is $0.5728449064271057$ against a closed form of $0.5728449064271062$ —
relative residual $7.8\times10^{-16}$ — while sitting $0.780\%$ *below* $c_\text{lat}$, a real
finite-aperture deficit four decades above tolerance.

Being wrap-free is a condition on the **carrier**, not only on the box: the residual backward
spectral weight of a one-sided seed is $\exp(-4k_0^2\sigma_x^2)$ and that tail runs backwards at
$-c_\text{lat}$, reaching the boundary before the packet does. The gate asserts
$k_0\sigma_\text{axis}\ge5$.

## What it extends

**The photon's kinematics in Maxwell theory and QED**, where the group velocity is $c$ exactly,
isotropically, and at every $k$. Here it is $c_\text{lat}$ exactly on the three cubic axes and a
computable function of direction and aperture elsewhere, with no free coefficient — the same
structure CL011 and CL012 assert in momentum space, now carried into real space by a propagating
object.

It also extends this automaton's own source literature. The Gaussian-wavepacket drift
$v=(\nabla_k\omega)(\mathbf k_0)$ is Bisio, D'Ariano, Perinotti and Tosini's result
(`references/qca-papers-1-4-overview.md`, arXiv:1601.04842), and `findings/F20-photon-fermion-propagation-demo.md`
records it for the fermion legs. What is derived here is the closed form for the **pair** rate,
its exact on-axis value, and the carrier condition $k_0\sigma_\text{axis}\gtrsim5$ that
one-sidedness requires on a lattice. `gauge.photon` is used unmodified; the module owns only the
seed, the estimator and the target.

Within the model, this card asserts something no live card did. CL002 asserts what the photon
*is* (a bound pair of two spin-half Weyl quanta) and CL012 that it is exactly non-birefringent —
both settled in momentum space; neither asserts that the object propagates. That assertion was
`docs/claims/CL030-wavepackets-propagate-across-the-bcc-lattice-at-the.md`, which is
`withdrawn`: F20 item (3) made it with the $\sigma$-bilinear composite photon that
`S1-F69-sigma-bilinear-photon` retired on 2026-06-01, and the remediation deferred its
replacement. **This card is the photon half of CL030, re-made on the photon the model has.**

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| record `F314-pair-group-velocity-closed-form` (gate, `expect: {exactness: exact, tol: 0}`) | $u^\pm(\tfrac k2\hat x)=\cos(kc_\text{lat}/2)$ bit-for-bit on both branches at 500 sample points; guarded by `offaxis_control_nonzero`, which requires the same residual along the body diagonal to be $O(1)$ — measured $0.723$ | **exact**, tol $0$ |
| same record | the general closed form against a central difference of `pair_dispersion` at 30 random off-axis $\mathbf k$ on all three axes: $8.0\times10^{-11}$, $3.4\times10^{-11}$, $9.1\times10^{-11}$ (the $h^2$ floor) | machine |
| same record | on-axis $\partial\Omega_\text{pair}/\partial k_x=c_\text{lat}$ at every $k$, zero curvature | machine, $5.6\times10^{-10}$ |
| record `F314-photon-packet-propagation` (gate) → `test-results/F314_photon_packet_propagation.json` | packet drift $=\langle\partial\Omega_\text{pair}/\partial k_x\rangle$ on a wrap-free $128\times48\times48$ box, boundary weight $1.6\times10^{-19}$ | machine, $7.8\times10^{-16}$ vs pre-registered $10^{-12}$ |
| same record | repeated on F20's own box and tick count ($256\times64\times64$, $x_0=60$, 44 ticks): residual $1.2\times10^{-15}$, boundary weight $2.7\times10^{-26}$ | machine |
| same record | energy $\sum(\lvert\mathbf E\rvert^2+\lvert\mathbf B\rvert^2)$ conserved **on the moving packet** — the gate F20 item (3) could not pass, its $\sum_i\lvert G^i\rvert^2$ falling $1.000\to0.628$ over 44 ticks | machine, $3.7\times10^{-15}$ |
| same record | no transient: first-tick drift equals the asymptotic drift, and the whole-window least-squares slope agrees with the tail mean to $0.0$, so the estimator carries no fit-window freedom | machine, $1.6\times10^{-14}$ |
| same record | drift is bit-identical across polarisation axes, $\Omega_\text{pair}$ being a scalar rate | **exact**, $0.0$ |
| same record | perturbation moves both sides together, one parameter at a time: $\sigma_\perp:7\to6$ ($1.8\times10^{-15}$), $m_\text{index}:24\to32$ ($1.2\times10^{-15}$) | machine |
| `findings/F314-paired-photon-real-space-propagation.md` §"Being wrap-free…" | the carrier condition, as a measured six-decade effect: $k_0\sigma_x=3.14\Rightarrow$ residual $1.1\times10^{-6}$; $5.89\Rightarrow7.8\times10^{-16}$. The undersampled run is retained in the artifact as an explicit negative control | machine |
| `tests/findings/test_F314_photon_packet_propagation.py` | 10/10 PASS (battery tier) | — |

The pre-registered $10^{-12}$ is derived, not read off: at the asserted wrap ceiling
$\varepsilon\le10^{-15}$ the arithmetic-centroid bias is $\varepsilon L/v=2.2\times10^{-13}$
relative, and the float64 FFT round-off floor over 24 spectral rotations is the same order. The
residual lands three decades below both.

## Falsifier

**Internal.** The claim dies if a wrap-free packet's measured centroid drift departs from
$\sum_{\mathbf k} w\,\partial\Omega_\text{pair}/\partial k_x$ by more than the pre-registered
$10^{-12}$ under the declared conditions ($k_0\sigma_\text{axis}\ge5$, boundary weight
$\le10^{-15}$). Three thresholds already have teeth rather than being satisfiable by
construction: (i) scoring the same run against $c_\text{lat}$ instead of the closed form fails at
$7.8\times10^{-3}$, so the target is doing work; (ii) the off-axis control requires an $O(1)$
residual along the body diagonal, so the on-axis exactness is not a tautology; (iii) undersampling
the carrier degrades the residual by six decades with nothing else changed.

**External.** The on-axis statement $\partial\Omega_\text{pair}/\partial k_x=c_\text{lat}$ at all
$k$ carries the same vacuum-dispersion and birefringence content as CL011 and CL012 and dies to the
same measurements. The finite-aperture deficit is beam optics, not a vacuum effect, and is **not**
an astrophysical falsifier — a card that offered it as one would be claiming a laboratory aperture
as a property of space.

## Status & history

`live` for the result as stated. Four scope boundaries, each from the finding's own record:

1. **On-axis only, and deliberately non-discriminating.** On a coordinate axis
   $\omega^+=\omega^-$, so $\Omega^\pm_\text{split}=2\omega^\pm(k/2)$ coincide with
   $\Omega_\text{pair}$ exactly and **the retired $\sigma$-bilinear photon would give the same
   drift here.** This run does not discriminate the pair law from a single-branch law; that
   discrimination is off-axis and belongs to CL002/CL012, already settled in momentum space.
   Measured in passing along the body diagonal: pair and single-branch differ in speed at
   $5\times10^{-5}$ ($0.3226312$ vs $0.3226157$ per axis component), while the two branches agree
   with each other to $6.3\times10^{-16}$ — no birefringent time-of-flight along that symmetry
   direction, consistent with F30.
2. **An open question is recorded and not adjudicated.** Seeded as a textbook in-phase transverse
   mode ($\tilde{\mathbf E}\parallel\hat e_1$, $\tilde{\mathbf B}=\hat k\times\tilde{\mathbf E}$,
   Hermitian) rather than as the codebase's quadrature convention, the same law gives net drift
   $1.0\times10^{-8}$ and a packet that separates into counter-propagating halves (rms width
   $\times3.37$), because $\Omega_\text{pair}$ is even in $\mathbf k$. Which $(\mathbf E,\mathbf B)$
   identification is the physical electromagnetic field is the F21/F23/F25/F306 curl question.
   This card asserts the propagation result **for the codebase's one-sided convention** and takes
   no position on that; the diagnostic (`run_inphase_transverse_packet`) is in the artifact.
3. **A partial supersession of F105 that the ledger does not yet carry.** F105's algebra and
   conclusions stand; only its beam-optics number is superseded — its small-angle deficit
   $1/(2(k_0\sigma_\perp)^2)$ is the right order and the right scaling and is wrong by $5.8\%$ *of
   the deficit* ($0.7352\%$ predicted vs $0.7804\%$ exact). `supersessions: []` above reflects
   `docs/theory/supersessions.yaml`, which has no record for it. Writing that record is open work.
4. **A neighbouring defect, reported and not patched.**
   `casim.engine.lattice.wavepacket.weyl_group_velocity` returns $c_\text{lat}\hat n_i$ and its
   docstring states that as a general identity; measured against a central difference at 200 random
   $\mathbf k$ it holds for $i=x$ only ($1.2\times10^{-10}$), failing on $y$ ($0.722$, a sign flip)
   and $z$ ($0.407$). No number in this card or in F20 depends on it — every F20 call site passes
   `axis=0` — but F20's own "closed forms" wording is wrong as written. Open in
   `docs/roadmaps/next-steps.md`.

Authored 2026-08-19 while working §E of the finding-coverage audit
(`tools/audit_finding_coverage.py`), which found F314 named by no claim card. The physics was read
from the finding and the two gate records; nothing in the finding, the module, the test registry or
the supersession ledger was changed in writing this card.

## Sources

- `findings/F314-paired-photon-real-space-propagation.md` — the finding, in full
- `findings/F69-paired-spinor-photon.md` — the pair law $\Omega_\text{pair}=\omega^+(\mathbf k/2)+\omega^-(\mathbf k/2)$
- `findings/F105-axial-photon-exactly-dispersionless.md` — the on-axis identity, here guarded, and the beam-optics number this supersedes
- `findings/F20-photon-fermion-propagation-demo.md` — the DEFERRED item this closes, and the withdrawn claim
- `findings/F306-curl-closes-at-k3-representation-artifact.md` — the analytic-amplitude vs quadrature-pair distinction, in a residual rather than in real space
- `docs/claims/CL002-photon-is-a-bound-weyl-pair.md` — the headline this rolls up to
- `docs/claims/CL030-wavepackets-propagate-across-the-bcc-lattice-at-the.md` — the withdrawn predecessor
- `src/casim/engine/gauge/photon_packet.py`; `test-results/F314_photon_packet_propagation.json`; `tests/findings/test_F314_photon_packet_propagation.py`
- `references/qca-papers-1-4-overview.md` — the prior art for $v=\nabla_k\omega$ on this automaton
