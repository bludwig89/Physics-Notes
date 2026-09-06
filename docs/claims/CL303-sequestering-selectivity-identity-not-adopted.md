---
id: CL303
title: 'A Kaloper-Padilla-style non-local/global sequestering mechanism achieves unbounded order-selectivity between the F164/F59 heat-kernel moments as an exact, sympy-verified identity, dwarfing F319 U8''s required selectivity of >=1.27e116 -- contingent on grafting new global Lagrange-multiplier fields onto the model''s gravity sector, which is not adopted here'
slug: sequestering-selectivity-identity-not-adopted
tier: supporting
kind: derivation
status: contingent
domain: [GR, cosmology]
exactness: quantitative
findings: [F367, F368, F332, F164, F193, F196, F241, F319, F178, F182, F79, F59]
tests: [F367-cc-sequestering, F368-cc-sequestering-consistency]
modules: [src/casim/engine/interactions/cosmology_lambda_sequestering.py, src/casim/engine/interactions/cosmology_lambda_sequestering_consistency.py]
constants: []
supersessions: []
reviews: []
rolls_up_to: null
falsifier: stated
first_issued: '2026-09-04'
last_verified: '2026-09-05'
provenance: authored
review_state: authored
confidence: medium
---

# CL303 — Sequestering's constant-cancellation identity gives unbounded selectivity and is well-matched to K9, but is not adopted into the model's gravity sector

## Statement

F367 proves, symbolically and independently of the Kaloper-Padilla citation, that a
spacetime-constant contribution $C$ to the matter trace $T(t)$ is annihilated *exactly*
($d(\text{residual})/dC\equiv0$) by the sequestering subtraction $T(t_0)-\langle T\range$, for
any finite spacetime 4-volume, any power-law domination exponent $n$, and any measure power $p$
— giving formally unbounded selectivity between a constant source and any time-varying one. F164's
bare $\rho_\text{vac}$ is exactly this class of source. This dwarfs F319 U8's required relative
selectivity of $\ge1.27\times10^{116}$. The surviving matter-history residual has an exact
closed form, $3n\,\rho_m(t_0)$ at the physical measure $p=3$, landing $0.036$ dex from the
observed $\Omega_\Lambda\rho_\text{crit}$ at matter domination ($n=2/3$) — a crude single-fluid
toy, not a tightened derivation of $\Omega_\Lambda$. **This claim is contingent**: it holds granted
that the model's gravity sector is extended with new global, non-propagating Lagrange-multiplier
fields (the sequestering mechanism's own machinery), which decision 4 of `CLAUDE.md` does not
currently contain and which this finding does not adopt.

## What it extends

Extends general relativity's treatment of the cosmological constant: standard GR sources
$G_{\mu\nu}$ locally from $T_{\mu\nu}(x)$; sequestering instead sources it from
$T_{\mu\nu}(x)-\langle T\range g_{\mu\nu}/4$ via a global constraint, evading Weinberg's 1989
no-go theorem (which applies only to local, Lorentz-invariant adjustment mechanisms) by
construction. This is the literature's own mechanism (Kaloper & Padilla 2014), adapted here to
this model's own quantities (structural $G$, F164's bare $\rho_\text{vac}$) rather than
re-derived in full generality.

## Additional adoption costs, not closures (F368, 2026-09-05)

F368 ran falsifier 4 (above) against Padilla's actual base action (arXiv:1502.05296 sec.7,
consulted directly) rather than only F367's abridged local-consequence identity. The three legs
falsifier 4 names (PPN, F178's vacuum-scope restriction, induced-$G$) are not in tension --
falsifier 4 does not fire. But Padilla sec.7 shows the *base* mechanism itself (not only its
"why now" scalar-potential extension) additionally requires:

- **Spatial closure ($k>0$)**, from the mechanism's own global integral constraint. Not excluded
  by current data: Planck CMB-alone has a live, *disputed* $>99\%$ C.L. preference for positive
  curvature (Di Valentino, Melchiorri & Silk 2020, arXiv:1911.02087; countered by Efstathiou &
  Gratton 2020, arXiv:2002.06892, who attribute it to a prior/parameter-volume artefact), resolved
  to flat once BAO is added. Independently sympy-verified (F368): eternal de Sitter and ordinary
  flat/open matter-only expansion both give divergent total spacetime 4-volume; only a closed
  matter-dominated recollapse gives finite 4-volume, matching the mechanism's own requirement.
- **Non-eternal ("transient") dark energy** -- eternal $w=-1$ is "incompatible with the
  sequestering proposal" (Padilla sec.7, cited) for the same finite-4-volume reason. DESI DR2's
  own $w_0>-1,w_a<0$ preference (3.1$\sigma$ over $\Lambda$CDM with CMB, arXiv:2503.14738) gives
  $dw/da>0$: $w$ trending less negative toward the future -- the qualitative direction transience
  needs, reported as *not contradicted, directionally aligned* (not as a derived prediction, and
  not as a promotion of rubric row K10, which this does not touch or absorb).

Neither cost changes this card's `status` (still `contingent` -- neither promotes nor forecloses
adoption); both are added to what adopting sequestering would need to be consistent with, on top
of the field-content cost already stated below.

