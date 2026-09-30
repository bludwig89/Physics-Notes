# Appendix A4 — Open Residuals

*Everything the monograph found not closed, sorted by where it bites and roughly by size. Two
kinds of entry appear: **physics residuals** (a number that doesn't yet match, a mechanism not yet
derived) and **documentation gaps** (`GAPS.md`, G-1 through G-15 — places where a source doesn't
justify itself, or two sources disagree and nobody has reconciled them). Both matter to a
rebuilder; only the first kind is "physics left to do."*

## A4.1 — Physics residuals, largest first

| Residual | Size | Where it bites | What would close it |
|---|---|---|---|
| Cosmological constant magnitude | ~$10^{121}$ overshoot reduced to one undetermined $O(1)$ factor ($\Omega_\Lambda\approx0.685$) | Ch.21 | A derivation of the last dilution/normalization factor; `docs/claims/CL021` states plainly this is `not_claimed` |
| Dark-sector relic abundance | Order-of-magnitude free for both surviving candidates | Ch.22 | Sterile neutrino: an unbuilt lepton-asymmetry/entropy-dilution history. Geon: a primordial spectral feature ~$2\times10^6\times$ CMB, which Ch.20's own inflaton no-go (F282) says the model structurally cannot supply via the standard route — the unfinished domain-wall channel (F366) is the only alternative on the table |
| $\alpha_s(M_Z)$ tension | 2.1σ (model 0.11955 vs. PDG $0.1175\pm0.0010$) | Ch.13b | `docs/claims/CL022` — open, not a fit-quality artifact; independent of the still-unresolved $d_1$ estimator (next row) |
| $d_1$ / $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}$ estimator | Extrapolates to $\approx31$–$34$, outside the committed $[1,7.98]$ bracket by $\sim4\times$ | Ch.13b (G-11) | F337's own named exhaustion condition has now fired (F350) — the estimator's non-convergence needs to be either resolved computationally or promoted from "non-convergence" to "evidence against the $g_s=\tfrac12$ lock," a call `CL022`/`CL252` have not yet made |
| $\sqrt\sigma/f_\pi$ confinement factor | $+12\%$ residual, not removable by any principled BCC correction attempted | Ch.13b/17 (F235) | Unknown — every attempted fix failed; compounded by F146's own σ measurement running on a pre-BCC cubic gauge action (S21), which could shift the number further on re-derivation |
| Ionization-energy underbinding | Mean 27.7% (Z=2–20), 38.2% (Z=21–30, Sc–Zn) | Ch.24 | Missing exchange interaction (Hartree + Koopmans only) — diagnosed cause, not yet fixed; relativistic corrections are 4 orders of magnitude too small to be the culprit |
| Photon–fermion momentum conservation | Not achieved at any coupling strength tested; direction reverses sign at `m_index=4`; off-axis numbers not converged in tick count | Ch.10 | Entirely open — the leading candidate mechanism (fermion internal spin-state dependence of the recoil direction) is identified but not derived |
| Superconducting $T_c$ (Eliashberg route) | Plateaus at 16–17%, vs. an Allen-Dynes target it cannot reach by this route | Ch.25 (F374) | A disclosed no-go for this specific route; the DFT-DOS route (F375) does reach 4.9% by a different path |
| Weight-as-phase falsification handle | Three numerically distinct but physically identical $\sigma$ figures in circulation ($-0.89\sigma$, $0.91\sigma$, $1.04\sigma$) | Ch.15 (G-10) | A single canonical statement, in `docs/theory/key-decisions.md` decision 7 or `CL028`, of which invariant each figure tracks |
| Horizon-entropy coefficient | F79 (heat-kernel) and F355 (direct entanglement) disagree by a bracketed $[0.79,3.18]$ factor | Ch.20/21 | An undecided doubler convention — the mechanism is named, not resolved |
| Deuteron binding energy | Two findings (F148, F157) both report 2.234 MeV via `solve_deuteron()`, vs. 2.224 MeV (0.026% from measurement) everywhere else in Ch.14 | Ch.24 (G-13) | Checking which configuration `solve_deuteron()`'s default call site actually uses |
| Curvature-ceiling convention | A factor of exactly 24 ($24^{1/4}=2.2134$ in length) between F183's static-core convention and F284's cosmological-epoch convention | Ch.19/20 (G-12, half-resolved) | Either derive one universal lattice curvature ceiling from the lattice's own dynamics, or adopt one of the two conventions by an explicit decision (in the manner of F178's adoption) |
| GRB dispersion-scale reconciliation | F28's displayed figure ($\sqrt2\,E_\text{Planck}$) and CL011's updated figure ($\sqrt{54}\,\hbar c/a$, F107) differ by ~27% | Ch.7/17 (G-5) | Re-derive F28's table with the canonical $a$; both values sit ~15 decades below any current bound, so this has no present observational consequence |

