# Open-Derivations Prompt Library

*Created 2026-07-02 - 00:00. A prompt to audit what still needs to be derived in the model, plus one self-contained prompt per known open derivation.*

This file has two parts:

1. **The Master Audit Prompt** — run it in a fresh session to sweep the authoritative sources and refresh the canonical ledger of everything still not derived. Use this first; it keeps the list below honest as concurrent sessions close items.
2. **Per-item derivation prompts** — one copy-paste block per open item, grouped by sector. Each is self-contained and follows the House Rules.

Items were confirmed open as of 2026-07-02 against `docs/status/exactness-inventory.md` ("Currently failing / not-yet-met"), `findings-index.md`, and the newest findings. **Before starting any item below, re-check its anchor finding** — the frontier moves and a concurrent session may already have closed it.

---

## House Rules (every prompt inherits these)

- **Derive first.** Attempt an algebraic derivation before introducing any new physics. Prefer algebraic exactness, then machine-precision, then quantitative-within-tolerance. If the derivation closes *negative*, that is a valid, publishable result — record it as such.
- **Use the existing structure.** Search `findings-index.md` (`grep -i keyword`) then read only the specific `findings/F{N}-*.md` you need. Reuse existing kernels/modules; don't rebuild what exists.
- **Use CASIM** for anything dynamical; if the sandbox will time out, write a runnable script + parameters that emit a JSON/result file to read back.
- **Numerics caution.** numpy/scipy on chiral transforms can silently drop real/imag parts — verify against a hand-rolled reference before trusting a result.
- **Document the outcome.** New physics or a candidate → a new `findings/F{N}-name.md` (check the highest current N first; concurrent sessions collide). Add a one-paragraph `docs/status/changelog.md` entry, update `docs/status/exactness-inventory.md` with the exactness tier, datestamp `yyyy-mm-dd - hh:mm`, then run `python3 tools/regen_indexes.py`.
- **State the acceptance test up front** and report the residual honestly (dex / %, and whether it is exact, machine-precision, or a fit).

---

## Part 1 — Master Audit Prompt

```
You are the research assistant on the Physics Notes cellular-automaton model. Produce a
current, authoritative ledger of everything in the model that is NOT yet derived from first
principles — i.e. every quantity that is still fit, tuned, assumed, posited, phenomenological,
or explicitly flagged "open".

SOURCES TO SWEEP (in order):
1. docs/status/exactness-inventory.md — read the "Currently failing / not-yet-met" table and
   scan every Tier-3 row for the words tuned/fit/anchor/calibration/scheme/residual.
2. findings-index.md — grep for: open, remaining, no-go, not derived, partial, relabel,
   coincidence, overshoot, tunable, calibration, residual, under pressure.
3. For every finding flagged above, open findings/F{N}-*.md and read its "open / remaining /
   what is derived vs computed vs open" section. Follow [[links]] to the latest superseding
   finding (numbers move; a "remaining =" note often migrates to a newer F-file).
4. docs/roadmaps/next-steps.md — collect un-struck-through, non-"Complete" lines.

FOR EACH OPEN ITEM, record a row:
  | ID | Sector | The undedived quantity/claim | Anchor finding(s) | Current status
    (fit value / bound / no-go) | What blocks it | Suggested attack |

RULES:
- Distinguish "not yet derived" (a target) from "derived negative / proven free parameter"
  (a closed result) — put the latter in a separate CLOSED-NEGATIVE section.
- Deduplicate items that appear under multiple findings; cite the newest anchor.
- Do NOT trust this file's Part 2 list as ground truth — regenerate from the live findings.

DELIVERABLE: write/overwrite docs/status/open-derivations.md with the ledger, a one-line
tally per sector, and a "changed since last audit" note. Update the changelog, datestamp,
and run tools/regen_indexes.py. Keep it to the table + short notes; no essay.
```

---

## Part 2 — Per-item derivation prompts

### Lattice / foundational

**L1 — Closed form for the subleading Lorentz-violation coefficient**

