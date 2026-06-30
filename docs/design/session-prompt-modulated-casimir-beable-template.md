# Session prompt — Does a *modulated* Casimir cavity probe the beable-vs-template split?

**Created:** 2026-06-30 - 22:10
**Thread:** advances the load-bearing assumption of [[F193-ontic-vacuum-gravitates-as-zero]], following the honest negative of [[F207-casimir-effect-source-channel-and-gravitation]] G1.

---

## Paste-to-start prompt

> **Goal.** Settle whether a *time-modulated* Casimir cavity can test F193's one load-bearing
> assumption — that gravity couples to the **beable** field-energy density, not the **template**
> ⟨T⁰⁰⟩ with its zero-point sum — in a regime that is **not** degenerate with strong-equivalence-
> principle (SEP) vacuum-buoyancy. This directly attacks F193's named soft spot, not a side-quest.
>
> **Where it stands.** F207 G1 already computed the static, leading-order case: the Casimir shift
> gravitates as beable binding energy Δm = E_C/c², which is **numerically degenerate** with the
> SEP vacuum-buoyancy weight after universal vacuum renormalisation. So *static weighing cannot
> discriminate* (honest negative, already recorded). The Casimir cavity is the one lab system where
> "actual configuration energy" and "zero-point sum" are experimentally separable, so the open move
> is modulation, not statics.
>
> **The two candidate modulated regimes to evaluate:**
> 1. **Archimedes-type modulation** (Calloni 2014 / Avino 2020): a superconducting transition
>    switches the cavity's reflectivity, modulating the Casimir/vacuum energy, and the modulation is
>    weighed on a balance. Compute the time-dependent weight signal in (a) the model's beable-source
>    picture (feed the *change* in E_C as ΔT⁰⁰ into ∇²ln K = −(8πG/c⁴)T⁰⁰, F106/F178) and (b) the
>    SEP vacuum-buoyancy picture. Determine algebraically whether the two differ at **any** order in
>    the modulation, or whether the F207-G1 degeneracy survives modulation. A surviving degeneracy is
>    itself a clean result that tightens F193's caveats.
> 2. **Dynamical Casimir (DCE) drive** (Wilson 2011; F207 D1): a parametric boundary drive converts
>    vacuum modulation into **real radiated pairs** — i.e. it turns a superimposable (template
>    zero-point) into beable quanta. This is the most direct place the beable-vs-template split
>    becomes operational. Ask: does the radiated-pair energy gravitate (must, if beable) in a way the
>    template picture would not account for, and is the predicted signal non-degenerate with any SEP
>    interpretation? Use the existing F207 D1 two-mode-squeezing result (n_a = n_b = sinh²(gt),
>    residual 0) as the starting beable source; remember a DCE photon = two F69 photons = four Weyl
>    quanta (the doubly-paired structure, F207 D1 — do not conflate with F69's *internal* pairing).
>
> **Method, per project practice.** Derive algebraically first; reach for machine-precision CASIM /
> `ca_casimir.py` only to confirm a closed form. Reuse what F207 already built
> (`casimir_gravitating_mass`, `dielectric_enclosed_mass_gauss`, `two_mode_squeezing`); add the
> *time-dependent / modulated* source as a new function rather than re-deriving the statics. Watch
> numpy/scipy on any chiral-transform step (CLAUDE.md). Keep ħ, c = 1/√3, a (F107) explicit.
>
> **What counts as the deliverable.** A binary, defensible answer to: *is there a modulated regime
> where the beable-source prediction departs measurably from SEP buoyancy / the template?*
> - **If no** → a clean negative that sharpens F193's caveat from "static is degenerate" to
>   "the split is not lab-accessible via Casimir at all," with the order at which degeneracy is
>   forced.
> - **If yes** → the first genuine lab handle on F193's core assumption; specify the observable,
>   its size for realistic Archimedes/DCE parameters, and whether it is a falsifier in principle or
>   in practice.
> Either outcome advances F193's named obstruction. Do **not** overclaim a "first lab gravity test"
> unless the non-degeneracy is established and the signal is quantified — F207 already corrected that
> optimistic framing once.
>
> **Bookkeeping.** Re-check the current max F-number before numbering (concurrent sessions have
> collided here before — F207/F208). Write the result as a new `findings/F{N}-*.md`, update
> `docs/status/exactness-inventory.md` (mark each result exact / computed / honest-negative),
> add a one-paragraph `docs/status/changelog.md` entry, then run
> `python3 tools/regen_indexes.py`. Cross-reference F193, F207, F106/F178, F69, F26.

---

## Why this is the right next step (context, not part of the paste)

- F196 already derived F193's *dilution exponent* (p = 2), so that obstruction is closed; the
  remaining exposed assumption in F193 is the **beable-source reading itself**, stated plainly in
  F193's load-bearing-assumption box. Making that assumption testable (or proving it isn't, in the
  one accessible system) is the highest-value follow-up.
- F207 G1 is explicitly an *honest negative on statics only*; its "Open / next" already flags a
  real-space moving-boundary DCE sim. This prompt operationalises that into the F193 question.
- Literature anchors already in the repo: `references/casimir-force-literature-and-model-integration.md`,
  `docs/design/casimir-effect-build-brief.md`; external Calloni 2014, Avino 2020 (Archimedes),
  Wilson 2011 (DCE), Jaffe 2005 / Nikolić 2016 (source picture).
