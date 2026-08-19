# F85 — P0: the electron and the up/down quarks certified as dynamical, real-time wavepackets

**Date:** 2026-06-03 - 00:35
**Status:** Confirmed — 16/16 PASS. This is an **integration / certification** finding: it does not introduce a new algebraic identity, it certifies that the existing first-generation machinery (`ca_dirac_bcc`, `ca_bcc`, `ca_strong`, `ca_charged_current`) behaves as a *measured, non-dispersing, correctly-charged real-time wavepacket* for each of e, u, d — the P0 foundation of `docs/roadmaps/roadmap-matter-binding.md`.
**Module:** none new. **Test:** `tests/findings/test_P0_dynamical_fermions.py` (~8 s).
**Results:** `test-results/P0_dynamical_fermions.json`.
**Cross-references:** [[F46-pythagorean-lattice-mass]] (rest rotation $\Omega_\text{rest}=\arcsin m$ → zitter $2\arcsin m$), F43 (SU(3) colour sector), F38/FG-1 (charge content), F83 (the physical $m_\text{lat}$ are ~$10^{-22}$; P0 uses representative O(0.05–0.4) test masses), `docs/roadmaps/roadmap-matter-binding.md` P0.
**Test record:** record `P0-dynamical-fermions` (tier battery) — `tests/registry/`, D9.

---

## What was certified

Representative dimensionless lattice masses (test values, not physical — that is a P6/scale concern): $m_e=0.05$, $m_u=0.10$, $m_d=0.40$ (the $d{:}u\approx4$ ratio honours the F40 splitting).

| Part | Check | e | u | d | Tier |
|------|-------|---|---|---|------|
| **A1** | Exact dispersion $\omega(k)$: eigenphase of $D_k$ vs analytic $\arccos$ | $3.3\times10^{-16}$ | $2.2\times10^{-16}$ | $2.2\times10^{-16}$ | machine |
| **A2** | Group velocity of a real-time Weyl packet $=c_\text{lat}=1/\sqrt3$ (transverse-uniform packet, exact-linear on-axis dispersion) | rel $1.1\times10^{-4}$ | — | — | quant |
| **B** | Norm conservation over **1000 ticks** | $2.6\times10^{-13}$ | $2.7\times10^{-13}$ | $2.4\times10^{-13}$ | machine |
| **C** | Zitterbewegung $\omega_Z=2\arcsin(m)$ (k=0 two-level, Hann + parabolic interp) | rel $1.2\times10^{-3}$ | $9.0\times10^{-4}$ | $5.0\times10^{-5}$ | quant |
| **D** | Electric charge $Q=T_3+Y/2$ exact over ℚ | $-1$ | $+2/3$ | $-1/3$ | exact |
| **E1** | Colour charge $Q^a$ conserved under real-time propagation (20 ticks) | — | $1.2\times10^{-13}$ (u,d) | | machine |
| **E2** | Pointwise SU(3) density Casimir $\sum_a J^a_0(x)^2$ invariant under local $V(x)$ | — | $1.3\times10^{-15}$ | | machine |
| **E3** | Quark norm conserved (50 ticks) | — | $1.0\times10^{-14}$ | | machine |

So each first-generation matter field is a genuine real-time object: it propagates at the right speed, never loses norm, oscillates at the right zitterbewegung frequency, carries the exact electric charge, and (for the quarks) carries a colour charge that is conserved in time and rotates correctly under local SU(3).

## Three subtleties the harness had to get right (all signal-processing, not physics)

1. **Group velocity (A2).** A full 3-D Gaussian has transverse $k_y,k_z$ spread; $\partial\omega/\partial k_x$ is genuinely smaller off-axis, so the *packet-averaged* velocity (0.52) sits below the on-axis $1/\sqrt3$ — **real physics, not a bug**. A packet Gaussian in $x$ but uniform in $y,z$ has $k_y=k_z=0$ for every mode, where $\omega=k_x/\sqrt3$ is exactly linear, recovering $c_\text{lat}=1/\sqrt3$ to $10^{-4}$. The k-space helicity projector $P_+(k)=(I+\hat n\!\cdot\!\sigma)/2$ (normalised per-mode) keeps the packet a pure +branch state so no $-$branch leaks backward.
2. **Zitterbewegung (C).** At $k=0$ the $D_k$ off-diagonal $i m$ mixes the chirality eigenstate (not an energy eigenstate) between eigenphases $\pm\arcsin m$, so the L−R population oscillates at the difference $2\arcsin m$. A Hann window + quadratic peak interpolation pulls the frequency to sub-bin accuracy.
3. **Colour covariance (E2).** Under a *local* $V(x)$ the *total* charge is not invariant (only globally); the correct covariance statement is pointwise on the charge **density**, which is invariant cell-by-cell to $10^{-15}$.

## Scope / what P0 is not

P0 certifies single particles. It does **not** yet bind them — that is P1 (3-D confinement) → P2 (dynamical baryon) onward. The representative masses are not physical; absolute MeV awaits P6 (scale fixing, CO-1/F83).