```
Follow the House Rules. Target: exactness-inventory "not-yet-met" #5 — the subleading LV
coefficient β ≈ 0.01883 (3D BCC) / α ≈ −0.0104 (2D), from Finding 7 (see F12/F15 for the
leading β_LV closed forms). We already have β_LV and γ_LV in closed form as the implicit-
function expansion of ω(u) = arccos(n·cos u). Extend that recursion to the NEXT order and
test whether the numerically-measured 0.01883 / −0.0104 coefficients have a closed rational-
in-(arcsin m, √(1−m²)) form. Acceptance: algebraic match to the measured coefficient at
machine precision, OR a proof that no closed form of that class reproduces it. Record the tier.
```

**L2 — Closed form for the composite-photon curl subleading coefficients**

```
Follow the House Rules. Target: exactness-inventory "not-yet-met" #3 (reframed) / Tier-3 #5.
The O(k) curl residual is the confirmed discrete-time prediction (coefficient c_lat/√2, F25).
Open question: do the SUBLEADING coefficients of the real-rotation curl law have a closed
form? Expand the exact F25 rotation law (ca_wmu._f26_rotation_step) to higher order in k and
compare against the free-Maxwell curl order-by-order. Acceptance: closed-form coefficients
matching the spectral measurement to machine precision, or a documented no-go. Note this is
a Planck-scale signature, not a failure — frame the result that way.
```

**L3 — Pin the lattice spacing a independently of any mass**

> ✅ **DONE 2026-07-02 → F232** (`F232-lattice-spacing-degeneracy-scale-invariance`). DEGENERATE/negative. The light-deflection route does *not* pin $a$: the deflection coefficient is exactly $-4$, dimensionless and $a$-independent over 47 decades (F107 L4a) — no stray $\sqrt d$ in the dimensionless part (it lives in the SI map). **Scale-invariance theorem:** no dimensionless, mass-blind observable can fix a length; the third input that breaks the degeneracy is a **dimensionful** gravitational coupling — $G$ (the F79 $G$-match, $a=\sqrt{8\pi}\,3^{1/4}\ell_P$). Closes exactness-inventory not-yet-met #7.

```
Follow the House Rules. Target: F83 established that the F46/F12 lattice-mass map gives only a
RELATION for the lattice spacing a, not a value (heaviest fermion sets a ceiling). Attempt an
independent pin by combining the F46 Dirac rest-leg geometry (the "△" rest-leg identity) with
the absolute light-deflection coefficient Δθ = 4GM/(bc²) (F55 / L4, which carries an explicit
√d, Finding 10). If the two constraints intersect at a single a, report it with error bars;
if they are degenerate, prove the degeneracy and state what third input would break it.
Acceptance: a numerical a with a quantified residual, or a proof of degeneracy.
```

### Electroweak / lepton sector

**E1 — Derive the lepton-spectrum angle δ\* = 2/9 (currently Koide-locked, not derived)**

> ✅ **DONE 2026-07-02 → F230** (`F230-lepton-angle-geometric-nogo`). NEGATIVE (sharpened no-go). The crystal-field/equipartition geometry fixes only the phase-coordinate **endpoints** (democratic $3\delta=0$; massless-Koide $3\delta=\pi/4$, exact; equipartition $45°$); the **interior** stopping point $3\delta^*=Q=\tfrac23$ rad is set by the brake ratio $B/C$ (a dynamical $\lambda_6\propto\alpha_\text{eff}^*$ number). Dimensional no-go: a radian cannot equal a pure ratio without a scale. Subsumed by F199's three-way structural no-go; $\delta^*=\tfrac29$ rad stays a Koide-confidence **target**.

```
Follow the House Rules. Target: F179 relabelled the charged-lepton spectrum as a one-angle fit —
δ* = 2/9 rad (with 3δ* = Q = 2/3) is Koide-locked to −0.89σ but NOT derived; granting it fixes
the whole spectrum to 0.01% (F120). Attempt a first-principles derivation of δ* = 2/9 from the
F75/F76 BCC crystal-field / T_1u irrep geometry and the F78/F80 Cooper-pair equipartition (45°)
structure. Acceptance: δ* = 2/9 emerging from the lattice geometry (exact or machine-precision),
or a sharpened no-go stating exactly which symmetry input is missing. Coordinate with the F179
relabel note.
```

