# F407 — Fork: the minimal pseudo-mass quark fit (report derivation three) — one real degree of freedom, spent on nothing

**Date:** 2026-09-24 - 16:55
**Status:** Candidate finding (fork) — 7/7 legs PASS in both the mixed and the $M_Z$ scheme (M1 numerical rank; M2–M5 numerical searches). Two declared controls, each red exactly on the three M2 legs. **Verdict: the report's minimal ansatz passes the report's failure test (it does not need $m_s$ far from 93.5 MeV) and still predicts nothing: its single degree of freedom is not spent on any CKM number, GST does not emerge, and the candidate E_g angles are not selected.**
**Module:** `casim.engine.forks.particles.koide_pseudomass_minimal` (new, `forks/`, status `fork_live`)
**Test record:** `F407-koide-pseudomass-minimal` (tier gate, entry `check_koide_pseudomass_minimal`), driver `tests/findings/test_F407_koide_pseudomass_minimal.py` → `test-results/F407_koide_pseudomass_minimal.json`
**Claim:** CL316 (narrowed and extended with this finding; no new card — same assertion, smaller ansatz)
**Cross-references:** [[F404]] (the general-Hermitian version of the same fork; every F404 no-go carries over), [[F78]] (mass = amplitude squared), [[F93]] (E_g on the cube axes), [[F175]] (δ\* = 2/9), [[F346]] (the δ_U ≈ 2/27, δ_D ≈ 1/9 coincidences), research report `reports/Quark neutrino hierarchy lattice fit.md`, next derivation three.

---

## Summary

Derivation three of the 2026-09-24 flavour report asks for the pseudo-mass quark fit **per sector, in a minimal form**: A₁g + E_g √M at Koide $k=1$ with δ at the candidate values, plus three $T_{2g}$ amplitudes and one phase. It asks for a fit to the PDG 2025 masses and CKM in both the mixed and $M_Z$ schemes, a parameter count against the 10 observables, and a test of whether Gatto–Sartori–Tonin (GST) $\lvert V_{us}\rvert\approx\sqrt{m_d/m_s}$ emerges without being imposed. The route fails if it needs $m_s$ far from 93.5 MeV.

F404 had already built the route with a *general* Hermitian amplitude matrix per sector (14 real parameters) and the masses imposed as exact eigenvalues. This finding builds the smaller ansatz the report actually specifies, fits masses *and* CKM as observables with errors, and lets the sign pattern of the amplitudes come out of the fit instead of choosing it. Five results:

1. **The count is 9 against 10, and all 9 are real (M1).** At fixed E_g angles the ansatz has $\mu_U,\mu_D$, six $T_{2g}$ amplitudes and one $T_{1g}$ amplitude. The Jacobian of the fitted observables has full rank 9 at the solution, so the fit has exactly one genuine degree of freedom.
2. **The candidate angle pairs all fit, and the one degree of freedom discriminates none of them (M2).** Universal $(\delta^*,\delta^*)$, Żenczykowski's $(\delta^*/3, 2\delta^*/3)$ and the $(\delta^*/3,\delta^*/2)$ coincidence candidate all fit at $\Delta\chi^2\le1$ in both schemes (table below). $m_s$ is not pulled ($\lvert\text{pull}\rvert\le1.1$).
3. **The fit picks a signed down sector by itself.** No passing solution has all-positive down amplitudes. Two sign branches appear: $(-,+,+)$ (lightest negative, the F404 choice) and $(+,-,+)$ in *both* sectors (middle negative), which is the branch Żenczykowski's pair lands on.
4. **Lepton-like all-positive amplitudes close only at $m_s\approx$ ¼ of its value (M4).** Freeing $m_s$ and forcing every amplitude positive, the fit closes exactly at $m_s=27$ MeV (mixed; PDG 93.5) and $12.6$ MeV ($M_Z$; 53.3). The profile scan finds solutions only for $m_s\lesssim30$ MeV (mixed) and $\lesssim12$ MeV ($M_Z$). That is the report's failure test, failed in the opposite direction from Gérard et al., who needed $m_s$ larger.
5. **GST does not emerge (M5).** With $\lvert V_{us}\rvert$ and $\lvert V_{td}\rvert$ held out, the fitted solutions spread over $\lvert V_{us}\rvert\in[0.21,0.98]$ (mixed) and $[0.20,0.83]$ ($M_Z$). All the ansatz does is put a soft floor near 0.19–0.20, and that floor does not follow $\sqrt{m_d/m_s}$ (scaling check below).

