# F87 — the U(1) charge-coupling path re-verified end-to-end on the paired photon

**Date:** 2026-06-03 - 02:10
**Status:** Confirmed — 20/20 PASS. **Numbering:** built after the concurrent colour-dielectric finding had already taken F86 → this is **F87**. **Integration / certification** finding: it
introduces no new algebraic identity beyond F68, but it certifies — *dynamically,
on the actual even-law `(E,B)` field* — that electric charge couples to the
**paired-spinor photon** (F69) correctly in both directions: a charge *reads* the
field (Aharonov–Bohm holonomy) and a charge *sources* the field (sourced Maxwell
curl), and the two close into one self-consistent loop.
**Module:** `ca-simulation/ca_charge_coupling.py` (new).
**Test:** `model-tests/test_F87_charge_coupling_paired_photon.py` (~0.5 s).
**Results:** `test-results/F87_charge_coupling_paired_photon.json`.
**Cross-references:** [[higgs-free-su2-key-choice]], [[f41-hypercharge-higgs-free]],
F68 (minimal coupling forces the even photon), F69 (paired-spinor photon),
F67 (even-law vs bilinear), `ca_photon_pair.py`, `ca_maxwell.maxwell_curl_residual`.

---

## Why this was open

When the project adopted the paired-spinor photon and retired the composite
σ-bilinear *as the photon* (F67/F68/F69), the old Standard-Model-style U(1)-gauge
fermion step and its `aharonov_bohm_test` driver were **removed** from
`ca_dirac.py` (the `[REMOVED 2026-05-26]` banners at lines ~389 and ~1021). That
left the charge-coupling path — how charge sources the `(E,B)` field and how a
charged fermion reads it back — unverified against the *new* photon. F87 rebuilds
that path on the even-law field and confronts it end-to-end.

The coupling is the **identity-channel Peierls phase** established by F68:

$$P = e^{\,i q\,A\cdot dl}\,\mathbf I_2 ,$$

a c-number (helicity-blind) phase. Everything below follows from that one object
plus the paired photon's curl generator $C(k)=2\,\mathbf n(k/2)$.

## The two halves, and the loop that joins them

### AB — Aharonov–Bohm holonomy (a charge *reads* the field)

The ordered product of Peierls link phases around a closed lattice loop is the
**discrete Stokes theorem**, exact on the lattice:

$$W(\partial S)=\prod_{\text{links}} e^{\,i q\,A\cdot dl}
   =\exp\!\Big(i q\!\oint_{\partial S}\! A\cdot dl\Big)
   =\exp\!\Big(i q\!\iint_S (\nabla\times A)\cdot d\mathbf S\Big)
   =\exp\!\big(i q\,\Phi_\text{enc}\big).$$

A charged fermion encircling a flux tube picks up $q\,\Phi_\text{enc}$ **even on a
field-free path** — the Aharonov–Bohm effect — and, because $P\propto\mathbf I_2$,
the phase is identical for either Weyl helicity (charge couples, spin does not).

| Check | Statement | Residual | Tier |
|------|-----------|----------|------|
| AB1 | Coulomb-gauge $A$ of the paired-photon $B$ exists: $\nabla\times A=B$, $\nabla\!\cdot\!A=0$ | $1.4\times10^{-17}$ / $1.1\times10^{-17}$ | machine |
| AB2 | holonomy $=q\,\Phi_\text{enc}$ (discrete Stokes) | $1.1\times10^{-16}$ | machine |
| AB2 | path-independence (two enclosing loops) / net-zero loop / no-tube loop | $5.6\times10^{-16}$ / $2.9\times10^{-16}$ / $4.1\times10^{-17}$ | machine |
| AB3 | field-free path: $\lvert B\rvert_\text{path}/\lvert B\rvert_\text{peak}=3.3\times10^{-9}$ while holonomy $=1.000$ | — | quant |
| AB4 | helicity-blind: $\lvert\phi_+-\phi_-\rvert$ and $\lVert[P,U^\pm(k)]\rVert$ | $3.3\times10^{-16}$ / $1.1\times10^{-16}$ | machine |
| AB5 | exact charge linearity $W(q)=q\,W(1)$ over $q\in\{1,2,3\}$ | $0.0$ | exact |