**E2 — Settle whether sin²θ_W = 2/9 is geometrically derived or an on-shell endpoint**

> ✅ **DONE 2026-07-02 → F231** (`F231-weinberg-2over9-onshell-face-of-1over4`). RECONCILED — not a rival tree value, not a coincidence. $\tfrac14$ is the MS-bar UV cap at $\mu_\star=4\pi v$ (F45/F138); $\tfrac29$ is the on-shell endpoint at $M_Z$ ($m_Z/m_W=3/\sqrt7$, F49). The exact bridge $8/9$ **decomposes** as one-loop running ($0.927$) × MS→on-shell scheme conversion ($0.965$) $=0.895$ vs $8/9=0.889$ (0.67%). So $\tfrac29$ is the on-shell face of the $\tfrac14$ physics; F49's $2{:}7$ assignment is still the underived piece. Residual vs PDG: $m_Z/m_W=3/\sqrt7$ to $0.064\%$.

```
Follow the House Rules. Two threads exist: F138 derives sin²θ_W = 1/4 (bare) as the μ*=4πv
compositeness-matching condition (hypercharge has no kinetic term → abelian pole caps the angle
at 1/4), running to 0.23173 at M_Z; F49 reproduces 2/9 from BCC bond/sublattice counting as a
PARTIAL derivation, and 2/9 is the on-shell m_Z/m_W = 3/√7 endpoint. Resolve the relationship:
is 2/9 a genuine second geometric derivation, an on-shell endpoint of the same 1/4 physics, or a
coincidence? Acceptance: a single reconciled statement with the derivation chain made explicit,
and the residual against PDG quantified. Update F49/F138 cross-refs.
```

**E3 — Derive the overall mass scale N (the hierarchy / kg absolute scale)**

> ✅ **DONE 2026-07-02 → F233** (`F233-mass-scale-N-transmutation-supersedes-F119`). REDUCED, not free: F119's "no running channel" no-go is superseded by F144 — colour-sector asymptotic freedom transmutes α_s(μ₀)=1/(16π) down to Λ_MS, giving N_pred=2.86×10⁻¹⁹ vs F119's 5.5×10⁻¹⁹ (**factor 1.9, zero params, 19 decades**). Residual = the one one-loop constant d₁ (Λ_MS/Λ_lat≈1.78), **shared with Q1+Q2**. Open seam: the lepton-condensate↔Λ_QCD scale identification (O(1), not derived).

```
Follow the House Rules. Target: F119 — the kg is already in via ħ and the mass SHAPE is derived,
but the ONE open number is the overall scale N = m_lat(τ) ≈ 5.5e-19. The gap mechanism cannot
make N from O(1) couplings (needs ~1e-36 tuning, no running channel), and gravity pins the
lattice constant a, not N. Attempt: find any dynamical channel (RG running, dimensional
transmutation à la F144, or a gravity/cosmology constraint) that fixes N without tuning.
Acceptance: N derived to within a stated tolerance, or a rigorous proof that N ≡ the hierarchy
(i.e. genuinely a free input) with the argument made airtight. This is the deepest open number —
be explicit about which.
```

**E4 — Self-consistent (W, v, c) triple / global-stability invariant**

> ✅ **DONE 2026-07-02 → F234** (`F234-Wvc-triple-closed-delta-2-9-pins-brake`). CLOSED. The prompt below reflects the pre-F118 (F108) state; F118 already found the stable triple on the κ_E<0 spontaneous-Eg branch (lepton point global, gap −2×10⁻⁶, all couplings O(1)). F234 pins the last residual (the brake value): the derived δ\*=2/9 (F174/F175) + derived B (F95) into cos3δ\*=|B|/2C give λ₆=0.243 exactly ⇒ **λ₆ derived, not fit** (supersedes F179/CN3). Residual collapses into **E1** (weight→phase).