## Physics

**The ansatz.** Per charged sector $f\in\{U,D\}$, on the $T_{1u}$ generation triplet (F78: $M_f=S_f^2$):

$$S_f=\mu_f\bigl(\mathbb 1+\sqrt2\,\hat E(\delta_f)\bigr)+\sum_{a<b}t_{f,ab}\,(e_{ab}+e_{ba})\;+\;i\varphi\,(e_{cd}-e_{dc})\big|_{\text{one slot, one sector}}.$$

The first term is the charged-lepton structure, exact Koide on the cube axes. The $t_{f,ab}$ are the three real $T_{2g}$ components. The last term is one $T_{1g}$ (imaginary antisymmetric) component. By F404 P6 at least one is needed for $J\neq0$, and "one phase" is the minimum. Which of the six slots holds it is a discrete choice. The fit tries all six and reports the one that wins. Masses are the squared eigenvalues of $S_f$ ordered by modulus, and the CKM is $V=U_U^\dagger U_D$. The sign of each eigenvalue is an output.

**Observables and the statistic.** Six masses with PDG 2025 errors. The $M_Z$ masses (Antusch–Hinze–Saad 2025) carry the same *relative* errors, a declared assumption since only their central values were fetched. The CKM enters as five numbers, $\lvert V_{us}\rvert,\lvert V_{cb}\rvert,\lvert V_{ub}\rvert,\lvert V_{td}\rvert,J$, as in F404. Four would be the independent count, but $J$ alone leaves the sign of $\cos\delta_\text{CP}$ open. A first four-observable version of this fit landed on the wrong branch at δ\*, with $\lvert V_{td}\rvert=0.0105$ against $0.0086\pm0.0002$. The fifth number costs the unitary floor $\chi^2=0.119$ that the best unitary matrix already pays on these inputs (F404), so the test statistic is $\Delta\chi^2=\chi^2-0.119$ with one degree of freedom, and a fit passes at $\Delta\chi^2\le3.84$ (95%).

**M1 — the count.** $2+6+1=9$ parameters, $6+4=10$ independent observables. The numerical Jacobian of the 11 fitted numbers with respect to the 9 parameters has rank 9 at the fitted point ($\sigma_\text{min}/\sigma_\text{max}=3.6\times10^{-2}$ mixed, $5.9\times10^{-3}$ $M_Z$). No parameter is redundant, so there is exactly one degree of freedom to test.

**M2 — the candidate angles** (best certificates found by the gate record; "slot" is where the $T_{1g}$ sits, $(f, \text{pair})$ with pairs 0 = (1,2), 1 = (1,3), 2 = (2,3)):

| $(\delta_U,\delta_D)$ | scheme | $\Delta\chi^2$ | $m_s$ pull | signs U / D | $T_{1g}$ slot |
|---|---|---|---|---|---|
| $(\delta^*,\delta^*)$ | mixed | 3.22 in the gate record; **0.03** in a 200-start-per-slot scratch search (slot U,1) | 1.09 | $(+,+,+)$ / $(-,+,+)$ | D,2 |
| $(\delta^*/3, 2\delta^*/3)$ | mixed | 0.94 | 0.42 | $(+,-,+)$ / $(+,-,+)$ | D,1 |
| $(\delta^*/3, \delta^*/2)$ | mixed | 0.03 | 0.10 | $(-,+,+)$ / $(-,+,+)$ | D,0 |
| $(\delta^*,\delta^*)$ | $M_Z$ | 0.35 | −0.26 | $(-,+,+)$ / $(-,+,+)$ | U,0 |
| $(\delta^*/3, 2\delta^*/3)$ | $M_Z$ | 0.003 | 0.00 | $(+,-,+)$ / $(+,-,+)$ | D,2 |
| $(\delta^*/3, \delta^*/2)$ | $M_Z$ | 0.006 | −0.04 | $(+,+,+)$ / $(-,+,+)$ | D,0 |

The gate record's search is a certificate search: it stops at the first solution under $\chi^2=1.119$, then also carries the anchor pair's per-slot solutions along the straight path in $(\delta_U,\delta_D)$ to each target ("continuation"). A reported value is an upper bound on the true minimum, not the minimum itself. The mixed-scheme δ\* entry shows the gap: 3.22 in the record, 0.03 in the deep search.

