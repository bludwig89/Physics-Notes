# F209 — Time-modulating a Casimir cavity does **not** break the F207-G1 degeneracy: the beable-source weight and the SEP vacuum-buoyancy weight coincide at **every** order/harmonic of Archimedes modulation, and dynamical-Casimir real-pair emission is degenerate too — the beable-vs-template split is **not lab-accessible via Casimir at any order** (honest negative, sharpened)

**Date:** 2026-07-01 - 01:20
**Numbering:** **F209** (re-checked per CLAUDE.md — committed max was F208; a concurrent session had taken F207/F208, F209 verified free).
**Status:** Confirmed — 4/4 checks PASS. The result is a **clean, sharpened negative**: M1 exact-algebraic (degeneracy at all harmonics), M2 exact (offset cancels differentially — the forcing mechanism), M3 exact (DCE beable = drive-supplied, residual 0), M4 quantified (both signals unweighable). No new physics introduced.
**Module:** `ca-simulation/ca_casimir.py` (new time-dependent functions; F207 statics reused verbatim).
**Test / results:** `tests/findings/test_F209_modulated_casimir.py` (4/4) → `test-results/F209_modulated_casimir.json`.
**Cross-references:** [[F207-casimir-effect-source-channel-and-gravitation]] (the static G1 degeneracy and D1 two-mode squeezing this extends), [[F193-ontic-vacuum-gravitates-as-zero]] (the load-bearing beable-vs-template assumption under test; the named soft spot), [[F106-psi-K-sourcing-derivation]] / [[F178-gravity-full-tensor-adoption]] (the dielectric source ∇²lnK=−(8πG/c⁴)T⁰⁰), [[F180-gw-speed]] (the dynamical/retarded generalisation — same equation in both pictures), [[F69-paired-spinor-photon]] (the photon; DCE event = two F69 photons = four Weyl quanta), [[F26-speed-of-light-as-rotation-rate]] (c=1/√3). External: Calloni et al. 2014 / Avino et al. 2020 (Archimedes); Wilson et al. 2011 (DCE); Jaffe 2005 (source picture).

---

## The question F207 left open

F207 G1 answered the static make-or-break question in the negative: the Casimir shift gravitates as beable binding energy Δm=E_C/c², which is **numerically degenerate** with the SEP vacuum-buoyancy weight after universal vacuum renormalisation, so *static weighing cannot discriminate* the model's beable-source gravity from ordinary SEP. The Casimir cavity is the one lab system where "actual configuration energy" and "zero-point sum" are, in principle, separable, so the open move is **modulation**. This finding evaluates the two candidate modulated regimes and returns a binary, defensible answer.

**The deliverable question.** *Is there a modulated Casimir regime where the beable-source prediction departs measurably from SEP buoyancy / the template ⟨T⁰⁰⟩?*

**The answer is NO** — and, more sharply, the degeneracy is **not merely leading-order**: it is forced at the level of *what a weighing measures*. Every lab-weighable quantity is an energy **change**, which is a beable configuration-energy shift in both pictures. The beable-vs-template difference lives entirely in the **homogeneous, unchanging, universally-renormalised zero-point offset** — precisely the quantity modulation never moves.

## What was computed (4/4 PASS)

