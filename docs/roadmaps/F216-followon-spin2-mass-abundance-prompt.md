# Session prompt — close the F216 obstruction: mass and relic abundance of the dark spin-2 bound state

**Created:** 2026-07-01 - 13:48
**Owner of the open problem:** [[F216-massive-spin2-dark-mode]] §6 (the named obstruction)
**Suggested next finding number:** re-check `findings/` for the current max before you start (F216 was the last one this line added; a concurrent session held F215-eliashberg). Renumber on collision per CLAUDE.md.

---

## Paste-in prompt for the next session

> You are the research assistant on the "universe in a bottle" BCC Weyl-QCA project (see `CLAUDE.md`). F216 established that the induced gravity sector has **no native massive spin-2 mode** (the metric graviton is exactly massless — UV transversality of the induced self-energy Π∝Q², F180 leg 3; IR irrelevance of the diff-breaking mass operator, F130). It concluded that the **only** admissible massive spin-2 is a **bound state of gauge-neutral constituents** (the sterile ν_R of F47, or a graviton–graviton "gravball"), which — if it exists and is cold — is a collisionless CDM candidate that passes the Bullet Cluster (unlike the emergent-gravity route falsified in F194).
>
> **Your task:** determine whether such a spin-2 bound state actually forms, derive its mass μ, and compute its relic abundance Ω_DM h², then confront it with the dark-matter data battery. Prefer algebraic exactness, then machine precision (CLAUDE.md). Produce a new finding, a self-contained real-arithmetic module in `ca-simulation/forks/`, a test in `tests/findings/`, a results JSON, a changelog entry, and regenerate the indexes.

---

## Context to load first (targeted, not everything)

- **This line's chain:** `findings/F216-massive-spin2-dark-mode.md` (the negative result + the open obstruction), `findings/F79-structural-newton-constant.md` (K has zero tree stiffness; conformal ln K mode), `findings/F180-gravitational-wave-speed.md` (induced self-energy Π∝Q²; c_grav=c_lat), `findings/F178-gravity-full-tensor-adoption.md` (exact GR, constant G).
- **Constituent candidates:** `findings/F47-*` (ν_R = total SM singlet, Y=0, Majorana), and the sterile-DM relic machinery already built: `findings/F200-sterile-neutrino-dark-matter.md`, `findings/F201-kev-sterile-from-eg-texture.md`, `findings/F205-sterile-qke-boltzmann-margins.md`.
- **Dark-relic obstruction precedent:** `findings/F197-first-excitation-dark-source.md`, `findings/F198-angular-mode-relic-misalignment.md`, `findings/F199-amplitude-mode-stability-nogo.md` (how a relic-abundance obstruction gets computed and named in this project).
- **DM data battery:** `findings/F191-dark-matter-rotation-curves-bullet.md`, `findings/F194-emergent-gravity-bullet-falsification.md` (`ca-simulation/ca_darkmatter.py`, `ca_emergent_gravity.py`).
- **Bound-state solvers to reuse:** `ca-simulation/ca_atom.py` (F125, attractive-1/r two-body), `findings/F122-*` / `findings/F140-*` (ECG / Cornell three-body + hyperradial machinery), `ca-simulation/forks/gr_fork_F216_massive_spin2.py` (the polarization/dof + equation-of-state helpers already written — reuse them).

## The concrete work

**Step 1 — Does it bind? (this gates everything.)**
Evaluate both channels honestly; either may fail, and a clean no-go is a real result:

- **Graviton–graviton spin-2 ("gravball"/geon).** Two helicity-2 gravitons can couple to J=2. Binding is gravitational-strength via the GR cubic vertex (the induced action of F79/F180). Set up the two-body potential from one-graviton exchange + the contact vertex, solve for a J=2 bound state (reuse `ca_atom.py`-style solver with the derived potential). Expected risk: binding is Planck-suppressed ⇒ μ ~ M_Pl (WIMPzilla regime). Determine whether a bound state exists at all and where μ lands.
- **ν_R ν_R spin-2.** Two spin-½ give J=2 only with orbital L≥1 (S=1 ⊗ L=1 → J=2). Check (a) whether the model supplies enough attraction — ν_R's only channels are gravitational, the F47 Majorana mass, and any E_g/Z₃-texture portal (F201) — and (b) whether a P/D-wave J=2 state binds. If gravity is the only force, expect no binding at sub-Planck scales; state that explicitly.

