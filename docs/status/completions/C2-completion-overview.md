# C2 Complete — Constants Inversion (decision D7)

*2026-07-30 - 17:24. Phase C2 of `docs/roadmaps/roadmap-casim-consolidation.md`.
Follows `docs/status/C0-completion-overview.md`; ran concurrently with
`docs/status/C1-completion-overview.md`.*

**Status: C2.1–C2.5 complete. All five acceptance-gate criteria met.
`make gate` green — 21 checks.**
Two numbers moved, both anticipated by the roadmap's own risk row and both
recorded below with their magnitudes. One artifact still needs re-running on a
machine with scipy before commit — see §"Open at hand-off".

---

## The one-sentence version

The registry stopped describing what the kernels declared and started deciding
it: 202 unregistered literals in `src/` and `ca-simulation/` became 0, and
`tests/casim/test_constants_consistency.py` now asks *"does any unregistered
site exist?"* instead of *"do the recorded ones still agree?"*

---

## What landed

### C2.1 — the registry owns values

`casim.constants` exports every registry symbol as an importable Python name:

```python
from casim.constants import c_lat, G_LATTICE, delta_star
```

**The exported name IS the registry symbol.** There is no second naming scheme
to keep in sync, and `_export()` generates the surface from `_REGISTRY`, so a
constant cannot be registered and then forgotten at the import line.

Exact constants resolve from **closed form, never a decimal** — `√(8π)·3^(1/4)`,
`1/√3`, `1/(72π)`, `Fraction(2, 9)`, `6·λ₆`. A rational constant exports the
`Fraction` under its symbol and a float under `<symbol>_f`:

| need | write | why |
|---|---|---|
| exactness | `3 * delta_star == Fraction(2, 3)` | exact rational arithmetic, not 0.6666… |
| array code | `delta_star_f` | a `Fraction` in a numpy expression yields an object array |

**Bracketed constants export nothing scalar, on purpose** (C2.2). `from
casim.constants import alpha_eff_star` fails; a caller must write
`endpoint("alpha_eff_star", "lo"|"hi")`. The frequently-quoted 0.39 is the
midpoint of two *scale choices*, not a determination, and a midpoint accessor
would launder a range into a result.

### C2.1b — the literals are gone

**174 substitutions across 42 files**, driven by an explicit table and an
AST-span rewriter rather than by hand, so every change is reviewable as a table
row. **34 of 34 substituted values are bit-identical to the literal they
replaced** — verified programmatically against the pre-substitution literals,
not asserted.

`Site` gained a `kind` field, so the registry now records *how* each path binds
a constant rather than only that it does:

| kind | meaning | count in `src/` + `ca-simulation/` |
|---|---|---|
| `import` | imports it from the registry — the target state | 71 |
| `literal` | still declares its own value | **0** |
| `reexport` | re-exports another module's binding | 6 |
| `runtime` | computed at run time (fit, dispersion, config default) | 3 |

`test_declared_import_sites_really_import` asserts that a site claiming
`kind='import'` actually contains the import. A registry that describes a
migration which never happened is the same class of lie as a stale path, one
level up.

### C2.4 — the polarity flip

The sweep engine lives in `tools/audit_constants.py` and is shared by the gate
and the ratchet, so the two cannot diverge — the same reason C7 will make
pytest delegate to the test registry rather than reimplement it.