| # | Check | Method | Result | Tier |
|---|---|---|---|---|
| M1 | Archimedes reflectivity modulation | η(t)=η0+δη cos(2π f t); beable weight via **Gauss closure** of ∇²lnK=−8πT⁰⁰ (F207 G1) vs SEP weight via **buoyancy definition** — two independent formulas, compared in time domain and every Fourier harmonic, over f∈{1, 3.7, 1000} Hz and (η0,δη)∈{(.5,.5),(.7,.3),(.9,.1)} | time-domain max\|ΔW\|=0 and FFT max\|Δ\|=0 for **all** frequencies/depths, with the signal genuinely modulating (ptp ∼10⁻²⁴ N) → **degeneracy survives to all orders** | **exact-algebraic** |
| M2 | The forcing mechanism | differential (tared) weighing W(sig)−W(ref) with a homogeneous offset ρ0 added to T⁰⁰, for ρ0∈{0, ρ_Λ, F164 bare 3.46×10¹¹¹} | offset contribution to the differential ≡ 0 **exactly** for **arbitrary** ρ0 (it fills space equally inside and outside — F193 A4); only the beable Casimir differential (−4.7×10⁻²⁴ N) survives | **exact** |
| M3 | Dynamical Casimir (DCE) | radiated beable energy E_rad=ħΩ_d sinh²(gt) (F207 D1); Δm_beable=E_rad/c² (real quanta) vs Δm_SEP=E_rad/c² (drive-supplied, energy conservation); template-change vs beable-change | residual **0** on both — the radiated energy is drive work in both pictures; template Δ⟨T⁰⁰⟩ = beable ΔT⁰⁰ = E_rad (offset unchanged) → **DCE degenerate too** | **exact** |
| M4 | Quantified realism | Archimedes (Avino-class 1 cm²/10 nm full switch) and DCE (Wilson ∼10.3 GHz, ∼10⁴ photons/s) weight signals | Archimedes ΔW≈4.7×10⁻²⁴ N; DCE ΔW≈7.4×10⁻³⁶ N — degenerate **and** ≳10⁶–10¹⁸× below any balance → not a lab handle | **quantified negative** |

## The crux — why modulation cannot break the degeneracy

**Two structural facts do all the work.**

**(1) In the weak field the model *is* GR (F178: PPN β=γ=1; F180: c_grav=c_lat=c).** The beable-source route (feed E_C into ∇²lnK=−8πT⁰⁰, close by Gauss) and the SEP-buoyancy route (weight of displaced vacuum energy) are therefore the *same field equation applied to the same source*. M1 computes them from genuinely different formulas and gets bit-identical signals — in the time domain **and** in every Fourier harmonic — for arbitrary modulation waveform, depth, and frequency. Finite-frequency retardation (gravitational radiation from the modulated Casimir mass) does not help: it is governed by the **same** F180 wave equation (∇²−c⁻²∂ₜ²)lnK=−8πT⁰⁰ in both pictures, so it too is degenerate. There is no order in the modulation at which the two routes separate, because they are not two theories.

**(2) The beable-vs-template dispute is *entirely* about the homogeneous offset Σ½ħω, and modulation never touches it.** This is the sharpening (M2). The whole content of F193's load-bearing assumption is whether the homogeneous zero-point sum Σ½ħω gravitates (template) or not (beable). But:

- Reflectivity modulation (Archimedes) changes only the **finite, renormalised, configuration-dependent** Casimir energy E_C(η(t)); the divergent bulk self-energy is renormalised into the mirrors' rest mass (F207 C4, Jaffe), and the homogeneous offset is identical inside and outside the cavity and identical across the switch (F193 A4).
- DCE (M3) creates **real** quanta whose energy is supplied by the **drive**, not extracted from the offset; the zero-point sea seeds the *rate* (sinh²(gt)) but the offset itself is unchanged.

A balance measures a **change** (it is tared). The offset — being homogeneous and unchanging — cancels **exactly** in any differential measurement, for *arbitrary* ρ0, including the F164 bare 3.46×10¹¹¹ J/m³ (M2 verifies the cancellation is independent of ρ0). What survives is the beable Casimir differential, which both pictures weigh identically by fact (1). **The one quantity that could discriminate is, by construction, the one quantity no differential weighing can see.**

## Regime-by-regime verdict

**1. Archimedes (Calloni/Avino).** Degeneracy survives modulation **to all orders and all harmonics** (M1, exact). Switching a superconducting mirror modulates E_C(t); both the beable-source weight and the SEP-buoyancy weight track g·E_C(t)/c² identically. A surviving degeneracy was itself flagged as a clean result in the brief — it is now established, with the forcing mechanism (M2) made explicit: the offset cancels differentially, so modulation only ever weighs beable energy, which is not where beable and template differ.

**2. Dynamical Casimir (Wilson).** The appealing intuition — "DCE turns a template superimposable into beable quanta" — is *correct about the quanta but wrong about the energy source*. DCE promotes vacuum *fluctuations* into real pairs, but the **energy** those pairs carry is drive work (energy conservation), not liberated offset. So the radiated energy gravitates (M3, beable) in exactly the amount the SEP/energy-conservation accounting already books for the drive (M3, degenerate, residual 0). The template-change and beable-change both equal E_rad because creating real photons *adds* to ⟨T⁰⁰⟩ in both pictures by the same E_rad; they differ only in the unchanging absolute offset. **DCE does not un-renormalise the cosmological constant** and is not a discriminator. (Its genuine model-specific content is structural, not gravimetric: one DCE event = two F69 photons = four Weyl quanta, doubly paired — a counting/correlation signature, F207 D1, carried forward unchanged.)

