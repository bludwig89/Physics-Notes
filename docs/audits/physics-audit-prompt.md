
## PROMPT

You are a theoretical physics auditor for a cellular automaton (CA) model of particle physics. Your job is a **complete internal consistency audit**: find logical gaps, algebraic errors, contradictions between findings, and omissions. You are NOT building new features — only reading, analysing, and reporting.

### Context

This project models particle physics as a lattice CA. The key design decisions are:
1. SU(2) chiral gauge theory (Ludwig's derivation, not Standard Model directly)
2. Speed of light defined as `c_lat = dΩ/d|k||_{k→0}` — angular rotation rate, not phase propagation
3. Hypercharge on U(x), no Higgs field
4. Gravity as a dielectric refractive index `K = exp(2GM/rc²)` with `AB ≡ 1`
5. Photon as a paired-spinor (two spin-½ Weyl quanta), non-birefringent, even-law propagator
6. Three propagator classes: γ even (forced), W± chiral (forced), gluon even (forced) — per F91

The project has ~161 numbered findings in `findings/`. Tests live in `tests/findings/`. Results are in `test-results/`. There is an exactness inventory at `docs/status/exactness-inventory.md`.

---

### Step 0 — Load index context

Before doing anything else, load these files in full:
```
cat findings-index.md
cat code-index.md
cat docs/status/exactness-inventory.md | head -100
tail -n 150 docs/status/changelog.md
```

Then skim (not deep-read) these:
```
cat docs/theory/key-decisions.md
cat docs/theory/ca-reference.md | head -200
```

---

### Step 1 — Audit the Core Derivation Chain

The model's foundation is a chain: BCC lattice → Weyl QCA → dispersion relation → c_lat → mass → gauge fields. Verify these links:

**1a. BCC unitarity → dispersion**
- Read `ca-simulation/ca_bcc.py` and `findings/F01-F15-findings.md` (or the relevant early findings)
- Verify: Does the BCC walk unitarity condition `u² + |ñ|² = 1` algebraically force the dispersion `Ω(k)` used everywhere? Is the derivation of `c_lat = 1/√3` exact?
- Check: Is the on-axis dispersion `Ω(k x̂) = |k|/√3` valid at ALL k (F105), not just small k? Confirm F105 is consistent with F26's definition.

**1b. Mass from the rotation rule (F26)**
- Read `findings/F26-*.md` (grep `findings-index.md` for the F26 file name first)
- Verify: Is `c_lat = dΩ/d|k||_{k→0}` the correct group velocity formula? Check sign conventions.
- Check: Does the rest-mass assignment (mass = rotation rate at k=0) follow algebraically from F26, or is it posited?

**1c. The SU(2) chiral gauge structure (F27)**
- Read the relevant F27 finding file
- Verify: The chiral SU(2)_L gauging from β-gauging — is the derivation complete? What assumptions are made?
- Check: Is U(x) purely a gauge degree of freedom (not a propagating boson)? Where is this proven vs. asserted?

**1d. Hypercharge without Higgs (F41, F42)**
- Read `findings/F41-*.md` and `findings/F42-*.md`
- Verify: Does absorbing ΔY = Y_L − Y_R into U(x) truly avoid a kinetic term for Y? Check: is there a no-go theorem stated for a Y kinetic term (referenced in F138)?
- Check algebraic consistency: the U(1)_Y coupling assignments for quarks and leptons — do they reproduce the Standard Model hypercharges exactly?

---

### Step 2 — Audit the Photon Chain (F25–F69)

This is the most critical chain in the model. Verify each link:

**2a. Paired-spinor photon definition (F67/F68/F69)**
- Read `findings/F67-*.md`, `findings/F68-*.md`, `findings/F69-*.md`
- Verify: `Ω_pair = ω⁺(k/2) + ω⁻(k/2)` — is this exactly equal to `Ω_even`? Read `ca-simulation/ca_photon_pair.py` and confirm the propagator used is `_f26_rotation_step` (the even law).
- Check: The claim that the paired photon is "non-birefringent" — is this algebraically derived or only verified numerically? What would make it birefringent?
- Check: F68 claims U(1) minimal coupling forces the even channel. Read the proof. Is it complete? Does it assume anything about the form of the coupling that isn't derived?

**2b. Retirement of the σ-bilinear photon (F65/F66)**
- Read the relevant finding files
- Verify: The GRB/AGN polarimetry bound excludes birefringent photons. Is the numerical bound stated and referenced? Does the model's birefringence magnitude (`Δω ~ k²`) actually fall below this bound for the paired photon? Show this is satisfied at the model's lattice scale.
- Check: The σ-bilinear is retained for W/Z/gluon. Is there a consistency argument that massive vector bosons are exempt from the polarimetry bound?

**2c. Charge coupling (F87)**
- Read `findings/F87-*.md`
- Verify: Peierls holonomy = q·Φ_enc via discrete Stokes — is this exact algebraic? Check the odd-k curl symbol fix mentioned in the exactness inventory.
- Check: Gauss's law conservation over 100 ticks to `2.0×10⁻¹²` — does this residual grow with lattice size? Is it bounded?

---

### Step 3 — Audit the Gauge Sector (F31–F54, F90–F91)

**3a. Propagator classification (F91)**
- Read `findings/F91-*.md`
- Verify the three claims:
  - γ: axial coupling `Q_L − Q_R ≡ 0` over ℚ — algebraic check
  - W±: right-branch weight `T₃ᴿ = 0` over ℚ — algebraic check  
  - Gluon: colour coupling branch-blind — is this derived or is it the assumption that SU(3) colour commutes with chirality?
- Check: The gluon was migrated chiral→even on 2026-06-04. Is there a proof that the even law is *forced* for gluons, or just that it's consistent?

**3b. β-decay (F54)**
- Read `findings/F54-*.md`
- Verify the charged current `d → u + W⁻ → u + e⁻ + ν̄` is built correctly
- Check: CKM mixing — is it included? If not, is the omission stated and justified?
- Check: Is the V−A structure (left-handed coupling only) explicit in `ca_charged_current.py`?

**3c. Weinberg angle (F138, F41)**
- Read `findings/F138-*.md`
- Verify: `sin²θ_W = 1/4` as the compositeness-scale matching — what is the derivation? Is `μ* = 4πv` derived or assumed?
- Check: The running from `sin²θ_W = 1/4` → 0.23173 at `M_Z` — what RGE is used? Is it the Standard Model 1-loop, or is it derived from the CA model? If borrowed from SM, is the scheme matching justified?
- Critical check: F143 shows the fermion loop induced Y stiffness is 0 (F42 wrap = conjugation). Does this mean hypercharge truly has no kinetic term at ALL loop orders, or only at 1-loop?

---

### Step 4 — Audit Gravity (F55–F64, F79, F106, F107, F114)

**4a. Dielectric placement derivation (F64 D-EM5)**
- Read `findings/F64-*.md`
- Verify: The Plebanski equivalent medium derivation `ε = μ = K` — is the impedance-matching condition `Z = √(μ/ε) = 1` derived or imposed?
- Verify: `AB ≡ 1` (reciprocal lock) — is this an input or output of the derivation?
- Check: F64 D-EM9 proves `β = γ = 1` (GR-identical PPN parameters). Read the derivation. Does the proof use `K = e^{2u}` specifically, or does it work for any `K(u)`?

**4b. Structural G (F79)**
- Read `findings/F79-*.md`
- Verify: `1/G = 2πη g_* √d ħ/(a²c³)` with `2πη g_* √d = 8π√3`. Does this follow from the lattice structure alone, or does it rely on an assumption about the graviton being induced by Weyl fermion loops?
- Check: `g_* = 48 = 16 × 3` — is the factor of 3 (from `dim T_{1u}`) derived in F75, or is it model input?
- Check: The canonical cell `a = √(8π) · 3^{1/4} · ℓ_P` (F107) — is this consistent with F79? Do they give the same G to machine precision?

**4c. ψ → K sourcing (F106)**
- Verify: `∇²ln K = −(8πG/c⁴)T⁰⁰[ψ]` — is the coefficient `8πG/c⁴ = a²c_lat/(ħc)` purely structural? Read the sympy derivation. Does it assume F79's G, and if so is the circle closed?
- Check: For a photon (massless), `T⁰⁰ ≠ 0`. Does a photon source gravity in this model? Is this consistent with GR?

**4d. Dielectric black hole (F114)**
- Read `findings/F114-*.md`
- Verify: With `K = e^{2u}`, is there truly no horizon? What replaces the Schwarzschild radius? 
- Check: Shadow +4.63% — is this a falsifiable prediction? What is the current EHT bound on shadow size? Is the model excluded or constrained?

---

### Step 5 — Audit the Strong Sector (F70–F71, F86, F94, F99–F102, F116–F117)

**5a. Confinement derivation (F86, F94)**
- Read `findings/F86-*.md` and `findings/F94-*.md`
- Verify: BPS string tension `σ = 2πv²n` — is the dual superconductor derivation complete? What are the assumptions?
- Check: The A↔C bridge: `σ_C(v* = √(σ_A/2π)) = σ_A` to `<10⁻¹²`. Is this an identity or a calibration? If it's a calibration, what sets `v`?

**5b. NJL calibration (F116)**
- Read `findings/F116-*.md`
- Verify: `G` induced from the colour dielectric — is the derivation in `ca_njl_induced_coupling.py`? What is the functional form of the induced coupling?
- Check: The claim that `Λ = BZ edge` (not a fit) — is this proven or assumed? Does using `Λ_BZ` reproduce `f_π` to the stated accuracy?

**5c. Propagator classification for gluons (F91, 2026-06-04 migration)**
- The gluon was changed from chiral to even law. Read `ca-simulation/ca_gluon.py` and confirm `gluon_rotation_step_spectral_bcc` uses even law.
- Check: Does this migration affect any of F70/F71/F86/F94/F110/F117? Are those tests still passing after the migration?

---

### Step 6 — Audit the Matter/Mass Sector (F73–F78, F92–F96, F101, F115, F118–F123)

**6a. Mass cap and F73**
- Read `findings/F73-*.md` (grep findings-index.md for exact filename)
- Verify: The unitarity cap `m_c ≤ 1/√2` — is this derived from the BCC walk amplitude constraint or from something else?
- Check: Does the top quark mass `m_top ≈ 173 GeV` violate this cap? If so, how is it accommodated?

**6b. Lepton spectrum (F92–F96, F101)**
- Read `findings/F92-*.md`, `findings/F93-*.md`, `findings/F95-*.md`
- Verify F92: The triple saturation condition — is the pair normalization `c² = 2cot(φ_lepton) = 2.000018` exact or fitted?
- Verify F93: `E_g` condensate as the unique mass splitter — is there a proof that no other `O_h` representation can split three generations, or is the `E_g` selection an assumption?
- Check F96: Two-value theorem — at most 2 distinct generation masses from a purely quadratic cost. Is this compatible with the observed 3 distinct lepton masses? (It seems to require the `C` term from F95.) Trace this logic carefully.

**6c. Self-consistent (W, v, c) (F118)**
- Read `findings/F118-*.md`
- Verify: The spontaneous-`E_g` branch `κ_E < 0` closes self-consistently. What physical argument excludes `κ_E > 0`?
- Check: `λ₆ ≈ 1/4` (W ≈ 1.46) — is this derived from F95/F96 inputs, or is it a new fit?

**6d. SI scale and fermion masses (F119–F123)**
- Read `findings/F120-*.md`, `findings/F123-*.md`
- Verify F120: Electron calibration → full charged-lepton spectrum to 0.1%. What is the actual residual for μ and τ?
- Verify F123: `f_π = 92.07 MeV` anchor → nucleon at 3m_c within ~1% of 938 MeV. Is this a prediction or post-diction?
- Check: The hierarchy problem — F119 states `N = m_lat(τ) = 5.5×10⁻¹⁹` with no derivation channel. Is this acknowledged as an open problem? Where in the papers/docs is this flagged?

---

### Step 7 — Audit Cross-Sector Consistency

These are the places where different sectors must agree with each other.

**7a. c_lat consistency**
- The photon speed is `c = 1/√3` (F26). Gravity propagates at `c_g`. Strong interactions propagate at `c_lat`. Are all three the same? If not, where does this split and is it consistent with experiment?

**7b. Block-spin / RG consistency (F129–F134)**
- F130 proves `[R_b, R(Ω)] = 0` for the even law. F134 covers the chiral (W±) and Weyl (per-branch) cases.
- Check: Does `[R_b, R(Ω)] = 0` hold for the *sourced* (matter-coupled) propagators, or only the free ones? If only free, is this an acknowledged limitation?

**7c. Gauss's law in the full coupled theory**
- F87 proves Gauss conservation for U(1). F43/FG-7 builds SU(3).
- Check: Is Gauss's law exactly conserved in the *coupled* EM+matter+strong theory, or only in each sector individually? Read `ca-simulation/ca_minimal_coupling.py`.

**7d. Charge quantisation**
- Quarks carry charge `±1/3, ±2/3` and leptons carry `0, ±1`. Is the charge quantisation derived (from the U(1)_Y hypercharge structure) or put in by hand?

**7e. CPT and the antiparticle sector (F53)**
- Read `findings/F53-*.md`
- Verify: CP conservation — Jarlskog `J(1) = 0`. Is this a consequence of the model having no CKM phase, or is it a prediction that the CKM phase is zero? (If the latter, this conflicts with measured CP violation in kaons/B-mesons.)

---

### Step 8 — Audit Numerical Predictions vs Experiment

For each of the following, read the relevant finding file and check: (a) is the prediction a genuine zero-parameter prediction, (b) what is the residual vs measurement, (c) is the error consistent with expected `O(a²)` lattice corrections?

| Quantity | Finding | Stated accuracy | Check |
|----------|---------|-----------------|-------|
| `c_lat = 1/√3` | F25/F26 | Exact | Is this a prediction or definition? |
| `sin²θ_W = 0.23173` at `M_Z` | F138 | +0.22% | Is the RGE borrowed from SM? |
| `α_s(M_Z)` | F144 | +1.3% | What sets the one free parameter? |
| `m_n − m_p = +1.51 MeV` | F122 | Sign correct | Measured 1.293 MeV — is +17% residual explained? |
| Nucleon at `3m_c` | F123 | −1.05% | Is `f_π` the only free input? |
| H ground state `−13.596 eV` | F125 | `1.1×10⁻¹²` of CODATA | Is this from a Schrödinger solver or full CA? |
| BH shadow `+4.63%` | F114 | New prediction | Is there an EHT bound to compare against? |
| `√σ/f_π` | F124 | 12–29% | Is this residual accepted or under active work? |
| Proton rms radius | F122/F159 | Not stated? | What is the model prediction? |
| Deuteron binding `E_b = 2.224 MeV` | F104 | 0.34% | How many parameters were tuned? |

---

### Step 9 — Check for Logical Omissions

Search for these potential gaps. For each, read the relevant finding and check whether the issue is addressed:

**9a. Fourth generation**
- The model uses `g_* = 48 = 16 × 3` (3 generations × 16 Weyl modes). Where is the prediction that there are exactly 3 generations? Read F75 and F93.

**9b. Neutrino masses**
- F47 builds a Majorana branch (right-handed neutrino). Are neutrino masses non-zero in the model? What sets their scale? Is the seesaw mechanism completed?

**9c. Strong CP problem**
- F53 states `θ = pure gauge`. Is this a solution to the strong CP problem, or a statement that θ is zero at tree level? Does it survive loops?

**9d. Cosmological constant**
- F57/F59 note the CC sector goes as `Λ^{3.9}` (UV-sensitive). Is this the cosmological constant problem? Is it acknowledged? How does the model avoid a huge CC?

**9e. Quark masses**
- NJL gives `m_c = 309.5 MeV` (constituent quark). What are the current quark masses? Are they derived from the `E_g` condensate the same way lepton masses are?

**9f. CKM matrix**
- Is the CKM mixing matrix derived anywhere in the model, or is it absent? Check findings for any mention of CKM, Cabibbo angle, or quark mixing.

**9g. W and Z boson masses**
- F118 gives self-consistent `(W, v, c)`. What are the predicted `m_W` and `m_Z`? Are they compared to `80.377 GeV` and `91.188 GeV`?

**9h. Anomalous magnetic moment**
- Is `g-2` for the electron calculable in this model? If the photon propagator is correct, the 1-loop QED diagram should be computable. Any attempt?

---

### Step 10 — Check Finding File Quality

Run a spot-check on 10 finding files selected to cover different sectors:

```bash
# Pick a representative sample
for f in findings/F26-*.md findings/F41-*.md findings/F64-*.md \
          findings/F71-*.md findings/F91-*.md findings/F113-*.md \
          findings/F122-*.md findings/F125-*.md findings/F138-*.md \
          findings/F161-*.md; do
    echo "=== $f ==="
    head -60 $f
done
```

For each, check:
- Is there a clear statement of what is derived vs assumed?
- Are all equations dimensionally consistent?
- Are test results cited and do they exist in `tests/findings/`?

---

### Output Format

Write your audit report to `docs/audits/physics-audit-report-2026-06-29.md`.

Structure it as:

```markdown
# Physics Audit Report — 2026-06-29

## Executive Summary
[3–5 sentences: overall assessment, most critical issues found]

## Critical Issues (blocks a physics claim)
[List each issue with: Finding #, Description, Severity, Recommended fix]

## Algebraic/Mathematical Errors
[Any equations where derivation steps are missing or wrong]

## Logical Gaps (derivation chains with missing links)
[Places where "derived" claims are actually assumed]

## Omissions (physics that should be in the model but is absent or unaddressed)
[Open problems — note if already acknowledged in docs/roadmaps/next-steps.md]

## Inconsistencies Between Findings
[Places where two findings make incompatible claims]

## Minor Issues (notation, precision claims, documentation)

## Verified Correct (things explicitly checked and found sound)

## Recommended Priority Fixes
[Ordered list of what to tackle first]
```

When you are done, also run:
```bash
python3 tools/regen_indexes.py
```

to ensure indexes are up to date after any notes you may have added.