Every pair fits with $\Delta\chi^2$ well under one unit once searched properly. The single degree of freedom has nothing to push against, so it cannot rank the candidates. Żenczykowski's pair does not fit on the $-\sqrt{m_d}$ branch in the mixed scheme (best 7.2 after 180 starts). It fits on the middle-negative $(+,-,+)$ branch in both sectors, a sign branch F404 did not examine for joint fits.

**M3 — the band carries over from F404.** The minimal ansatz is a subset of F404's general Hermitian one, so it can only fit where F404 fits. The off-band pairs $(0.24,0.01)$ and $(0.15,0.30)$ fail at $\chi^2\approx10^3$–$10^4$. The landscape scan (21 × 21 grid over $[0,\pi/3]^2$, `test-results/F407_koide_pseudomass_minimal.json`) shows the same diagonal band as F404, $-0.05\lesssim\delta_D-\delta_U\lesssim0.1$, covering about 4% of the cell in both schemes. It extends up to $\delta_U\approx0.5$ in the mixed scheme and $\approx0.37$ at $M_Z$. Nothing inside the band is preferred. Scratch grids with 6 starts per slot show isolated holes inside the band that deeper searches fill.

**M4 — the $m_s$ test.** The report's failure criterion is "fails if it needs $m_s$ far from 93.5 MeV". With the fit free to choose signs, it never needs to: $m_s$ lands at 93.5–94.5 MeV (mixed) and 53.2–53.4 MeV ($M_Z$) at every passing point. Forcing lepton-like all-positive amplitudes and freeing $m_s$:

| scheme | $m_s$ at exact fit | $m_s$ where all-positive fits (profile) | first failing $m_s$ | PDG |
|---|---|---|---|---|
| mixed | 27.3 MeV | 10, 20, 30 MeV ($\chi^2\le0.01$) | 40 MeV ($\chi^2=95$) | 93.5 |
| $M_Z$ | 12.6 MeV | 3, 5, 8, 12 MeV | 20 MeV ($\chi^2=204$) | 53.3 |

At the PDG value the all-positive fit is off by $\chi^2\approx2700$ (mixed) and $3200$ ($M_Z$), consistent with F404 P4a. **In this model's amplitude reading the all-positive route needs $m_s$ at about a quarter of its value.** Gérard–Goffinet–Herquet needed $m_s(M_Z)$ about 2.5 times *larger*. The two pseudo-mass definitions differ: theirs is the mass-matrix diagonal in a weak basis, this one is the amplitude diagonal. So the two failures are not the same failure, and the sign of the shift is itself a diagnostic between the definitions.

**M5 — GST does not emerge.** With $\lvert V_{us}\rvert$ and $\lvert V_{td}\rvert$ removed from the fit (9 fitted numbers, 9 parameters), the ansatz at universal δ\* reaches $\chi^2<1$ on dozens of disconnected branches. Their $\lvert V_{us}\rvert$ values run from 0.21 to 0.98 (mixed) and 0.20 to 0.83 ($M_Z$). Pinning $\lvert V_{us}\rvert=0.15$ costs $\chi^2=26.5$ (mixed) and $16.8$ ($M_Z$). So the ansatz forbids small Cabibbo mixing but does not predict its value.

The floor is soft. At δ\*, $(\delta^*/3,\delta^*/2)$ and $(0.05,0.05)$ the held-out fit reaches $\chi^2\le1$ from $\lvert V_{us}\rvert\approx0.19$ upward, and $\chi^2=0$ at about 0.205, in both schemes. It is not the Fritzsch lower edge $\sqrt{m_d/m_s}-\sqrt{m_u/m_c}=0.183$: it does not move when $m_u$ is scaled by 4 or ¼. It is not $\sqrt{m_d/m_s}$ either (scratch scan at $(0.05,0.05)$, mixed):

| $m_d$ scaled by | $\sqrt{m_d/m_s}$ | floor ($\chi^2<1$) |
|---|---|---|
| ¼ | 0.112 | no solution up to 0.6 |
| ½ | 0.159 | 0.20 |
| 1 | 0.224 | 0.20 |
| 2 | 0.317 | 0.28 |

The measured $\lvert V_{us}\rvert=0.2250$ sits just above the floor. That is a numerical observation with no mechanism behind it, and it is recorded here as such.

## What this settles for derivation three