## Verdict

**No modulated Casimir regime — Archimedes or DCE — makes the beable-source prediction depart from SEP buoyancy / the template.** The F207-G1 degeneracy is not fragile-at-leading-order but **structurally forced**: (i) the model reproduces GR in the weak field, so the two gravitation routes are one equation; (ii) every weighable quantity is an energy change = a beable configuration shift, which both pictures agree on; (iii) the sole discriminating quantity, the homogeneous offset Σ½ħω, is unchanged by any Casimir modulation and cancels exactly in any differential weighing. This **sharpens F193's named caveat** from *"static weighing is degenerate"* to *"the beable-vs-template split is not lab-accessible via the Casimir effect at any order of modulation,"* with the order of forcing identified as **zeroth — the definition of the observable**, not a coincidence at leading order. Realistic signals (≈4.7×10⁻²⁴ N Archimedes, ≈7.4×10⁻³⁶ N DCE) are in any case far below weighability. We explicitly do **not** claim a lab gravity test — consistent with F207's earlier correction of that framing.

## What is exact vs computed vs honest-negative

| Piece | Status |
|---|---|
| Beable weight = SEP weight at every harmonic of η(t) modulation | **Exact-algebraic** (independent formulas, residual 0 in time + FFT) |
| Homogeneous offset ρ0 cancels in a differential weighing for arbitrary ρ0 | **Exact** (structural; verified incl. F164 bare 3.46×10¹¹¹) |
| DCE Δm_beable = Δm_SEP (radiated energy = drive work) | **Exact** (residual 0) |
| DCE template-change = beable-change = E_rad | **Exact** (offset unchanged) |
| Degeneracy is zeroth-order / structural (order of forcing) | **Derived** (observable = energy change = beable shift) |
| Archimedes ≈4.7×10⁻²⁴ N, DCE ≈7.4×10⁻³⁶ N | **Computed** (Avino/Wilson-class parameters) |
| "Modulated Casimir tests F193's core assumption" | **Honest negative** — not accessible at any order via Casimir |

## Caveats (do not overclaim)

- The negative is *about the Casimir channel specifically*. It shows the beable-vs-template split cannot be reached by Casimir modulation; it does **not** prove the split is untestable by every conceivable means (a system that physically *converts* offset energy into weighable form — none known — would be the target).
- M1's exact zero reflects that the two pictures are the same weak-field equation (F178/F180). If a future finding broke PPN β=γ=1 at some order, M1 would need re-checking; within the adopted gravity sector it is structural.
- The E_C(η)=η²E_C_ideal switch is a concrete monotone; the degeneracy verdict is independent of the switch shape (it follows from facts (1)–(2), not from f(η)).
- DCE's sinh²(gt) parametric growth is the idealised resonant proxy (F207 D1); real DCE saturates and decoheres, lowering the signal further — it does not change the degeneracy.

## Open / next

- The genuinely model-specific Casimir signature remains the O((a/L)²) lattice dispersion correction (F207 C3, ∼10⁻⁵⁶ for lab L) — a falsifier in principle, unobservable, and *not* a beable-vs-template discriminator (it shifts both pictures equally).
- If F193's assumption is ever to get a lab handle, it must come from a process that moves the **homogeneous** offset itself, not a boundary-shift (Casimir) or drive-fed pair-creation (DCE); no such process is identified here. Recorded as the sharpened obstruction.

## Files
- Module: `ca-simulation/ca_casimir.py` (`casimir_energy_reflectivity`, `weight_beable`, `weight_sep_buoyancy`, `modulated_weight_signals`, `homogeneous_offset_differential`, `dce_radiated_gravitating_mass`, `dce_change_beable_vs_template`).
- Test: `tests/findings/test_F209_modulated_casimir.py` (4/4).
- Results: `test-results/F209_modulated_casimir.json`.
