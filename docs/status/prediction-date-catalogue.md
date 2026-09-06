# Prediction-date catalogue — watching for a second H3 instance

**Date:** 2026-09-06 - 02:00

## Purpose

Rubric row **H3** ("out-of-sample survival") is graded `QUANT` on exactly one clean instance:
`CL014`/`CL007`, $m_Z/m_W=3/\sqrt7$, fixed **2026-06-08** and checked against the PDG 2025
re-analysis that excluded the CDF-II $m_W$ measurement — a prediction tested against data that
arrived *after* it was fixed, not fit to data already in hand. A second such instance would
substantially strengthen the row (one survival could be luck; two starts to look structural), but
it cannot be forced — it depends on an external dataset actually being revised in the future
against a number this project already committed to on a known date.

This document is the lookup table that makes that check systematic instead of accidental (the
$m_Z/m_W$ survival was apparently noticed rather than watched for). It does **not** contain a
second instance — none currently exists — it is the list a future session (or a periodic search
pass) checks new PDG/CODATA/Planck/DESI/LIGO/gamma-ray releases against. Do not use this list to
re-derive or re-litigate the $m_Z/m_W$ result itself; that is closed (see `CL014`).

## What counts as a second instance

Three conditions, all required, matching the standard the $m_Z/m_W$ case already meets:

1. **The model's number was fixed on a known date, before any revision.** The `first_issued` /
   finding date columns below are that date.