Deliverable of Step 1: the two-body potential(s) derived from the model (not posited), the J=2 radial/Bethe-Salpeter solve, and μ = 2m_constituent − E_b (or the geon virial mass), with the exactness tier noted.

**Step 2 — Relic abundance Ω_DM h².**
For whichever channel binds, compute the yield. Because the coupling is gravitational-only, the relevant production is **gravitational particle production / freeze-in** during reheating (not thermal freeze-out), unless a portal exists. Mirror the F198 misalignment and F205 QKE Boltzmann computations in structure. Output Ω_DM h² vs the observed 0.12 (Ω_DM ≈ 0.26), with the dependence on reheating temperature / initial conditions made explicit (this is the likely dominant uncertainty — quantify it, as F198 did for the 15-order misalignment shortfall).

**Step 3 — Confront the data battery.**
Reuse F216's screens and `ca_darkmatter.py`:
- Cold ⇒ w→0 (already in `gr_fork_F216`); confirm the relic is non-relativistic at matter–radiation equality.
- Fuzzy-DM / Lyman-α floor: μ ≳ 10⁻²¹ eV (else excluded). Check against the derived μ.
- ΔN_eff from any relativistic tail at BBN/CMB.
- Bullet Cluster: σ/m ≪ SIDM bound (F216 C2 shows gravitational self-interaction is negligible — re-confirm for the actual μ).
- Structure growth / CMB: at minimum a qualitative CDM-consistency statement; a full CMB fit is out of scope but name it.

## Acceptance criteria

1. A derived (model-native, not posited) two-body potential for at least the graviton–graviton channel, with the J=2 bound-state solve run to the solver's floor.
2. A definite verdict per channel: **binds → μ value**, or **no-go → why** (both are publishable outcomes; F199 is the template for a clean no-go).
3. Ω_DM h² computed for any binding channel, with the reheating-temperature dependence quantified (order-of-magnitude band acceptable, as in F198/F205).
4. The full data battery (cold, fuzzy floor, ΔN_eff, Bullet, structure) evaluated against the derived μ.
5. Standard artifacts: `findings/F###-*.md`, `ca-simulation/forks/gr_fork_F###_*.py`, `tests/findings/test_F###_*.py`, `test-results/F###_*.json`, `docs/status/changelog.md` entry, `docs/status/exactness-inventory.md` row(s), and `python3 tools/regen_indexes.py`.

## Honest risks to flag up front (don't bury these)

- **Planck-scale mass.** Pure gravitational binding likely gives μ near M_Pl (a super-heavy WIMPzilla). That is *not* fatal — gravitationally-produced super-heavy spin-2 DM is viable in the literature (Babichev et al. 2016) — but it changes the production story (Step 2) entirely and pushes μ far above the fuzzy floor. Decide early which regime you're in.
- **ν_R ν_R may simply not bind into J=2.** If so, say so cleanly; the graviton–graviton channel then carries the whole result.
- **Relic abundance from gravitational production is reheating-dependent.** Expect the abundance, not the mass, to be the softest number. Quantify the band rather than quoting a single Ω.
- **Numpy/scipy caution (CLAUDE.md).** The bound-state solve is real arithmetic — safe — but if you touch any chiral/complex spinor step for the ν_R channel, verify the transform by hand first (the project has been bitten by numpy dropping the imaginary part).

## Definition of done

F216's obstruction is closed either way: a derived mass μ (with regime and exactness tier) **plus** a quantified Ω_DM h² band **plus** the data-battery verdict — or a documented no-go for each channel that binds nowhere. Update `findings/F216-massive-spin2-dark-mode.md` §6 to point at the new finding as the closure.
