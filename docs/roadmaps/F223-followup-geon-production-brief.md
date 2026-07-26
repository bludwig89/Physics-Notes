# Research brief — Geon production within the model as it stands (F223 follow-on)

> You are the research assistant on the "universe in a bottle" BCC Weyl-QCA project (see `CLAUDE.md`). F223 closed the F216 §6 obstruction on the *binding* side: the graviton–graviton J=2 "geon" **binds** at the Planckian virial mass **μ ≃ √2 M_Pl ≈ 1.7×10¹⁹ GeV** (a structurally perfect cold, collisionless CDM particle passing every kinematic DM screen), while the ν_R ν_R J=2 channel is a clean no-go. F223 also showed the *production* side is the one remaining soft number: cosmological gravitational particle production (CGPP) under-produces by ~10⁵ orders because the virial pins μ far above the maximum inflationary Hubble scale (μ/H_inf ~ 3×10⁵), leaving only Planck-mass-relic (PBH-remnant) or preheating channels, with the abundance tunable via an external input.
>
> **Your task:** determine, *within the model as it stands*, how the geon is actually produced — whether any channel reaches Ω_DM h² ≈ 0.12 without new physics, and what the dominant-uncertainty band is. **Gate the whole thing on stability first** (a Planckian geon may radiate to gravitons or Hawking-evaporate before today). Prefer algebraic exactness, then machine precision (CLAUDE.md). Produce a new finding, a self-contained real-arithmetic module in `ca-simulation/forks/`, a test in `tests/findings/`, a results JSON, a changelog entry, exactness-inventory row(s), and regenerate the indexes. Update F223 §6 to point at the closure.

---

## Context to load first (targeted, not everything)

- **This line's chain:** `findings/F223-spin2-bound-state-binding-and-relic.md` (the binding result + the open production obstruction — §4/§6), `findings/F216-massive-spin2-dark-mode.md` (why a massive spin-2 must be a gauge-neutral bound state; the "Planck-mass relic = black hole" note), `ca-simulation/forks/gr_fork_F223_spin2_binding_relic.py` (the CGPP-suppression + data-battery helpers already written — reuse them).
- **Gravity / Planck scale:** `findings/F79-structural-newton-constant.md` (G = a²c³/(8π√3 ħ) ⇒ M_Pl; zero-tree-stiffness graviton), `findings/F178-gravity-full-tensor-adoption.md` (exact GR, constant G), `findings/F180-gravitational-wave-speed.md` (massless luminal graviton, induced self-energy ∝ Q²).
- **Black-hole / remnant machinery (the load-bearing route):** `findings/F183-blackhole-under-full-tensor.md` (exact Schwarzschild/Kerr, **Hawking radiation**, evaporation), `findings/F190-horizon-entropy-lattice-microstates.md` (S=A/4 iff each F107 cell carries 2π√3 nats — **does evaporation halt at a lattice-cell Planck remnant?**), `findings/F114-dielectric-black-hole.md` + `findings/F186-shadow-raytracer-microarcsec.md` (superseded shadow, but the horizon-structure discussion), `ca-simulation/ca_blackhole.py`.
- **Model cosmology (the consistency check):** `findings/F182-friedmann-pressure-cosmology.md` + `findings/F188-multicomponent-lcdm-cosmology.md` (standard ΛCDM: z_eq≈3430, age≈13.8 Gyr — the timeline any relic must preserve), `findings/F196-dilution-exponent-derived.md` (holographic dilution / horizon-scale reasoning), `ca-simulation/ca_cosmology.py`, `ca-simulation/ca_darkmatter.py`.
- **Relic-computation templates:** `findings/F198-angular-mode-relic-misalignment.md` (how a relic band + its dominant uncertainty gets named), `findings/F205-sterile-qke-boltzmann-margins.md` (momentum-resolved Boltzmann yield), `findings/F200-sterile-neutrino-dark-matter.md` (the stability/lifetime screen structure), `findings/F164-cosmological-constant-*.md` / `findings/F192-vacuum-energy-full-tensor.md` (the model's vacuum-energy accounting, in case reheating touches it).

## Step 0 — Stability gate (do this first; it can kill the candidate)

A √2 M_Pl geon sits at its own gravitational-radius scale, so two independent decay/disappearance channels must be ruled out before any abundance matters. Both mirror the F199/F200 lifetime screens.

1. **Radiative decay geon → 2 free gravitons.** The bound state can un-bind by emitting gravitational radiation (Wheeler/Brill–Hartle geons are only *quasi*-stable). Estimate the width Γ from the gravitational-strength binding (the same α_g = (m/M_Pl)² vertex used in F223), and require the lifetime τ = ħ/Γ ≫ t₀ = 13.8 Gyr (F188). If τ ≪ t₀ the geon is not dark matter — a clean no-go, and PBH remnants (below) become the only tensor-dark object.
2. **Hawking evaporation.** A Planck-mass object has Hawking temperature T_H ~ M_Pl (F183); a Schwarzschild BH of that mass evaporates in ~t_Pl. The decisive question is whether the model's **horizon-cell structure (F190, 2π√3 nats/cell)** forces evaporation to **halt at a stable one-cell Planck remnant** — in which case the geon and the remnant are the *same* stable object — or whether it evaporates completely. Resolve this using F183 + F190 (and F114's horizon discussion); it determines the ontology in Step 3.

**Deliverable of Step 0:** τ_geon vs t₀ (radiative) and a definite verdict on evaporation-vs-remnant, with the exactness tier noted. This gates everything downstream.

## Step 1 — Enumerate and compute the production channels (model-native only)