2. **The comparison dataset gets revised** (a new PDG average, a new CODATA adjustment, a new
   Planck/DESI/BICEP release, a tightened astrophysical bound, a superseded measurement excluded
   the way CDF-II's $m_W$ was) — not just re-quoted unchanged.
3. **The model's fixed, unchanged number is re-compared against the new value** and the residual
   is reported (better *or* worse — both are informative; only "improves, or holds inside its
   stated bracket, against a real revision" counts as a survival in the $m_Z/m_W$ sense).

A case that fails condition 2 (the model number moves, or the "revision" is just noticing an
existing dataset for the first time) is not an instance — see `CL276` below.

## Watch list

| # | Prediction | Value (fixed) | Fixed | Compared against | Current comparison | Status / what to watch |
|---|---|---|---|---|---|---|
| 1 | $m_Z/m_W$ (`CL014`/`CL007`) | $3/\sqrt7=1.133893$ | 2026-06-08 (F49 2026-05-28, F138 2026-06-11) | PDG world average $m_W$ | PDG 2025 (CDF-II excluded): $-0.064\%$ | **The existing clean instance. Closed — do not re-attack.** Next PDG cycle is the thing to watch for a *third* data point on the same line, not a new independent instance. |
| 2 | $\alpha_s(M_Z)$ (`CL022`) | $0.11955$ (1-loop) | 2026-06-08 (F144 2026-06-12) | PDG world average $\alpha_s(M_Z)$ | Moved once already: PDG avg $0.1180\to0.1175\pm0.0010$ (2026-08-18), residual $+1.3\%\to+1.7\%$ ($\approx2.1\sigma$) | **Already has one revision on record — but it worsened, not survived.** Worth tracking anyway: it is the one case in the register where "the measurement moved, not the model" is already documented mechanically. A *further* PDG average shift (tighter lattice-QCD determinations are ongoing) either sharpens the tension past $3\sigma$ (falsifier) or swings back toward the model. Search: "PDG world average alpha_s strong coupling constant". |
| 3 | $m_W$, $m_Z$ absolute (`CL276`) | $m_W\in[80.147,80.548]$ GeV, $m_Z\in[90.879,91.332]$ GeV | 2026-08-16 (F320) | PDG 2024 $m_W=80.3692\pm0.0133$, $m_Z=91.1880$ GeV | Both inside bracket; $+0.222\%$ / $+0.158\%$ $\Delta r$-free residual | **Not yet an instance (F320 postdates PDG 2025, so this is a fresh prediction, not a survived revision) — but the single best candidate to become one.** A future PDG/CODATA revision to $\alpha$, $G_F$, or a new precision $m_W$ measurement (CDF-II-style events recur) checked against this *already-fixed* bracket is exactly the $m_Z/m_W$ pattern repeated. Search: "PDG electroweak review m_W m_Z", "CODATA fine structure constant new measurement". |
| 4 | Newton's constant $G$ (`CL008`) | $G=a^2c^3/(8\pi\sqrt3\hbar)=6.6743\times10^{-11}$ | 2026-06-08 (F79 2026-06-02, F107 2026-06-06) | CODATA recommended $G$ | $3\times10^{-8}$ (CODATA 2022) | $G$ is the one fundamental constant whose lab measurements are famously discordant across groups (BIPM, HUST, Wuhan, etc.), so CODATA's recommended value has shifted between adjustment cycles historically and is a real candidate for a future revision to test this fixed, zero-free-parameter number against. Search: "CODATA recommended value Newton's gravitational constant" (next full CODATA adjustment). |
| 5 | Quantum-gravity dispersion scale (`CL011`) | $E_{\text{QG},2}=\sqrt{54}\,\hbar c/a\approx1.36\times10^{19}$ GeV | 2026-06-08 (F28 2026-05-23, F107 2026-06-06) | GRB/gamma-ray time-of-flight quadratic-dispersion bounds | No bound yet at this scale (Fermi-LAT/HAWC/LHAASO bounds currently well below $10^{19}$ GeV) | Not a converging measurement but a hard ceiling: any future analysis (LHAASO, CTA, next-generation GRB polarimetry) that pushes the $n=2$ bound *above* $1.36\times10^{19}$ GeV falsifies outright; one that approaches without crossing it is a tightening worth logging with its date. Search: "quantum gravity dispersion GRB bound quadratic n=2 2026". |
| 6 | No dimension-6 Lorentz-violating photon operator beyond bound (`CL274`) | coefficient $\in[-1/162,0]$, exact rational | 2026-08-16 (F319) | LHAASO/Crab/AGN polarimetry, photon dispersion | No detection (consistent) | The model asserts an *absence*, not a small number, so there is nothing to "survive" in the usual sense — but a future null result from a more sensitive facility (CTA, next LHAASO catalogue) reported against this pre-existing, dated, zero-parameter coefficient is still worth a dated log entry if it ever becomes the subject of a dedicated bound (as happened to the sibling claim `CL284`/F327 against Li & Ma's LHAASO analysis, 2026-08-26). |
| 7 | Structure-growth index $\gamma_g=6/11$, $\mu\equiv\Sigma\equiv1$ (`CL254`) | $\gamma_g=6/11$ exact; $S_8=0.8410$ | 2026-08-05 (F288) | Combined CMB $S_8=0.836^{+0.012}_{-0.013}$ (0.29σ); KiDS-Legacy 2025 (1.17σ); **DES Y6 $3\times2$pt $0.789\pm0.012$ (3.00σ, live tension)** | Mixed — passes two surveys, in tension with a third | Fixed before DES Y6 was folded in, so DES Y6 is itself close to (arguably already inside) instance territory depending on exactly when F288 was written relative to the DES Y6 release date — **worth confirming that ordering explicitly in a future session** rather than assuming it here. The next round (Euclid, LSST/Rubin $S_8$) is the one to watch either way: if DES Y6's $3\sigma$ direction consolidates, this falls; if it resolves toward Planck/KiDS, this is candidate #2. Search: "DES Y6 S8 tension update", "Euclid cosmic shear S8 2026/2027". |
| 8 | Electron anomalous magnetic moment $a_e$ (two-loop, `CL228`-adjacent, F261) | $a_e=1.15963743\times10^{-3}$ | 2026-07-23 (F261) | Measured $a_e=1.15965218\times10^{-3}$ | rel. err $1.3\times10^{-5}$ | Lower priority: this is a standard QED calculation (confirms the model reproduces known QED, not a distinctively model-specific zero-parameter structural claim in the `CL014` sense), and the *model* number is not independent of an input $\alpha$ that is itself contested between competing recoil measurements (Berkeley Cs vs LKB Rb). Listed for completeness; a future $\alpha$ revision would change the comparison but says more about which $\alpha$ measurement wins than about this model. |

## Softer / not yet trackable in this form

- **Tensor-to-scalar ratio $r\sim10^{-118}$, $n_t=2$ (`CL267`)** — fixed 2026-08-11, contingent status (not `live`), and the falsifier is a detection threshold (any $r$ at all) rather than a converging comparison, so there is nothing to "check improve/worsen" — only "has BICEP Array detected anything yet." Worth a periodic look but does not fit this table's pattern.
- **$\dot G/G\equiv0$ (`CL242`)** — fixed 2026-08-04, `open`/`unreviewed-seed`, no external bound cited in its card yet. If a future session sources a lunar-laser-ranging or pulsar-timing $\dot G/G$ bound and dates it, this becomes trackable in the same form as row 4.
- **Deuteron $E_b=2.224$ MeV** — already at $0.026\%$ against a very mature, unlikely-to-move nuclear measurement; low value as a future-revision candidate.

## Protocol for future sessions

Do not force this — per the standing session brief, finding a second instance is opportunistic,
not a single-session deliverable. When a session does touch this file:

1. Re-run the search terms above (periodically, not once) against current PDG/CODATA/Planck-DESI/LIGO releases.
2. For any row where the comparison dataset has genuinely revised (not merely been re-quoted), add
   a dated sub-entry recording the old value, the new value, and the model's unchanged residual
   before/after — the same structure `CL014`'s card already uses.
3. If a row clears all three conditions in "What counts as a second instance," promote it: write it
   up in `docs/claims/` the way `CL014` documents the first one, and update rubric row H3 in the
   live `docs/status/completeness-*.md` file to `QUANT (2 instances)` or similar, with both cited.
4. Do not edit `CL014`, `CL007`, or their underlying findings as part of this exercise.

## Sources

- `docs/claims/CL014-weinberg-angle-threshold.md`, `CL007-weinberg-angle-derived-with-its-scale.md` — the existing instance
- `docs/claims/CL022-alpha-s-at-mz-open-tension.md`
- `docs/claims/CL276-absolute-gauge-boson-masses-two-inputs.md`, `CL016-mw-and-mz-absolute-not-claimed.md`
- `docs/claims/CL008-gravity-sourced-by-full-stress-energy.md`
- `docs/claims/CL011-quantum-gravity-dispersion-scale.md`
- `docs/claims/CL274-no-dimension-5-photon-operator.md`, `CL284-elementary-single-branch-fermion-excluded.md`
- `docs/claims/CL254-structure-formation-zero-free-functions.md`
- `docs/status/exactness-inventory.md` (row 299, `a_e` two-loop)
- `papers/Claims-and-Falsifiers-Summary.md` (revision 7) — headline numbers table, falsifiable predictions
- `docs/status/completeness-2026-08-20.md` row H3