## A4.2 — Structural / non-numerical open items

- **PMNS mixing angles and $\delta_{CP}$** (Ch.16): proven, not merely unfinished, to have no lattice
  selector (F254/F353) — the three mixing amplitudes are inequivalent 1-d irreps of the residual
  point group. This is a closed no-go, not a residual awaiting more work.
- **Absolute Majorana scale $M_R$** (Ch.16, F343): three routes checked and closed; $M_R$ joins
  $v$, the quark masses, and $m_{E_g}$ as a fifth unfixed-scale cluster member.
- **Hidden deterministic layer beneath the amplitude** (Ch.1 §1.7, revisited Ch.5 §5.6, Ch.25):
  genuinely undecided by every source read, and the two readings are stated to be
  experimentally indistinguishable by every test proposed to date. Chapter 25 sharpens the case
  for *not needing* the hidden layer (real entanglement generation, Tsirelson saturation with no
  superdeterministic construction) without resolving whether one could still exist.
- **Free-parameter count, provisional** (final reconciliation belongs to Appendix A3): today the
  model uses at minimum $\{G, f_\pi, m_\tau \text{(or } N\text{)}, v\}$ as independent dimensionful
  external anchors (Ch.17), plus the still-external $\alpha_\text{em}$ (Ch.9's four-avenue no-go)
  and the per-flavor fermion mass magnitudes (Ch.11). Chapter 17's own synthesis flags an
  unconfirmed case that three of these collapse to one shared constant $d_1$ — which would cut the
  count from four to two if the Ch.13b non-convergence (above) resolves in its favor.

## A4.3 — Documentation gaps (`GAPS.md`, full ledger)

One line each; see `docs/monograph/GAPS.md` for full text and exact citations.

| # | Chapter | One-line description |
|---|---|---|
| G-1 | 1 | The elegant-design heuristic (P7) is used throughout with no source ever arguing it tracks truth |
| G-2 | 2 (resolved by 6) | Two CLAUDE.md decisions used by Ch.2 were never promoted to numbered postulates — bookkeeping gap, not a circularity; fully resolved by Ch.6 |
| G-3 | 3 | F276's variable-speed stepper correction is verified on a non-canonical 2D module, not the canonical BCC hop — untested whether it transfers |
| G-4 | 5 | `CL253` doesn't record that F312 already supplies the non-Abelian commutator its own text says is missing |
| G-5 | 7 | F28's LIV scale and `CL011`'s updated figure disagree by 27%, unreconciled (no observational consequence at present) |
| G-6 | 8 | F89's W/Z/gluon table is wrong for gluon (chiral, should be even per F91/S2); separately, `CL084` is a claims-layer artifact |
| G-7 | 12 | Unreconciled duality: is the W boson a postulated Yang-Mills link field (F31–F36) or a forced pairing-classification channel (F91)? Ch.13a resolved this for the gluon; the W question stays open |
| G-8 | 18 | F79's $g_*=48$ silently depends on Ch.12 (F38) and Ch.15 (F75) — undeclared in the plan's dependency table |
| G-9 | 19 | `CL160`/F181 claims-layer artifact — F181 is live, not withdrawn |
| G-10 | 15 | Three inconsistent $\sigma$ figures for the same falsification handle (also in A4.1) |
| G-11 | 13b | `CL022`/`CL252` stale against F337/F340/F350 — genuine content staleness, not a bookkeeping artifact (also in A4.1) |
| G-12 | 20 | Curvature-ceiling factor-24 fork between F183 and F284, genuinely open (also in A4.1); the companion $\sqrt3$ tick-duration error was found and corrected |
| G-13 | 24 | 0.45% deuteron binding-energy discrepancy between two findings' own `solve_deuteron()` calls (also in A4.1) |
| G-14 | 17 | `CL205`/F233 claims-layer artifact — F233 is live and load-bearing |
| G-15 | 22 | `CL177` accurately reflects F203 but is stale against three later findings that have since closed or sharpened three of its six falsifiability tests |