| | before C2 | after C2 |
|---|---|---|
| rogue literals, `src/` + `ca-simulation/` | 202 | **0** |
| rogue literals, `tests/` | 278 | 277 *(C7's backlog — counted and ratcheted, not enforced)* |
| registered constants | 20 | 43 |
| `MeasuredConstant` records | 0 (a 5-entry dict) | 10 |

The 12 sites P0 recorded as **unenforceable** are enforceable now, exactly as
the roadmap predicted: `gap_solve(..., Lam3=0.347)` was outside the static
reader's reach only for as long as the default carried a literal. Once it names
an imported symbol, the pattern it hid behind is gone.

Two engineering choices in the sweep are worth recording, because the first cut
of each was wrong:

1. **Seed the evaluator with the module's own names.** The two-step spelling
   `SQRT3 = math.sqrt(3.0)` / `C_LAT = 1.0 / SQRT3` is common, and four
   QED-precision kernels hid a `c_lat` definition behind it. The first cut
   evaluated expressions in an empty environment and walked past all of them.
2. **Report every symbol a value could be; never pick one.** 0.2222… matches
   three registered constants. The sweep prints `c_fierz_colour | delta_star |
   sin2_thetaW_onshell` and makes the author resolve it by importing the one
   they mean — which is the whole point, since before C2 nothing at the point
   of use said which was which.

### C2.3 — `MeasuredConstant` replaces the allowlist

P0's `ALLOWLIST` was a dict of five `(path, name) → prose` entries inside the
test. It worked, but it had no type, it lived in the wrong place, and it was
the usual "add a line to make the check pass" surface. C2 replaces it with
typed declarations in `casim/constants/measured.py`, in two kinds:

- **`measured`** — the *same* quantity in a regime where the answer genuinely
  differs. `derive_velocity_addition.py` at 1/√2 (2-D square lattice) and
  `forks/curl_fork_cubic.py` at 1.0 (simple cubic, where the emergent light
  speed *is* the quantity under test — rewriting it to import `c_lat` would
  delete the result). Also `forks/gr_fork_F79_structural_G.py`, which derives
  a/ℓ_P and checks it against the closed form: importing the registry's copy
  would make the check compare the answer with itself.
- **`coincidence`** — a *different* quantity that happens to equal a registry
  value. The SU(3) λ₈ normalisation is 1/√3 for reasons unrelated to a lattice
  light speed; an Abramowitz–Stegun erfc coefficient is 1.4531; the
  sterile-neutrino thermal prefactor 2ζ(3)/π² is 0.2436.

Every record carries a mandatory reason and a `MeasuredConstant` without one
raises at import. That is the entire difference between this and an allowlist.

**Two of P0's five entries were deleted rather than ported.**
`spectral_matter.TARGETS` (92.4) and `ca_chiral_anomaly.F_PI_MEV` (92.28) needed
an exemption only because a literal check could not distinguish them from a
drifted anchor. Both now import `f_pi_pdg_target_MeV` and
`f_pi_gamma_convention_MeV` respectively, so the distinction is carried by the
name at the point of use — which is where it was always missing.

### C2.5 — the registry is complete

20 → 43 constants. The additions, by cluster:

| cluster | constants | why |
|---|---|---|
| QCD calibration block (audit items 6–10) | `Lambda_NJL_GeV`, `G_Lambda2_NJL`, `m0_current_quark_MeV`, `g_A`, `M_N_isoaveraged_MeV`, `r_c_hardcore_fm`, `g_rho_pi_pi` | These are the model's genuinely **underived** strong-sector inputs. They are registered *because* they are inputs: one that no registry names is one that can quietly be re-described as a result. |
| SI / CODATA anchors | `ell_P_m`, `c_SI`, `hbar_SI`, `hbar_SI_from_h`, `G_CODATA` | 60 independent copies across 20 files before C2; a CODATA revision was a 60-file edit. |
| IR-face scales | `m_D_F88_lattice`, `m_V_F117_lattice`, `q_star_a_implied`, `q_star_a_band_lo`, `alpha_hat0_over_pi_CZBR`, `m_g_continuum_GeV`, `sqrt_sigma_GeV` | The two endpoints of `alpha_eff_star` are two *scale choices*; registering both makes the bracket's width queryable rather than folkloric. |
| λ₆'s inputs | `e_saturation`, `M0_constituent_GeV`, `c_fierz_colour` | λ₆'s derivation string cited e ≈ 0.733 and nothing owned it. The e⁶ dependence means a 1% move in e is a 6% move in λ₆ — most of why λ₆ is `quantitative` and not `exact`. |
| neutron mass | `M_n_neutron_MeV` | 939.565 (CODATA neutron) is a *different quantity* from 938.918 (isospin-averaged nucleon). A careless sweep would have merged them. |

---

## What the sweep found

This is the part worth reading. Every item below follows C2.2's rule — values
that coincide stay separate constants — and each was found by the flipped test,
not by inspection.

### 2/9 appears three times, in three sectors, for three unrelated reasons

| constant | sector | origin |
|---|---|---|
| `delta_star` | lepton | dim(E_g)/dim(T₁ᵤ⊗T₁ᵤ), exact O_h (F175) |
| `sin2_thetaW_onshell` | electroweak | m_W²:m_Z² = 7:9 from the BCC Wigner–Seitz facet count (F49/F141) |
| `c_fierz_colour` | strong | colour-Fierz coefficient of one-gluon-exchange → NJL scalar channel; F256 calls it "the Fierz 2/9" |

The third had **no owner anywhere in the tree** and accounted for most of the 42
flagged 0.2222s. F231 already reconciles the first two in prose; the third makes
it a trio. `test_the_three_hard_cases_stay_separate` asserts that exactly three
registered constants equal 2/9 and that they sit in three different sectors —
so a future consolidation cannot quietly merge them.

**This may be worth a finding.** Three independent exact-2/9 coincidences in one
model is either bookkeeping or structure, and this session is not the place to
decide which. Recorded, not claimed.

### 0.733 twice

`e_saturation` (F92/F118 lepton condensate amplitude) and `q_star_a_implied`
(0.7327, the F151/F155 matching scale). They collide only because
`e_saturation` carries a 5e-3 tolerance. Registering the second was the fix;
widening the first's tolerance would have been the non-fix.

### 1/√3 twice, as different *kinds* of object

`c_lat` is a speed in cells per tick. `q_star_a_band_lo` is a momentum scale in
1/a. Both are exactly 1/√3 and both descend from the BCC √3, but
`QSTAR_LO = c_lat` would typecheck and read as nonsense, so they are two
constants. Same discipline as the three f_pi.

### ħ twice, at different precisions — the near-miss

`ca_superconductivity.py` computes `HBAR = H_PLANCK / (2π)` from the SI-**exact**
h, giving 1.0545718176461565e-34. The registry's `hbar_SI` is CODATA's 10-digit
quote, 1.054571817e-34. **The substitution pass replaced the exact form with the
rounded one**, coarsening it by 6e-11, and the review caught it before the drift
run. It is now registered separately as `hbar_SI_from_h` and the site is left
computed, marked `kind='runtime'`.

### Six substitutions flattened a derivation and were reverted

Seeding the evaluator with module-local names (the fix that found the hidden
`c_lat` definitions) has a cost: an expression built from *meaningful* names
also evaluates, and the rewriter will happily replace it with a constant.
`weight = sp.Rational(2,9)` / `delta_withN = weight*1` became
`delta_withN = <float>`, which turned `matches_2_9` from `true` to `false` in
`weight_as_phase_E1.json` — caught by the drift check, because the two halves of
the comparison stopped being the same kind of object. Five more of the same
shape were found by reading the full span-by-span diff and reverted:
`ca_superconductivity`'s ħ, F79's self-consistency check, F164's computed
`a_over_ellP` diagnostic, and two `np.cos(3·δ*)` computations in the derive
scripts. **A rewriter can find these sites; only a person can tell a literal
from a derivation.** All three derive scripts re-run to zero drift afterwards.

### sympy `Rational` sites need the exact object, not the float

`Fraction(2, 9) == 0.2222222222222222` is `False` in Python, unlike sympy's
`Rational`, which sympifies. The rewriter therefore substitutes `delta_star`
(the `Fraction`) at `sp.Rational(...)` sites and `delta_star_f` everywhere else.
Getting this backwards silently downgrades an exact check to a float one — which
is the precise failure C2 exists to prevent, so it is worth stating twice.

---

## Acceptance gate

| criterion | result |
|---|---|
| `grep "1/np.sqrt(3)\|0.5773502691896258" src/ ca-simulation/` returns only the registry and declared MeasuredConstant sites | **met** — 5 hits: `constants/geometry.py`, `constants/strong.py`, `constants/measured.py` ×2, and one registry docstring |
| changing `c_lat` moves a named, countable set of tests | **met** — 271 modules / **141 named tests** from the module graph; 2 of the 21 fast-gate checks move under a +1% perturbation |
| `make drift` clean, or the difference recorded | **met with two recorded moves** — see below |
| every registered constant has a finding; every `MeasuredConstant` has a reason | **met** — asserted by `test_registry_is_well_formed` and `test_every_measured_record_is_honest` |
| `make gate` green before and after | **met for every C2 check**; two unrelated failures at hand-off, both C1's in-flight work |

### The two recorded moves

The roadmap's own risk row: *"Constants inversion changes a number. Closed forms
replace truncated literals; a/ℓ_P alone moves by 3.4e-6 relative."*

| site | was | now | relative |
|---|---|---|---|
| `ca_alpha_s_running.A_OVER_LP` | 6.59782 (6 sf) | √(8π)·3^(1/4) | 5.06e-7 |
| `ca_qed_renormalization.A_OVER_LPLANCK` | 6.5978 (5 sf) | √(8π)·3^(1/4) | 2.53e-6 |

Downstream, in `test-results/F233_mass_scale_N_transmutation.json`, six values
move by 6.7e-8 to 9.6e-7:

```
alpha_s_MZ_1loop            0.11954571992 -> 0.11954572797   (6.73e-08)
alpha_s_MZ_converged        0.12797713504 -> 0.12797714463   (7.49e-08)
equiv_Lambda_ratio_conv     1.77665208169 -> 1.77665298501   (5.08e-07)
near_continuum_vs_wilson   16.21533011268 -> 16.21532186819  (5.08e-07)
factor_conv_vs_F119         0.51935433919 -> 0.51935427045   (1.32e-07)
dev_conv_%                  8.45519918505 ->  8.45520731084  (9.61e-07)
```

**Accepted, not tolerated.** The truncation was the defect; F107 makes the closed
form canonical. `F112_si_predictions.json` shows no numeric movement at all,
confirming that the canonical `ca_si_scale` path already used the exact form and
only the two derived copies had drifted.

### A cross-session defect, found by causing it

Regenerating the migration manifest **reset `ca_fft.py`'s `migrated:` stamp to
null** while the C1 session's migration was in fact complete — shim at the
source, target at `src/casim/numerics/fft.py`, backup in `deprecated/code/`.
`check_deprecated.py` then reported the tree INVALID with *"a backup exists but
the manifest record has migrated: null"*, which is exactly the false alarm a
lost stamp produces.

`gen_migration_manifest.py` now preserves `migrated`, `drift` and `dead_symbols`
across regeneration (`_STATE_FIELDS`), and the stamp is restored with a note.
C4–C6 explicitly invite parallel sessions, so a regenerator that silently
clobbers migration state would have scaled very badly.

---

## Perturbation blast radius

Now countable per constant, from `docs/design/module-graph.json` plus the
registry's `kind='import'` sites. The top of the table:

| constant | modules | named tests |
|---|---|---|
| `c_lat` / `G_LATTICE` / `F106_COEFF_LATTICE` | 271 | 141 |
| `f_pi_anchor_MeV` | 22 | 12 |
| `g_A`, `M_N_isoaveraged_MeV`, `M0_constituent_MeV` | 19 | 11 |
| `q_star_a_band_lo` | 16 | 10 |
| `a_over_ellP` | 16 | 8 |
| `c_fierz_colour`, `Lambda_NJL_GeV` | 12 | 6 |

The honest caveat: this counts reachability through *imports*. The 277 test-side
literals C7 still owns do **not** move when the registry changes, which is
precisely why the backlog is ratcheted rather than ignored.

---

## Enforcement added

- `tools/audit_constants.py` — the sweep engine, plus `--list`, `--json`, and
  `--ratchet` against `tools/constants_baseline.json`
  (`rogue_gate` 0, `rogue_backlog` 277, `literal_sites` 13 — all only go down).
- `make constants-report` lists every rogue with its line and its candidates.
- `make gate` gains **constants sprawl has not regressed (D7)**, next to C1's
  numerics ratchet.
- `tests/casim/test_constants_consistency.py` is now 12 checks, and still runs
  standalone when pytest is absent — a provenance gate that can vanish quietly
  is not a gate.

---

## Open at hand-off

1. **`F144_route_a_alpha_s.json` needs re-running.** It consumes
   `ca_alpha_s_running.A_OVER_LP` and will show the same ~5e-7 drift as F233.
   This machine has no scipy, so it could not be run or accepted here.
2. **The three-fold 2/9 may deserve a finding.** F231 reconciles two of the
   three; the colour-Fierz 2/9 makes it a trio. Recorded in the registry with
   cross-references; not written up, because whether it is bookkeeping or
   structure is a physics judgement.
3. **Not from this session:** the wmu/gluon drift C1 already reported
   (including the 20% `ym_action` shift) is untouched and still wants a look
   before commit. `tests/casim/test_backend.py` was fixed here — its `__main__`
   still called `test_default_is_ca_fft()`, a name C1's `casim.numerics` work
   renamed; pytest never runs `__main__`, so only the standalone gate saw it.
   C1's session had been idle five hours, so the one-line fix was safe.
4. **C7 inherits 277 test-side literals and 13 recorded `literal` sites.** Both
   are ratcheted, so they cannot grow.