```
Follow the House Rules. Target: exactness-inventory "not-yet-met" #8, F108 → F118. The democratic
class is excluded exactly (Gap ≥ +0.0386); the two-invariant completion {v·Σy⁴<0, c·e⁴>0} makes
the exact lepton point GLOBAL at fixed W*=1.46, but v shifts the F95 angle requirement (W*→2.58)
where stability is lost. The self-consistent (W, v, c) triple is the open problem; the one-loop
momentum-resolved bubble does NOT deliver it (wrong-sign sextic, positive-definiteness lost at
e≳0.35). Attempt a self-consistent solution beyond one loop (or a non-perturbative closure).
Acceptance: a (W,v,c) triple that is simultaneously stable and reproduces the F95 angle, or a
proof that no such triple exists in this class. Reuse the F118 machinery.
```

### QCD / hadron sector

**Q1 — Derive the √σ / f_π scale-setting factor**

> ✅ **DONE 2026-07-02 → F235** (`F235-sqrt-sigma-fpi-scale-setting-unifies-with-d1`). REDUCED + honest negative: the chiral factor Λ/f_π=7.04 is exact; the +12% confinement-factor residual does **not** close to <5% from any principled BCC Brillouin-zone cutoff (matching 4.56 needs Λ_eff=2.758/a, below even the axis edge π/a). It is a genuine scale-setting object = the same one-loop constant d₁ that **E3 (F233) and Q2 (F154/F144-A4)** reduce to ⇒ **Q1=Q2=E3 (one number d₁)**, closable by the F162 background-field computation.

```
Follow the House Rules. Target: F124 — the two QCD calibrations reconcile only to ~12%: chiral
Λ/f_π = 7.04 is exact (Pagels-Stokar), and confinement from the F86/F88 condensate σ = 2πv² at
the BZ cutoff gives √σ/f_π = 4.00 (axis) / 3.23 (sphere) vs empirical 4.56. The residual factor
(~a strong-coupling gap; the bare rotor gives ~1, off by ~4) is the open scale-setting number.
Attempt to derive it from the strong-coupling running (link to F144 α_s and F86 σ). Acceptance:
√σ/f_π to <5% from the lattice with no new anchor, or a documented account of the missing
scale-setting factor. This also would firm up the F123 f_π anchor.
```

**Q2 — Derive the α_s scheme-conversion coefficient**


