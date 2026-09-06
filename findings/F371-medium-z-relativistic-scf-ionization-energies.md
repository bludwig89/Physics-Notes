# F371 — Extending the relativistic SCF ionization-energy map from Z=1–20 (F208) to the full 3d series (Z=21–30, Sc–Zn): the Hartree/no-exchange underbinding persists at 33–48%, relativity stays sub-meV in the valence channel through Zn, and a second, previously unflagged limitation is found — F208's own fixed-N=900 uniform radial grid is not grid-converged above roughly Z~20, with the numerical uncertainty growing with Z until it rivals the physical error by Z=30

**Date:** 2026-09-05 - 04:10
**Status:** Confirmed, scope-narrowed — the 3d-series extension is a genuine result, but this finding also documents an honest, previously-undocumented numerical caveat (grid non-convergence) that F208's own Z=1–20 table inherits too, at a smaller but non-zero level.
**Checked:** 2026-09-05 — 11 PASS / 2 WEAKENS / 0 FAIL / 0 NOT RUN — **CONFIRMED-NARROWER**
**Module:** `src/casim/engine/core/manybody.py` (`electron_cloud_hartree`, `aufbau_configuration`, `_scalar_relativistic_shift_Ha` — unmodified; only new call-site parameters and diagnostic runs)
**Registry record:** `F371-medium-z-scf-ionization-energies` (`tests/registry/core.yaml`, kind `assertion`, tier `battery`)
**Results:** `test-results/F371_medium_z_ie_sweep.json`
**Claims topic:** `docs/design/session-claims.yaml`, session `cowork-g4-atomic-medium-z`
**Claim:** `CL182` (extended — see "Decision / scope" below; not a new card, per D12's narrowed-not-rewritten precedent)
**Cross-refs:** [[F208-relativistic-scf-ionization-energies]] (the Z=1–20 sweep and accuracy map this extends), [[F125-p5-hydrogen-atom-em-bound-state]] (the Dirac–Coulomb fine-structure operator both findings apply), [[F157-manybody-nuclei-and-electron-clouds]] (the Hartree SCF this and F208 both build on), [[F148-modular-element-assembler]], [[F195-blockspin-element-atom]] (the element-assembler consumers of the same Aufbau/Hartree structure)

---

## Summary

F208 built the relativistic (F125 Dirac–Coulomb) correction into the Hartree
SCF and swept first ionization energies Z=1–20, concluding the light-element
error is **exchange-correlation** (Hartree mean-field + Koopmans), not
relativity (valence shift <0.6 meV through Ca). This finding takes the
explicitly-named next step — extend past light elements — by running the
**unmodified** F208/F157 machinery over the entire first transition-metal row,
**Z=21–30 (Sc through Zn)**, including the requested target **Fe (Z=26)**, and
comparing against NIST-sourced first ionization energies.

Two things came out of doing this carefully:

1. **The physical conclusion extends cleanly.** Every element Sc–Zn is
   underbound by 33–48%, still overwhelmingly dominated by missing exchange
   (never relativity — the valence relativistic shift stays at 0.22–0.38 meV
   all the way to Zn, four orders of magnitude below the eV-scale SCF error).
   This is the same physics F208 found for H–Ca, extended by ten more
   elements including the one specifically asked for (Fe: −40.9%, IE 4.67 eV
   vs NIST 7.90 eV).
2. **A second, independent limitation was found and is reported rather than
   hidden.** The default F208 SCF settings (`mix=0.4, max_iter=60`) silently
   fail to converge from Ni (Z=28) onward — and the unconverged output is
   **not** a small perturbation of the true SCF answer (Zn's unconverged
   Koopmans IE is 7.37 eV; the properly converged value is 4.85 eV). Fixed
   by tightening the mixing (`mix=0.2, max_iter=150`; verified identical to
   the default on Z=21–27, where both converge). Separately, and more
   fundamentally: **the fixed-N=900 uniform radial grid itself is not
   grid-converged above roughly Z~20.** Because `r_max` grows only as
   `~12(1+√Z)` while the natural 1s core radius shrinks as `~1/Z`, the grid
   spacing relative to the core size gets systematically worse with Z. A
   spot check at N=1200 (vs. the N=900 used throughout) shifts the Fe
   valence IE by +10.8% and the Fe 1s core relativistic shift by +65.9%;
   at Zn the shifts are +12.6% and +81.4%. **This means F208's own Ca/K/Ar
   endpoint (Z=18–20) is also not grid-converged**, at a smaller (Ca: +6.9%
   valence, +41.2% core) but non-negligible level — a caveat F208 did not
   flag because it never went far enough in Z to need to.

Net: the Z=21–30 accuracy-map numbers below are genuine, honestly computed,
self-consistency-converged results at N=900 (matching F208's own grid choice
so the two tables are apples-to-apples) — but they carry an **unquantified
additional numerical uncertainty that grows with Z**, on top of the ~30–40%
physical (exchange) error, and that uncertainty is not yet closed. Reported
as a scope boundary, per the research protocol, rather than smoothed over.

## The Z=21–30 accuracy map (first ionization energy, eV, N=900 grid)

| Z | el | ground config (last subshell) | IE (SCF, rel.) | IE (NIST) | err | valence rel. shift | 1s core rel. shift |
|---|----|--------------------------------|---------------:|----------:|----:|--------------------:|--------------------:|
| 21 | Sc | 3d¹ | 4.204 | 6.5615 | −35.9 % | 0.225 meV | −6.450 eV |
| 22 | Ti | 3d² | 4.337 | 6.8281 | −36.5 % | 0.239 meV | −7.164 eV |
| 23 | V  | 3d³ | 4.442 | 6.7462 | −34.2 % | 0.251 meV | −7.865 eV |
| 24 | Cr | 3d⁴ | 4.530 | 6.7665 | −33.1 % | 0.261 meV | −8.544 eV |
| 25 | Mn | 3d⁵ | 4.605 | 7.43402 | −38.1 % | 0.270 meV | −9.194 eV |
| 26 | **Fe** | 3d⁶ | **4.669** | **7.9024** | **−40.9 %** | 0.277 meV | −9.813 eV |
| 27 | Co | 3d⁷ | 4.725 | 7.8810 | −40.1 % | 0.284 meV | −10.400 eV |
| 28 | Ni | 3d⁸ | 4.773 | 7.6398 | −37.5 % | 0.290 meV | −10.959 eV |
| 29 | Cu | 3d⁹ | 4.815 | 7.72638 | −37.7 % | 0.295 meV | −11.492 eV |
| 30 | Zn | 3d¹⁰ | 4.853 | 9.3942 | −48.3 % | 0.300 meV | −12.004 eV |

Mean \|err\| over Z=21–30: **38.2 %** (median 37.6 %, worst Zn at −48.3 %) —
worse than F208's Z=2–20 mean of 27.7 %, and combined Z=2–30 mean 31.3 %.
NIST values cross-checked against F208's own Na/Al table entries (exact
match) via the Wikipedia ionization-energies data page, itself sourced from
CRC/NIST; Fe additionally re-verified directly against the NIST ASD tool
(physics.nist.gov/cgi-bin/ASD/ie.pl): **7.9024 ± 0.0010 eV**, ground
configuration [Ar]3d⁶4s² — exact match to the value used here and to the
model's own computed configuration. The NIST uncertainty (±0.001 eV, ~0.01%)
is four orders of magnitude below every error reported in this finding, so it
never affects a conclusion.