### MX — sourced Maxwell curl (a charge *sources* the field)

The paired photon propagates by the even-law rotation of the real $(\mathbf E,
\mathbf B)$ pair; its Maxwell-curl content is the BCC generator
$C(k)=2\,\mathbf n(k/2)$ (the small-$k$ law already in
`ca_maxwell.maxwell_curl_residual`). For a **real** field the operative curl is
the odd part $C_\text{odd}(k)=\tfrac12[C(k)-C(-k)]$, with $\lvert C_\text{odd}
\rvert\to\lvert k\rvert/\sqrt3$ (luminal, $c_\text{lat}=1/\sqrt3$). Minimal
coupling adds the charge current to Ampère:

$$\dot{\mathbf E}=i\,C\times\mathbf B-\mathbf J,\qquad
  \dot{\mathbf B}=-\,i\,C\times\mathbf E.$$

Because $C\cdot(C\times\mathbf x)\equiv0$, the curl term contributes **nothing**
to $\nabla\!\cdot\!\mathbf E$, so the Gauss constraint $i\,C\cdot\mathbf E=\rho$
is preserved under charge continuity $\partial_t\rho=-\,i\,C\cdot\mathbf J$:
**electric charge is conserved by the coupling**, to machine precision, on the
paired photon's own propagator.

| Check | Statement | Residual | Tier |
|------|-----------|----------|------|
| MX1 | $\lvert C\rvert/\lvert k\rvert\to1/\sqrt3$ (luminal curl rate) | $1.8\times10^{-12}$ | quant |
| MX2 | $C\cdot(C\times B)=0$ (curl sources no charge) | $5.3\times10^{-16}$ | machine |
| MX3 | Gauss residual $i C\!\cdot\!E-\rho$ over 100 sourced ticks (charge conserved) | $2.0\times10^{-12}$ | machine |
| MX4 | $\nabla\!\cdot\!\mathbf B=0$ preserved over 50 ticks | $2.0\times10^{-11}$ | machine |
| MX5 | magnetostatics $i C\times B=J_T$ (resolved sector) | $1.4\times10^{-15}$ | machine |

### E2E — charge → field → A → holonomy on one field

A compact interior $B_z$ flux tube is sourced by its Ampère wall current
$\mathbf J=\nabla\times\mathbf B$; the Coulomb-gauge $A$ solved from that **same**
field gives a holonomy equal to $q\times$ the current-driven interior flux:

| Check | Residual / value | Tier |
|------|------------------|------|
| $\nabla\times A=B$ | $7.8\times10^{-16}$ | machine |
| Ampère $\nabla\times B=J$ | $0.0$ | exact |
| holonomy $-$ flux | $3.6\times10^{-15}$ | machine |
| enclosed flux (non-zero AB signal) | $15.9$ | — |

The single number "interior flux" appears identically as (a) $\sum B_z$ over the
enclosed plaquettes and (b) holonomy$/q$ — the charge-coupling loop closes.

## What this certifies (and what it does not)

It certifies the **first-generation U(1) charge-coupling path is intact on the
post-F69 photon**: the coupling that minimal coupling selects (F68) reads a flux
via a helicity-blind holonomy and sources a field while conserving charge, both to
machine precision, with $c_\text{lat}=1/\sqrt3$ throughout. It is the EM-sector
analogue of F85 (which certified the matter fields as real-time wavepackets).

Scope: this is the *Abelian* (U(1)/hypercharge) coupling — the identity channel.
It does **not** address the non-Abelian W/Z/gluon couplings (still carried by the
σ-bilinear, F68 part 3), nor full dynamical fermion + radiation back-reaction
(the holonomy is verified as an operator/transport phase, not yet a scattering
amplitude). Two lattice subtleties were handled, both signal-processing not
physics: (i) the curl symbol must be projected to its **odd-in-$k$ part** to keep
the real $(\mathbf E,\mathbf B)$ field real (the even remainder is invisible to
the single-mode eigen-analysis of `maxwell_curl_residual` but a real-field stepper
sees it); (ii) **odd lattice length** $L$ is used in the curl sector to avoid the
self-paired Nyquist bin breaking exact oddness (same even-grid issue corrected in
F37).