Evaluate each; several will fail, and quantified failures are results (F198/F199 templates). Because the geon is **composite**, first fix the treatment: either (i) an effective heavy field of mass μ, gravitational coupling ∝ 1/M_Pl, and a **compositeness form factor** cutting off momentum transfers above the binding scale (size R ~ √N ℓ_P), or (ii) explicit two-graviton production + coalescence. Justify the choice and use it consistently.

- **(a) Planck-mass relics from PBH evaporation.** If Step 0 gives a stable remnant, the abundance is set by the primordial black-hole mass function; compute the initial PBH energy fraction β(M_form) required to land Ω_relic h² ≈ 0.12, and check it against known PBH constraints. This is the most "within the model" route (F183/F190).
- **(b) CGPP, done rigorously.** Upgrade F223's representative exp(−2πμ/H) estimate to an actual Bogoliubov-coefficient computation for a heavy field in the F182/F188 FRW background (`ca_cosmology.py`), and quantify the exact suppression vs (H_inf, T_RH). Confirm it cannot reach 0.12.
- **(c) UV freeze-in via graviton exchange.** SM/inflaton + SM → geon geon has rate Γ ~ T⁶/M_Pl⁴; integrate the Boltzmann yield and show the T_RH dependence. For μ ~ M_Pl this needs (near-)Planckian T_RH — quantify how far it falls short at CMB-allowed T_RH.
- **(d) Graviton coalescence.** Thermal/produced gravitons binding pairwise into geons (2→1 with the binding form factor); estimate the rate and its α_g / phase-space suppression.
- **(e) Preheating / parametric resonance.** The model has **no explicit inflaton finding** — state this. Either treat the reheating sector as an external input (representative H_inf, T_RH, as F198/F205 did with g_*), or, if you posit a high-scale lattice condensate as the inflaton, flag it explicitly as *beyond the model as it stands*.

**Deliverable of Step 1:** a per-channel Ω_DM h² (or a quantified shortfall), with the single dominant uncertainty identified and banded (PBH β for (a); T_RH for (b)–(d)).

## Step 2 — Consistency with the model's own cosmology

Feed the surviving channel's Ω into `ca_cosmology.py` / the F188 multi-component solver and confirm the ΛCDM timeline is preserved: z_eq ≈ 3430, matter–radiation ordering, age ≈ 13.8 Gyr, and that the relic is non-relativistic at equality (already cold from F223 S6). Confirm no overclosure and no ΔN_eff tension at BBN/CMB.

## Step 3 — Ontology verdict

Answer plainly: **is the geon distinct from a Planck-mass black-hole remnant, or the same object?** If Step 0 gives a stable F190 remnant and the only viable abundance is the PBH-remnant route, then F223's "graviton–graviton geon" and "Planck relic" are the *same* tensor-dark object under two descriptions — say so. If the geon is a genuinely distinct sub-remnant bound state (lighter than, or structurally different from, a one-cell remnant), establish the distinction. This decides whether F223 is a new channel or a re-description of Planck relics.

## Acceptance criteria

1. A stability verdict (radiative τ vs t₀ **and** evaporation-vs-remnant) that gates the rest.
2. Each production channel evaluated with a computed Ω_DM h² or a quantified shortfall; the dominant uncertainty banded (order-of-magnitude acceptable, as F198/F205).
3. The compositeness treatment (effective field + form factor, or coalescence) chosen and justified.
4. Consistency with F182/F188 cosmology confirmed (z_eq, age, no overclosure, ΔN_eff).
5. A definite ontology verdict (geon vs Planck relic).
6. Standard artifacts: `findings/F###-*.md`, `ca-simulation/forks/gr_fork_F###_*.py`, `tests/findings/test_F###_*.py`, `test-results/F###_*.json`, `docs/status/changelog.md` entry, `docs/status/exactness-inventory.md` row(s), `python3 tools/regen_indexes.py`, and F223 §6 updated to point here. Re-check the finding number before writing (concurrent sessions took F219–F222; pick the first free slot).

## Honest risks to flag up front (don't bury these)

- **The geon may be unstable.** If it radiates to gravitons on τ ≪ t₀, or Hawking-evaporates without a remnant, the geon is a no-go and the whole tensor-dark result collapses onto PBH remnants — which may or may not count as "within the model as it stands." Decide early.
- **Every gravitational channel is Planck-suppressed.** The likeliest honest outcome is "only the PBH-remnant route reaches 0.12, and its abundance is a free β" — a legitimate but *soft* result. Quantify β rather than claiming a prediction.
- **No inflaton in the model.** Reheating parameters (H_inf, T_RH) are external cosmological inputs here; be explicit about that boundary, exactly as F223 was.
- **Compositeness is not optional.** Treating the geon as elementary will over-count production above the binding scale; the form factor (size √N ℓ_P) is essential and must be justified.
- **Numpy/complex caution (CLAUDE.md).** Bogoliubov mode-function integration (channel b) is complex arithmetic — verify the real/imaginary handling by hand before trusting numpy, and prefer a hand-rolled real 2-component integrator if in doubt (the project has been bitten by numpy dropping the imaginary part).

## Definition of done

A stability-gated verdict on geon production: either a viable channel with a computed Ω_DM h² band and its dominant uncertainty named, **or** a documented no-go per channel with the residual pinned to a single external input (PBH β or trans-Planckian T_RH) — plus the ontology answer (geon vs Planck relic) and confirmed consistency with the F188 cosmology. F223's §6 production obstruction is then closed the same way F223 closed F216's binding obstruction: the mechanism is settled, and any remaining freedom is reduced to one clearly-named number.