**Configuration note:** strict Madelung (n+ℓ) filling gives the textbook
ground configuration for every element in this range **except** Cr and Cu,
whose real ground states (`4s¹3d⁵`, `4s¹3d¹⁰`) are stabilized by an
exchange-energy effect a Hartree-only mean field cannot represent — the
model reports `4s²3d⁴` / `4s²3d⁹` instead. This is not a new error mode: it
is the *same* missing-exchange limitation already responsible for the ~35%
IE underbinding, showing up a second way (in the configuration itself, not
just its energy) for exactly the two elements where real-world exchange
stabilization is strongest (half-filled and filled d-subshells).

## Why Ni/Cu/Zn need tighter SCF mixing than Sc–Co

At the default `mix=0.4, max_iter=60` (F208's own light-element setting):
Z=21–27 converge and reproduce the tightened-mixing values exactly (checked,
<0.001 eV). Z=28–30 do not converge in 60 iterations, and the unconverged
snapshot is badly wrong — not close to the converged answer:

| Z | el | default (unconverged) IE | converged IE (mix=0.2, iter=150) |
|---|----|---------------------------:|-----------------------------------:|
| 28 | Ni | 4.773 (coincidentally close) | 4.773 |
| 29 | Cu | 5.350 | 4.815 |
| 30 | Zn | 7.372 | 4.852 |

This is a numerical-parameter issue (density-mixing oscillation), not a new
physical regime — it is fixed by damping harder and iterating longer, and
the converged answer is what the table above reports. It is flagged here so
a future session (or an automated sweep) does not silently trust an
unconverged Ni/Cu/Zn Hartree solve, which for Cu/Zn is wrong by 10–52%.

## The deeper caveat: fixed-N=900 grid resolution degrades with Z

`electron_cloud_hartree` sets `r_max = max(40, 12(1+√Z))` and solves on a
**uniform** grid of `N` points, so the grid spacing `h = r_max/N` grows with
Z while the 1s orbital's natural radius shrinks as `~1/Z`. At fixed N=900
this is fine for light atoms (F208's own regime) but degrades as Z grows.
Checked directly by rerunning four representative Z (Na, Ca, Fe, Zn) at
N=1200 with everything else identical:

| Z | el | ΔIE (900→1200) | Δ(1s core shift) (900→1200) | err vs NIST at 900 | err vs NIST at 1200 |
|---|----|-----------------:|-------------------------------:|---------------------:|----------------------:|
| 11 | Na | +3.5 % | +13.2 % | −21.8 % | −19.1 % |
| 20 | Ca | +6.9 % | +41.2 % | −35.7 % | −31.2 % |
| 26 | Fe | +10.8 % | +65.9 % | −40.9 % | −34.5 % |
| 30 | Zn | +12.6 % | +81.4 % | −48.3 % | −41.8 % |

The sensitivity **grows monotonically with Z** and is not small by Fe/Zn:
the grid-refinement shift (order 10–13% on the valence IE) is now the same
order of magnitude as the physical exchange-correlation error this and F208
are trying to characterize. The qualitative physics conclusion is unchanged
at N=1200 (Zn is still underbound by 41.8%; relativity is still sub-meV:
0.380 meV at N=1200 vs. 0.300 meV at N=900) — but the **precise** error
percentages in the main table above should be read as N=900-grid values
with a real, unclosed numerical uncertainty on top, not as grid-converged
numbers. No attempt was made to reach grid convergence this session (would
need a non-uniform/log radial grid, or N well beyond what an SCF iteration
loop affords inside the sandbox's per-call time budget at this Z) — this is
named as concrete follow-on work, on the same footing as F208's own named
exchange-correlation gap.

## Falsifier

This finding's two live claims each have a named threshold that would kill them:

- **"Relativity stays negligible for the valence IE through Zn"** is falsified for any Z in
  this range if a grid-converged recomputation pushes the valence relativistic shift above
  ~1 meV (the current margin is 3–4 orders of magnitude: 0.22–0.38 meV observed at both grids
  checked). It is separately falsified if the missing-exchange explanation is wrong — i.e. if
  a grid-converged Hartree IE lands within ~10% of NIST for any Z=21–30 element (it does not,
  at either N=900 or N=1200: worst case Zn is 41.8–48.3% off).
- **"The grid-sensitivity caveat is real, not noise"** is falsified if a further grid
  refinement (N>1200) reverses or flattens the Na→Ca→Fe→Zn growth trend measured here. Not
  checked past N=1200 this session (named as follow-on work above).

## Decision / scope

- **Built & certified:** the unmodified F208/F157 machinery correctly
  produces the Madelung-Aufbau configuration and a converged (self-
  consistency, N=900) Hartree ionization energy for every element Z=21–30,
  including the requested Fe. The relativistic correction stays negligible
  for the valence channel through Zn and continues to grow in the 1s core,
  as F208 predicted it would for heavier atoms — though the core-shift
  Z-scaling itself is now shown to be partly a grid artifact (see above),
  so F208's own Ne→Ar Z⁴ slope measurement should not be extrapolated
  past where this finding checked it without a finer grid.
- **G4 rubric (atomic structure) promoted from "light elements only" to
  "H through Zn (Z=1–30), one full transition-metal row, with an honest
  two-axis accuracy map"**: physical error (Hartree/no-exchange, 15–48%,
  dominant and expected) and numerical error (fixed-grid resolution,
  growing with Z, unquantified past N=1200, newly discovered this session).
- **What would extend this further:** (1) a non-uniform (log-spaced or
  Chebyshev) radial grid, or a Richardson extrapolation in N, to separate
  the physical and numerical errors cleanly and push past Z=30 without an
  intractable per-call runtime; (2) exchange (Hartree–Fock) or a
  correlation functional — F208's own named next step, unchanged by
  anything here; (3) a genuinely self-consistent Dirac–Fock treatment,
  relevant once heavy/superheavy valence chemistry is in scope, still well
  beyond this range.
- **Not re-attacked:** F208's H–Ca physical conclusion (exchange, not
  relativity, is the light-element ceiling) — confirmed again, not redone.
  The light-element certifications (H/He/Li/C net-charge and Pauli-exclusion
  results) are untouched.

## Reviewed & corrected

**2026-09-05 - 04:35** — attack pass (inline, `.claude/commands/review-finding.md` on this
device-mounted repo predates the fix-in-place mechanism the loaded skill and CLAUDE.md both
describe, so followed the current skill's 13-point checklist inline, matching this session's
own precedent from the concurrent K9/K11 findings — no cold subagent available against a
device-mounted repo). **Verdict: CONFIRMED-NARROWER.** 11/13 attacks PASS outright (1
circularity, 3 exactness inflation, 4 tolerance shopping, 5 numerology, 7 perturbation —
structural check that C1/C6 can fail, verified by inspection, not a registry `--param` sweep
since this is battery tier with no control block, matching F208's own precedent — 8 test-record
integrity, 9 supersession hygiene — none of F125/F148/F157/F195/F208 appear in
`supersessions.yaml` — 10 scope creep, 11 prior art — no novelty claimed, standard Hartree/
Aufbau/Dirac-Coulomb methods — 13 falsifiability, after fix). Two **WEAKENS**, both already
substantially disclosed by the finding's own text and tightened here: (2/12 robustness) grid
convergence above N=900 was not established before the diagnostic added this session — fixed
as far as budget allowed (N=1200 spot-check at 4 Z, trend reported, explicitly NOT claimed
closed); (6 external data) the NIST comparison values came from a secondary compilation
(Wikipedia's ionization-energies data page) rather than the primary NIST ASD tool — fixed by
re-querying NIST ASD directly for Fe (7.9024 ± 0.0010 eV, exact match, ground config
[Ar]3d⁶4s² also an exact match) and noting the uncertainty is four orders of
magnitude below every reported error. Found: no circularity, no undercounted inputs, no
exactness inflation, no missing falsifier (fixed by adding the section above). Fixed: added
direct NIST citation for Fe with uncertainty; added the Falsifier section. Rejected: none.
Deferred: full grid convergence (N well past 1200, or a non-uniform radial grid) — named in
"Decision / scope" as follow-on work, same footing as F208's own exchange-correlation gap.