| Report criterion | Result |
|---|---|
| Fit PDG 2025 masses and CKM, per sector, both schemes | Done. Fits at $\Delta\chi^2\le1$ in both |
| Count parameters against 10 observables | 9 vs 10, Jacobian rank 9: one genuine dof |
| Test whether GST emerges | **No.** $\lvert V_{us}\rvert$ spans 0.2–0.98 when held out; only a soft floor near 0.2 |
| Fails if it needs $m_s$ far from 93.5 MeV | **Passes** with signed amplitudes ($m_s$ unpulled). **Fails** with lepton-like signs ($m_s\approx27$ MeV) |
| δ at the candidate values | All three fit; none is preferred |

The route survives the test the report set for it and still predicts nothing. With one degree of freedom it reproduces ten inputs and constrains only the angle band F404 already found. For the model this means three things. The route cannot be the *mechanism* for the quark hierarchy without a principle that fixes the $T_{2g}$ texture. The δ coincidences (δ_U ≈ 2/27, δ_D ≈ 1/9) get no support from it: the fit accepts them, and it accepts δ\* equally. And the sign structure is forced, not chosen: no passing solution has a lepton-like down sector.

## Exactness

| Result | Type | Residual |
|--------|------|---------|
| Parameter count 9 vs 10, Jacobian rank 9 | numerical (finite-difference rank) | $\sigma_\text{min}/\sigma_\text{max}\ge5.9\times10^{-3}$ |
| Candidate pairs fit at $\Delta\chi^2\le3.84$ | numerical certificates (explicit parameter vectors) | upper bounds on the minimum |
| Off-band pairs fail | numerical search | $\chi^2\ge617$ |
| All-positive needs $m_s\approx27$ / 12.6 MeV | numerical search | profile grid $\Delta m_s=10$ MeV |
| GST not emergent; soft $\lvert V_{us}\rvert$ floor ≈ 0.19–0.20 | numerical search | not a proof; floor mechanism unknown |

Nothing here is exact beyond what F404 already proved (the trace identity and the $T_{1g}$ requirement for CP). The "fits" results are existence certificates and are robust. The "fails" results are search results.

## Tests

`casim test --id F407-koide-pseudomass-minimal` — 7/7 legs PASS (M1, M2 × 3, M3, M4, M5), about 40 s. The $M_Z$ scheme was run by hand with `--param scheme=MZ`: 7/7 PASS.

Controls (`casim test --control --id F407-koide-pseudomass-minimal`), both measured to red exactly the three M2 legs:
- `t1g=False` → no $T_{1g}$ amplitude, so $V$ is real and $J=0$ (F404 P6), which costs $\chi^2\approx576$ at every angle pair.
- `force_positive=True` → lepton-like amplitudes at the PDG $m_s$ fail everywhere, which is F404 P4a seen from the minimal ansatz.

`python3 src/casim/engine/forks/particles/koide_pseudomass_minimal.py --scans` regenerates the δ landscape and $m_s$ profile in the results JSON (about 30 min; not part of the gate).

## Scope and limits

- **One $T_{1g}$ slot.** "One phase" is implemented as one imaginary antisymmetric amplitude in one of six (sector, pair) slots, chosen by the fit. Other one-phase readings (a common phase on all off-diagonals of one sector, for example) were not tested. They have the same count.
- **The mixed scheme mixes scales.** It is kept because the model's quoted $Q$ values (F76) use it. The $M_Z$ scheme is the physically consistent one, and every conclusion here holds in both.
- **$M_Z$ mass errors** are PDG's relative errors carried over, not Antusch et al.'s own.
- **The $m_s$ profile** is a 10 × 9 grid in $(\delta_U,\delta_D)$ with 3 starts per slot. The boundary between 30 and 40 MeV (mixed) and between 12 and 20 MeV ($M_Z$) is bracketed, not located.
- **The $\lvert V_{us}\rvert$ floor** has no derivation. It is reported as a property of this ansatz at the physical masses, not as a prediction.

## Status

Fork, `fork_live`. Derivation three of the flavour report is **done**: the route passes its failure test and is non-predictive. CL316 is extended with this finding. What would change the verdict is a lattice principle that fixes the $T_{2g}$ texture (removing parameters). The report's derivation four was the candidate source for a sector-dependent texture. F405 found identity-class colour and charge dressing sector-blind, and left three channels open: $A_{1g}$/$E_g$-weighted stiffness, family charges, and a sector-dependent amplitude in the unitarity-cap regime.