## Evidence

| Source | What it shows | Exactness |
|---|---|---|
| `findings/F367-cc-sequestering.md` | Full derivation, the constant-cancellation identity, the closed-form residual, the numerical spot-check, the 13-point attack pass | mixed: exact (identity, coefficient) / quantitative ($0.036$ dex) / structural (S1, S6 citations) |
| `tests/registry/interactions.yaml` → `F367-cc-sequestering` | 3/3 checks PASS (tier: gate), 2/2 declared controls verified red-and-only-there | exact / quantitative |
| `test-results/F367_cc_sequestering.json` | `dresidual_dC_is_zero: true` for all tested $n$; `coefficient_matches_3n: true`; `dex_from_observed: -0.0357` | exact / quantitative |
| `findings/F319-uv-sector-reconciled-physical-cutoff-and-counterterms.md` §U8/§7 | The required selectivity bound and the dim-0/dim-2 operator-ledger separability this claim's applicability rests on (S1) | quantitative / structural |
| `findings/F241-omega-lambda-o1-residual-anthropic.md` §3 | The already-excluded circular FEH route this mechanism is distinguished from (S6) | structural |
| `findings/F368-cc-sequestering-consistency.md` | Falsifier 4 (below) checked directly against Padilla's base action: PPN/F178-vacuum/induced-$G$ legs not in tension (one algebraic sympy identity); two NEW costs surfaced -- spatial closure and non-eternal $w$, both base-mechanism features (cited), neither excluded by current data, the latter directionally aligned with DESI DR2 | structural (cited) / exact (one identity) |

## Falsifier

`falsifier: stated`:

1. A demonstration that $d(\text{residual})/dC\ne0$ for some finite $V_4$ (i.e. the constant-
   cancellation identity of F367 §2 fails to hold generally) would falsify the core claim outright.
2. A demonstration that F164's $\rho_\text{vac}$ is *not*, in fact, a spacetime constant under the
   model's own adopted cosmology (e.g. a reading of F182/F107 under which the lattice cell $a$ is
   itself dynamical with cosmic time) would break the model-specific applicability of the identity
   without touching the identity itself.
3. A demonstration that F319 §7's operator ledger is wrong to treat $\Lambda$ and $1/G$ as
   separable IR-EFT coefficients (e.g. that this model's specific UV completion forces a fixed
   relation between them at the effective level) would remove the applicability argument (S1) this
   card's contingency rests on — the single most attackable structural step, per F367's own
   falsifier 3.
4. A worked construction showing sequestering's global Lagrange-multiplier sector is inconsistent
   with the model's other decision-4 content (PPN, the F178 vacuum-scope restriction, the
   induced-$G$ derivation) would close the adoption question in the negative, converting this
   card's `status` from `contingent` to `withdrawn`. **CHECKED by F368 (2026-09-05) and NOT MET**:
   in vacuum, Padilla's own local field equation reduces algebraically to ordinary GR plus a
   $\Lambda_\text{eff}$ term (ordinary Schwarzschild-de Sitter, PPN-negligible), and the
   induced-$G$ coefficient is untouched by construction (F367 S1) -- so this falsifier does not
   fire and `status` stays `contingent`. F368 does, however, surface two *further* costs this
   falsifier did not name: Padilla's own base action (not only its "why now" extension) requires
   spatial closure ($k>0$) and non-eternal ("transient") dark energy -- see "Additional adoption
   costs (F368)" below.

## Status & history

`status: contingent` because the claim holds only granted the (currently un-adopted) hypothesis
that the model's gravity sector is extended with sequestering's global fields — the card is not
`open` because the evidence for the *stated* claim (the identity, its selectivity, its match to
F164's residual) is complete; the contingency is the point of the claim, not a gap in it. Not
`rolls_up_to` any headline card: this is a standalone supporting result on rubric K9/ledger G1,
first issued alongside F367 with no prior history to narrow.

## Sources

- `findings/F367-cc-sequestering.md`
- `findings/F368-cc-sequestering-consistency.md` (ran falsifier 4; not met; two new costs named)
- `findings/F332-cc-dynamics-two-channels-excluded.md` (named this channel type, did not build it)
- `docs/status/open-derivations.md` row G1
- Kaloper, N. & Padilla, A., *Phys. Rev. Lett.* **112**, 091304 (2014); *Phys. Rev. D* **90**,
  103523 (2014); Weinberg, S., *Rev. Mod. Phys.* **61**, 1 (1989)
- Padilla, A., "Lectures on the Cosmological Constant Problem", arXiv:1502.05296 (2015), sec.7
- Planck Collaboration, arXiv:1807.06209 (2018); Di Valentino, E., Melchiorri, A. & Silk, J.,
  *Nature Astronomy* **4**, 196 (2020), arXiv:1911.02087; Efstathiou, G. & Gratton, S.,
  arXiv:2002.06892 (2020)
- DESI Collaboration, arXiv:2503.14738 (2025)
