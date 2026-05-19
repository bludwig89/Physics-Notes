### Model review — items flagged for back-fix or re-framing (2026-05-16)

`changelog.md` 2026-05-16 (later) contains the full list (items 1–14, ranked substantive → cosmetic). The substantive items, in priority order:

1. `ca-unified-v2.md` line 48: $c = c_0(1 + \phi/c_0^2)^{-1}$ has the wrong sign for gravitational lensing; the working `ca_emqg.py` code uses the GR-Shapiro form $c = c_0/(1 - 2\phi/c_0^2)$. Doc back-fix required.
2. `ca-unified-proposition.md` line 69: published as $c \propto |\Phi|^{-\alpha}$ but F3b test uses $|\Phi|^{+\alpha}$ — published formula would give *repulsion*. Either back-fix v1 to `(+α)` or mark v1 retired with pointer to v2 S1.
3. `H_Y = c^2 \cdot y \cdot (\Phi\,\eta^\dagger\chi + \text{h.c.})` carries a `c²` factor that has no Standard-Model counterpart — internal units kludge. Yukawa coupling values reported by this code are *lattice* couplings, not SM couplings.
4. The L4 EMQG Poisson is 2-D but the lensing test scores it against a 3-D-Newtonian linear-in-M target. 2-D Green's function is logarithmic; the "8.5% off the expected 2.0" claim is dimensionally inconsistent.
5. L3 composite-photon "PASS" hides an O(k) curl-equation residual (Finding 2). The kinematic parts (dispersion, transversality) pass cleanly; the central Maxwell identity does not.
6. 3-D simple-cubic `ca_core.py::weyl_step_3d_splitstep` is *not* a non-trivial QCA — Papers 1, 2 prove only the trivial automaton lives there. The code is a valid linearized-Weyl spectral propagator; the "CA" label is overstated. v2's `ca_bcc.py` is the non-trivial replacement.

Cosmetic items 7–14 are in the changelog: F3 pass band is 7 decades wide; `mu2_neg = -0.5` is a brittle sign-flip convention; `ca_maxwell.py` line 171 has a dead placeholder; `qca-papers-1-4-overview.md` line 53 still has Paper 1 Eq. 15 sign typo not back-fixed; `c` parameter is overloaded across three meanings; F3b doesn't test the $1/b$ scaling; no $dt \to 0$ convergence anywhere; no discrete-current-conservation check for U(1) or SU(2).

### Model-observation items 8–14 cleared (2026-05-16, later still)

| # | Item | Resolution |
|---|------|-----------|
| 8  | Brittle `mu2 = -0.5` sign-flip in F4 | `ca_higgs.py` / `ca_unified.py` now take explicit `phase ∈ {'broken','symmetric'}` kwarg; `mu2` is the magnitude in both cases.  F4 migrated.  Legacy negative-mu2 callers still work. |
| 9  | Dead placeholder at `ca_maxwell.py` line 171 | Removed.  Curl residual unchanged. |
| 10 | `qca-papers-1-4-overview.md` line 53 Paper 1 Eq. 15 sign typo | Back-fixed in doc and `ca_bcc.py` module docstring (working code already correct). |
| 11 | `c` overloaded across three meanings | Added non-breaking parameter aliases `c_unitary` (weyl_step_2d_splitstep), `c_macro` (c_field_from_phi), `c_energy_unit` (unified_step) with docstring notes. |
| 12 | F3b doesn't test $1/b$ scaling | New `test_F3b_scan` scans $b \in \{40,60,80,110,150\}$ at L=192; passes if power-law slope is within $\pm 0.4$ of $-1$ and norm preserved at machine precision. |
| 13 | No $dt \to 0$ convergence anywhere | New `test_dt_convergence` runs `unified_step` at $\Delta t \in \{1.0, 0.5, 0.25\}$ over fixed T; Richardson ratio $= 4.07$ confirms $O(\Delta t^2)$. |
| 14 | No discrete current-conservation check | New `test_E3_continuity`: (a) U(1) lattice $\partial_t \rho + c\,\nabla\!\cdot\!J = 0$ residual scales as $O(\Delta t^2)$ (Richardson ratios 4.05, 4.01); (b) SU(2) isospin rotation preserves local $\rho$ at $4.4\times 10^{-16}$. |

Items 1–6 (substantive) and item 7 (F3 pass-band width) remain open — they require physics decisions, not refactors.

### Model-observation items 1–5 cleared (2026-05-16, even later)

The five substantive items resolved with code and doc changes:

| # | Item | Resolution |
|---|------|-----------|
| 1 | `ca-unified-v2.md` line 48 wrong-sign $c(\phi)$ | Doc back-fixed to GR-Shapiro form $c = c_0/(1-2\phi/c_0^2)$ matching `ca_emqg.py::c_field_from_phi`. Wrong Paper-6 citation removed. |
| 2 | `ca-unified-proposition.md` line 69 $(-\alpha)$ exponent | §Coupling-2 marked RETIRED; explicit pointer to `ca-unified-v2.md` §S1 Poisson replacement. |
| 3 | Yukawa $H_Y$ carries spurious $c^2$ | Refactored `H_D = c·α·k + m·β` (c only in kinetic). $H_Y$ is now clean SM form $y\cdot(\Phi\eta^\dagger\chi + \mathrm{h.c.})$. F1 / F4 still pass at machine precision; D1 dispersion residual $1.2\times 10^{-16}$ with updated analytic. Zitterbewegung frequency analytic = $2m$ (was $2mc^2$). |
| 4 | L4 EMQG Poisson 2-D scored against 3-D Newtonian | New `solve_poisson_3d` + `test_lensing_deflection_3d`. Linear-in-M scaling on the 3-D 1/r Green's function: $\|\Delta(2M)/\Delta(M)-2\| = 3.5\times 10^{-3}$ at L=64 (26× tighter than the 8.5% number against the 2-D log-potential). |
| 5 | L3 "PASS" hid O(k) curl residual | `test_L3` split into `test_L3a` (dispersion + transversality + anisotropy — 3/3 PASS) and `test_L3b` (Maxwell curl — PARTIAL/INFO). Driver prints distinct status lines. |

Open: item 6 (`ca_core.py`'s 3-D simple-cubic propagator mis-labeled as "QCA"; the trivial-only result is documented but the function name has not been retitled). Item 7 (F3 pass-band width) requires a physics judgment about what "back-reaction works" means.
