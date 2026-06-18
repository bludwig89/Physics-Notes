# F136 — The scalar confining string on genuine SU(3) colour-triplet quarks: a real-space confined proton

**Date:** 2026-06-11 - 20:10
**Status:** Confirmed — 3/3 checks PASS. Q1 exact (rational charge); Q2 quantitative (bounded vs dispersing cluster, norms machine-precision); Q3 structural (SU(3) loop live).
**Module:** `src/casim/particles/channel.py` (new `ColourDiracQuarkChannel`, type `quark_dirac`).
**Scenarios:** `scenarios/proton_confined.yaml`, `scenarios/proton_confined_free.yaml` (control).
**Test:** `tests/findings/test_F136_colour_quark_confinement.py` (3/3, ~60 s).
**Results:** `test-results/casim_proton_confined{,_free}.json`.
**Cross-references:** [[F135-realspace-scalar-confinement]] (the scalar string this carries onto colour quarks), [[F134-unified-real-space-integration]] (the U0 chain), [[F122-p2-dynamical-baryon-three-body]] (the spectral uud proton), [[F71-colour-singlet-baryon-proton]] (operator proton + exact quantum numbers), [[F43-fg7-dynamical-gluons]] (the SU(3) gluon loop), `docs/roadmaps/roadmap-unified-real-space.md` (U3 Part 1).

---

## 1. What this closes

F135 demonstrated the scalar confining string but on **colour-blind massive Dirac stand-ins** (the string binds; colour only labels the singlet). This finding promotes it to genuine **SU(3) colour-triplet Dirac quarks** — a `uud` proton with the right charge, the F43 gluon loop live, and the F135 scalar string binding it in real space. It is U3 Part 1 of the unified real-space programme.

## 2. The colour-Dirac quark

The new `quark_dirac` channel carries a 4-component Dirac spinor $(\eta_\uparrow,\eta_\downarrow,\chi_\uparrow,\chi_\downarrow)$ stacked on three colours. Per tick:

1. **SU(3) colour rotation** from the gluon octet potential $A^a(x)$ — $V(x)=\exp(i\,\epsilon\,A^aT^a)$ (`_su3_expmap_field`, the audited F43 primitive) applied to every spinor component's colour axis (the live F43 loop: quark publishes $J^a_\text{colour}$ → `gluon_sourced` accumulates $A$ → rotation back on the quark);
2. **variable-mass Dirac kinetic step per colour** with the F135 Lorentz-scalar confining mass $m_\text{eff}(x)=m+\sigma$-string (`dirac_step_3d_bcc_varm_splitstep`); the confining mass is colour-blind;
3. the **U(1) EM minimal-coupling phase** if charged.

It publishes $J_\text{colour}$ (sources the gluon) and $J_\text{em},\rho_\text{em}$ (sources the photon), closing both loops on a real colour quark. The crucial difference from the Weyl `particle` quark: it is **massive**, so the scalar string binds it (F135) — the massless Weyl quark Klein-tunnels.

## 3. The result — a confined proton (Q1–Q3)

Three colour quarks ($u_r,u_g,d_b$, $m=0.9$, $\sigma=0.5$, COM Y-string), gluon loop live:

| tick | confined cluster RMS | free control RMS |
|---|---|---|
| 0 | 2.02 | 2.02 |
| 40 | 3.43 | 5.63 |
| 80 | 3.66 | 7.37 |
| 120 | 3.72 | 6.76 |

- **Q1 — exact charge:** $\sum Q = \tfrac23+\tfrac23-\tfrac13 = +1$ (uud), rational-exact.
- **Q2 — bound:** the cluster RMS plateaus at $\approx3.7$ (non-dispersing proton) vs the free control's box saturation ($\sim7$); norms conserved to $2\times10^{-14}$.
- **Q3 — SU(3) loop live:** each quark publishes a non-zero $J_\text{colour}$ and the gluon octet potential $A$ grows from it.

So the F135 mechanism now binds a **genuine colour-triplet proton** in real space, with the colour dynamics running.

## 4. Checks

| # | Check | Tier | Result |
|---|---|---|---|
| Q1 | uud aggregate charge $=+1$ | exact (rational) | $+1$ |
| Q2 | scalar string binds colour quarks vs free; norms | quantitative / machine | confined max $3.72$ vs free $>6.7$; drift $2\times10^{-14}$ |
| Q3 | SU(3) loop live ($J_\text{colour}\!\to\!A$) | structural | both $>0$ |

## 5. The honest open edge

The binding is still the F135 **mean-field geometric** string (σ toward the singlet COM); the SU(3) gluon loop runs but the *binding* is the scalar mass, not yet the gluon field itself. Sourcing the confining scalar mass from a live colour field is F137 (Part 2). And the scale separation of F134 §6 stands — this is a compressed-scale proton; physical fm scale is U4.

## 6. Ledger

New `quark_dirac` channel (`ColourDiracQuarkChannel`); two scenarios; suite `tests/findings/test_F136_colour_quark_confinement.py` (3/3). Exactness rows: Tier-1 #79 (uud charge $+1$), Tier-3 #80 (colour-quark scalar confinement bound vs free; SU(3) loop live).