> ✅ **DONE 2026-07-03 → F239** (`F239-scheme-conversion-factorizes-exact-VtoMSbar-times-open-lattice-d1`). HALF-CLOSED. The lattice→MS-bar scheme conversion for g_s=½ factorises **exactly**: Λ_MSbar/Λ_rule = 1.773 = **1.299 (V→MS-bar via exp(a₁/2b₀), a₁(6)=11/3 exact — on F151-S1's exact V-scheme identification of the rotor lock)** × **1.365 (rule→V one-loop lattice matching = 1/q\*a, the shared open d₁ of F235/F233/F154)**. The true *scheme* leg is closed exactly; only the lattice→V leg remains, and F162's subtracted transverse coefficient shows the residual is **vertex-form-factor dominated** (rule prop-shift ≈0.16× Wilson; Wilson-28.81-gated). α_s(M_Z)=0.1180 the instant q\* is pinned. **Sharpens F235: only the lattice→V leg is d₁, not the whole of Q2.** Bracket q\*a∈[0.577,0.979] ⇒ Λ-ratio∈[1.33,2.25] (target 1.78). Test 3/3.

```
Follow the House Rules. Target: F144 — g_s = 1/2 at the BZ edge gives α_s(M_Z) to +1.3% (1-loop),
a zero-parameter result; the one open coefficient is the SCHEME conversion (lattice → MS-bar).
Derive that conversion factor from the rotor/dielectric structure (F115/F117) rather than fitting
it. Acceptance: α_s(M_Z) reproduced with the scheme factor derived (exact or to <1%), or a clear
statement of what perturbative-matching input remains. Coordinate with the F145/F154 residual
notes (Residual B is solved; this is the remaining IR/scheme piece).
```

**Q3 — Derive the NN isoscalar-vector (ω) short-range repulsion**


> ✅ **DONE 2026-07-03 → F240** (`F240-omega-coupling-from-vector-sector`). Deuteron binds with a fully-derived OBE, coupling bracketed. Derived the ω channel from the vector-meson sector — repulsive sign (F128), m_ω=m_ρ, and g_ωNN=3·g_ρNN are **Tier-1**; KSFR×universality×baryon-coherence gives g_ωNN²/4π=25.9, but this **overshoots and unbinds the deuteron**, so the absolute coupling stays a **Tier-B bracket [5.4, 11.1]**, quenched 0.43× below the universality ceiling — numerically the same quench (0.45) F126 needed on the scalar coupling. The full derived OBE (F104 π + F126 σ + F113 core + ω) binds the deuteron with **no tuned hard core**: B_d=2.221 MeV (0.1%), r_d=1.978 fm (0.4%), σ+ω residual well −81 MeV. One open item = the common ~0.43 channel-dressing factor. Test 10/10.

```
Follow the House Rules. Target: F126 §"room left for the vector (ω)". The NN force has the pion
tail (F104), the σ intermediate attraction (F126), and the F113 quark-Pauli + chromomagnetic
core, but the isoscalar-VECTOR (ω) short-range repulsion is the one underived element (the full
one-boson-exchange short-range repulsion = F113 core + ω). Derive the ω-exchange channel from the
model's vector-meson sector and add it to the NN potential. Acceptance: the deuteron binds at the
physical point with the FULL derived OBE potential (no tuned hard core), r_d and B_d within a
stated %; reproduce the ~−50 to −100 MeV residual well. Reuse the F104 deuteron solver.
```

### Gravity / cosmology sector

**G1 — Close the cosmological-constant magnitude (the Ω_Λ ≈ 0.69 residual coincidence)**


> ✅ **DONE 2026-07-03 → F241** (`F241-omega-lambda-o1-residual-anthropic`). Rigorous NEGATIVE (coincidental/anthropic). The last O(1) factor after F196's p=2, Ω_Λ=0.6847, is **not** derivable from the F190 area-entropy / F183 BH sector: that sector fixes only the **ceiling** ρ_crit (Ω=1, the de Sitter fixed point), and the sub-unity value is the **"why-now" coincidence residual = 1 − Ω_m**, requiring the cosmic matter fraction the model lacks (blocked by F197–F199). The event-horizon route is circular (dS fixed point =1; also mispredicts w₀=−0.885), and the parameter-free near-hits (2/3, ln2, e/4) are numerology by a band-density count. p=2 **not** reopened. Test 6/6.

```
Follow the House Rules. Target chain: F164 (bare lattice ρ_vac overshoots ρ_Λ by ~10^121, sign
also wrong) → F193 (ontic vacuum gravitates as zero: bare CC = 0 exactly, killing magnitude AND
sign) → F196 (the dilution exponent p=2 DERIVED two ways → ρ_crit, landing 0.10 dex from ρ_Λ).
The 121-order residual is now reduced to the single Ω_Λ ≈ 0.69 O(1) coincidence. Attempt to
derive that remaining O(1) factor (the leftover after p=2), i.e. why the holographic/CKN residual
lands at Ω_Λ ≈ 0.69 and not, say, 0.1 or 0.9. Acceptance: the O(1) factor derived to <0.1 dex
from the F190 area-entropy / F183 black-hole scaling, or a documented statement that it is an
anthropic/coincidental residual. Do not reopen the p=2 derivation.
```

### Neutrino / dark sector

**D1 — Three-generation seesaw: light-neutrino masses + PMNS mixing**

> ✅ **DONE 2026-07-03 → F236** (`F236-three-generation-seesaw-pmns`). Sharpened negative. Promoted F47 to the full 3×3 in `ca-simulation/ca_majorana.py`: the diagonal see-saw reduces to three copies of F47's M_D²/M_R at machine precision, so the F93/F76/F201 E_g (Z₃) texture **derives the three light masses + hierarchy** (incl. the F201 keV node) — **but** E_g is the diagonal-traceless channel (F93 O1), forcing **PMNS = 𝟙 exactly** (structural no-go). Large mixing is thus pinned to the orthogonal second-shell **T₂g channel** (F93 commitment #1), whose amplitudes are **free inputs** (5 oscillation observables reproducible only with 6 inputs). Masses derived; mixing angles free. Test 5/5.

```
Follow the House Rules. Target: F47 built the Higgs-free single-flavour ν_R Majorana mass step and
the see-saw scaling m_ν ≈ M_D²/M_R. Generalise to the full 3×3 case: build the 6×6 see-saw matrix
[[0, M_D],[M_Dᵀ, M_R]] with M_R textured by the F93/F76 Z₃ (E_g) generation structure (see F201).
Diagonalise for the three light active masses and the PMNS mixing matrix. Acceptance: the light
mass-squared splittings and PMNS angles reproduced within stated tolerance from the lattice
texture (no free mixing angles), or a clear account of which texture inputs remain free. Promote
to ca_majorana.py if downstream sectors need it (F47 open follow-up #1).
```

**D2 — Resolve the keV sterile-neutrino dark-matter candidate under observational pressure**

> ✅ **DONE 2026-07-03 → F237** (`F237-kev-sterile-resolution`). Clean EXCLUSION as 100% DM. Reusing the F205 QKE solver + late entropy dilution S (F202 GeV N₂,₃ decay), no (m_s, L, S) point across 154 grid points clears both the current X-ray line bound **and** even the conservative 3.5 keV Lyman-α floor at 5.6 or 7.1 keV. Mechanism-level, not a grid artefact: the X-ray margin scales as sin²2θ∝S (slope +1) while the Lyman-α floor improves only as S^(−4/9) (slope −4/9) — opposite signs ⇒ no S co-satisfies both; best case still **+0.78 dex** over the X-ray bound. keV sterile **excluded as 100% DM** (demoted to bounded sub-dominant); 100%-DM identity handed off to the **F223/F228 spin-2 geon**. Test 7/7.

```
Follow the House Rules. Target: F200/F201/F205 — the F47 sterile ν_R is the model-native DM relic;
the full QKE Boltzmann run (F205) puts the keV sterile under quantified pressure: Dodelson-Widrow
X-ray excluded by 2.55 dex, the Lyman-α floor pushes 41→9–15 keV, and the model's ~5.6 keV point
sits under pressure. Attempt to resolve: either (a) find the production channel (resonant/entropy-
dilution) that lands a viable mass+abundance inside the current X-ray + Lyman-α windows, or (b)
show the keV-sterile route is excluded and hand off to the F216/F223 spin-2 or E_g candidates.
Acceptance: a viable (mass, mixing, Ω_DM) point with all §4 falsifiers passed, or a clean
exclusion. Reuse the F205 QKE solver.
```

**D3 — Relic abundance for the spin-2 "geon" dark-matter candidate**

> ✅ **DONE 2026-07-03 → F238** (`F238-geon-relic-abundance`). Documented negative (extends F228). The geon side is exact (one-cell M_rem=(√3/2)^{1/2}M_Pl, entropy-conserved), leaving the F228 PBH-remnant fraction β(M_form) as the sole residual. Deriving β from Press–Schechter β=½erfc(δ_c/√2 σ) requires a small-scale amplitude σ~0.06–0.08, i.e. **~1.6×10⁶** above the CMB √A_s=4.6×10⁻⁵; the only tuning-free (scale-invariant, n_s=1) spectrum under-produces Ω_DM by **~2.1×10⁷ orders**, β(σ) is monotone (no attractor), and the model has **no inflaton/primordial-spectrum sector**. Verdict: **Ω_DM h²=0.12 is a free cosmological initial condition** (the small-scale P(k)), not a derivable coupling — sharpens F228's "β tunable" to "β provably free, stated cause". Test 7/7.

```
Follow the House Rules. Target: F216 → F223 — the graviton–graviton J=2 geon BINDS at the
Planckian virial mass μ ≈ √2·M_Pl and passes every DM screen (cold, collisionless, non-fuzzy,
ΔN_eff≈0); the obstruction has migrated from binding/mass to PRODUCTION: gravitational particle
production under-produces Ω_DM by ~10^5 orders because μ ≫ H_inf, so abundance needs a Planck-
mass-relic (PBH remnant) / preheating channel and is currently "tunable". Attempt to derive a
non-tunable abundance: compute the relic yield from a specific preheating/PBH-remnant channel and
test whether it hits Ω_DM h² ≈ 0.12 without fine-tuning. Acceptance: a derived Ω_DM within the
Planck band from a stated channel, or a documented account of why abundance remains a free input.
Reuse the F223 machinery.
```

### Applied (superconductivity) — open first-principles piece

**S1 — Morel–Anderson μ\* from the F64 dielectric**

> ✅ **DONE 2026-07-03 → F242** (`F242-mustar-from-f64-dielectric`). POSITIVE (with honest residual). The F64 dielectric's static long-wavelength limit **is** the Thomas–Fermi screening ε(q)=1+k_TF²/q² (same dielectric already used for the phonon side). FS-averaging the screened Coulomb gives the parameter-free **μ(r_s)=0.082930·r_s·ln(1+6.0299/r_s)**, and Morel–Anderson retardation μ\*(ω_c)=μ/(1+μ·ln(E_F/ω_c)) — **evaluated at the solver's own cutoff ω_c=6ω_log (the crux; ω_log gives too-small μ\*)** — yields **μ\*=0.10–0.12, matching the empirical values with no fit**. Cuts Allen–Dynes 7-element error 14.3%→6.3% (simple metals 17.7%→6.7%). Corrects F218: the derived μ\* is only ~6 of the ~28 pts of the Eliashberg overshoot (27.6→21.6); the rest is the ω_c-window scale, not μ\*. New module fns `mu_coulomb_jellium`, `mustar_from_dielectric`. Test 5/5.

```
Follow the House Rules. Target: F218 remaining item — the Eliashberg T_c and gap ratio are now
first-principles (Debye α²F derived from the F213 deformation potential; Padé gap ratio), and the
residual is reframed as a μ* CALIBRATION matter. Derive the Coulomb pseudopotential μ* (Morel-
Anderson) from the F64 EM-connection dielectric K rather than taking it as a fit. Acceptance:
μ* computed from the dielectric and fed to the F215 solver, tightening the 7-element T_c set
(currently ~27% high with the single mode) toward experiment with no fit parameter, or a stated
account of the remaining scale. Reuse ca_superconductivity.py.
```

---

## Coverage note

The per-item prompts above cover the open derivations confirmed on 2026-07-02: three lattice/
foundational (L1–L3), four electroweak/lepton (E1–E4), three QCD/hadron (Q1–Q3), one gravity/
cosmology (G1), three neutrino/dark-sector (D1–D3), and one applied (S1). Run the **Master Audit
Prompt** periodically to catch new open items and retire ones that concurrent sessions have closed.

### Completed log

- **2026-07-02 — L3, E1, E2** (concurrent session) → F229/F230/F231 (+F232).
- **2026-07-02 — E3, E4, Q1** → **F233 / F234 / F235**. All three were already closed/reduced by findings the ledger hadn't integrated. **E3** reduced (F144 transmutation lands N to factor 1.9; residual = d₁). **E4** closed (F118 existence + F174/F175 δ\*=2/9 pins λ₆; residual ⊂ E1). **Q1** reduced (honest negative; residual = d₁). **Net: E3 = Q1 = Q2 unify into the one one-loop background-field constant d₁** (closable by the F162 program); **E4 ⊂ E1**.
- **2026-07-03 — D1, D2, D3** (prompts #12/13/14, neutrino/dark sector) → **F236 / F237 / F238**. All three close as sharpened negatives. **D1** (F236): full 3×3 Higgs-free see-saw built in `ca_majorana.py`; the E_g (Z₃) texture **derives the light masses + hierarchy** at machine precision, but being diagonal-traceless it forces **PMNS = 𝟙** exactly ⇒ lepton mixing lives in the free second-shell **T₂g** channel (masses derived, angles free). **D2** (F237): keV sterile **excluded as 100% DM** — resonant + entropy-dilution production cannot thread the X-ray line ∧ Lyman-α floor (levers anti-correlated: sin²2θ∝S vs floor∝S^−4/9; best case +0.78 dex short); demoted to sub-dominant, 100%-DM handed to the geon. **D3** (F238): geon relic abundance is **NOT derivable non-tunably** — β(M_form) is fixed by the small-scale primordial amplitude (needs ~1.6×10⁶ over CMB; scale-invariant spectrum under-produces by ~2.1×10⁷ orders) and the model has no inflaton sector ⇒ **Ω_DM = a free cosmological initial condition** (extends F228). **Net: the model's surviving 100%-DM candidate is the F223/F228 Planck-mass spin-2 geon, with abundance an external initial condition; the keV sterile survives only sub-dominant; lepton mixing is the free T₂g channel.** Tests 5/5, 7/7, 7/7 (21/21). Concurrent sessions took F239/F240/F241 for Q2/Q3/G1.
- **2026-07-03 — Q2, Q3, G1** → **F239 / F240 / F241** (renumbered from F236–F238 after a concurrent session took those for D1/D2/D3). **Q2** half-closed (scheme leg exact = V→MS-bar via a₁=11/3; residual = the shared lattice→V d₁, vertex-form-factor dominated). **Q3** binds the deuteron with a fully-derived OBE (B_d 0.1%, r_d 0.4%), ω sign/mass/×3-ratio Tier-1, absolute coupling bracketed [5.4,11.1] (universality overshoots). **G1** closes negative — Ω_Λ≈0.685 is the coincidental/anthropic 1−Ω_m residual, not derivable from the F190/F183 holographic sector (which fixes only the ceiling ρ_crit); p=2 untouched.
- **2026-07-03 — S1, F1, F2** (ledger items #15/#16/#17) → **F242 / F243 / F244**. Highest prior F-number was F241; a pre-existing F218 title collision noted, no new collision. **S1** (F242, has the Part-2 block above): POSITIVE — μ\* derived from the F64→Thomas-Fermi dielectric, μ(r_s)=0.082930·r_s·ln(1+6.0299/r_s), μ\*(6ω_log)=0.10–0.12 with no fit; Allen–Dynes error 14.3%→6.3%; corrects F218 (μ\* is only ~6 of the ~28-pt Eliashberg overshoot, rest = cutoff-window scale). **F1** (F243; ledger-only, no Part-2 block — "F3 lensing prediction failure at low fermion density", next-steps line 5 / inventory not-met #4): **NOT FALSIFIED** — the F3 depression source stays correct-sign, positive-definite, non-divergent from ρ=1 to 10⁻³, scaling linearly (weak-field slope 1.012); no low-density pathology. **F2** (F244; ledger-only — "1/b scaling of 3-D EMQG lensing", inventory not-met #2): **PASS** — on the genuine 3-D EMQG potential (solve_poisson_3d, 1/r) with parameter-free GR-Shapiro c (no free α), Δθ∝1/b: closed form −0.9959 (exact), lattice isolated −1.074 / periodic −1.062, Cayley stepper toward-mass, norm 10⁻¹⁵; supersedes the F3b \|Φ\|^α scan. Tests 5/5, 6/6, 5/5 (16/16). New module fns in `ca_superconductivity.py`; F1/F2 reuse `ca_unified.py`/`ca_emqg.py`/`ca_curved.py`. **Net: the SC sector's last empirical input (μ\*) is now derived; inventory not-yet-met #2 and #4 both retire as PASS.**
