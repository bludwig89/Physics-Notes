# F137 — The live colour-dielectric flux-tube field: the proton digs its own confining bag

**Date:** 2026-06-11 - 20:10
**Status:** Confirmed — 4/4 checks PASS. B1 quantitative (bound vs dispersing, norms machine-precision); B2 structural (live, melts core); B3 quantitative (connected tube + monotone ≈linear confining E(R)); B4 caveat (the self-sourced bag also self-traps a *single* colour charge — generic self-trapping, not singlet confinement; added 2026-06-12, see audit).
**Module:** `src/casim/particles/channel.py` (new `ColourBagChannel`, type `colour_bag`; `_gauss_smear`; `confine.field` mode on the quark).
**Scenario:** `scenarios/proton_bag.yaml`.
**Test:** `tests/findings/test_F137_live_flux_tube.py` (4/4, ~95 s).
**Results:** `test-results/casim_proton_bag.json`.
**Cross-references:** [[F86-colour-dielectric-dual-superconductor]] (the dielectric ε_c / dual-superconductor mechanism and the exact BPS σ=2πv²n this realises dynamically), [[F136-colour-triplet-dirac-quark-confinement]] (the colour quarks this confines), [[F135-realspace-scalar-confinement]] (the scalar-mass mechanism, now field-sourced not geometric), [[F70-gradient-flow-confinement-string-tension]] (string tension), `docs/roadmaps/roadmap-unified-real-space.md` (U3 Part 2).

---

## 1. What this closes

F135/F136 confined the proton with a **posited geometric** string ($m_\text{eff}=m+\sigma|x-R_\text{cm}|$ toward the singlet COM). This finding makes the confining field **live** — sourced dynamically by the quarks' own colour charge, the F86 colour-dielectric / dual-superconductor mechanism realised in real time — so the proton **digs its own bag** rather than being held by a hand-built potential.

## 2. The mechanism — a self-generated MIT bag (F86 in real time)

The QCD vacuum is a colour-magnetic condensate; by the dual Meissner effect it expels colour-electric flux (F86). The new `colour_bag` channel implements this dynamically each tick:

$$\rho(x)=\sum_\text{quarks}\lVert J_\text{colour}(x)\rVert,\quad \phi=G_\lambda*\rho,\quad f^2(x)=e^{-\phi/\phi_0},\quad \boxed{S(x)=M_\text{bag}\,f^2(x)},\quad \varepsilon_c=1-f^2.$$

The condensate $f$ is **melted** ($f\to0$, $\varepsilon_c\to1$) where the quark colour charge sits — the bag the quarks dig — and **full** ($f\to1$, $\varepsilon_c\to0$) in the vacuum, where the bag wall mass $S\to M_\text{bag}$ expels the quarks (F86's $\varepsilon_c\to0$ = infinite effective mass in the vacuum). The quarks read $S(x)$ as their F135 Lorentz-scalar confining mass (`confine: {field: bag}`). The smear range $\lambda$ is the F86 dual-London penetration depth $\lambda=1/ev$. Nothing is posited about the quark positions — the field tracks them through $J_\text{colour}$.

## 3. The result (B1–B3)

**B1 — the live bag binds.** With $M_\text{bag}=8,\ \phi_0=0.01,\ \lambda=1.5$, the `uud` cluster RMS plateaus at $\approx2.95$ (tighter than the geometric string's $3.7$) while the free control disperses to $\sim8$; norms conserved to $1.7\times10^{-14}$.

**B2 — it is live.** The condensate is melted in the dug-out core ($\varepsilon_{c,\text{core}}\approx0.52$) and the bag wall is non-flat ($S_\text{min}\!\ll\!S_\text{max}$, $\sim3.8$ vs $8.0$); the bag follows the quark colour charge each tick.

**B3 — a flux tube with an approximately linear potential.** For two static colour charges at separation $R$, the condensate melts into a **connected channel** between them, and the confining bag energy rises monotonically and roughly linearly over the tube range:

| $R$ | $\varepsilon_c$ midpoint (tube depth) | bag energy $E(R)$ |
|---|---|---|
| 1 | 0.88 | 1175 |
| 2 | 0.84 | 1206 |
| 3 | 0.78 | 1245 |
| 4 | 0.69 | 1282 |
| 5 | 0.56 | 1311 |
| 6 | 0.42 | 1329 |
| 8 | 0.17 | 1343 |

$E(R)$ is linear-in-$R$ ($\Delta E\approx30\text{–}37$ per unit) over $R\lesssim4$ — the **constant energy-per-length flux tube** of confinement — and the midpoint stays melted (connected tube) up to $R\approx2\lambda$, beyond which it **pinches off** (a string-breaking-like cutoff). This is the F86 dual-superconductor signature realised dynamically.

## 4. Checks

| # | Check | Tier | Result |
|---|---|---|---|
| B1 | live bag binds the colour-quark cluster vs free; norms | quantitative / machine | bag max $<3.0$ vs free $>6$; drift $1.7\times10^{-14}$ |
| B2 | bag is live: melts the condensate in the core | structural | $\varepsilon_{c,\text{core}}\approx0.52$; $S_\text{min}\ll S_\text{max}$ |
| B3 | connected flux tube + monotone ≈linear $E(R)$ | quantitative | midpoint melted to $R\!\approx\!2\lambda$; $E(R)$ linear $\Delta\!\approx\!33$/unit |
| B4 | single colour charge ALSO self-traps (caveat) | quantitative | lone-quark RMS $\approx2.2$ vs free $\approx8.2$ — generic self-trapping, not singlet confinement |

## 5. The honest open edge

The bag is a **mean-field** dielectric: the condensate responds to the colour-charge density through a fixed smear ($\lambda$), not a self-consistent dual-Ginzburg–Landau back-reaction. Consequently the flux tube is connected and linear only out to $\sim2\lambda$, then pinches (the genuine *asymptotic* linear law, $\sigma=2\pi v^2 n$ exactly, is F86's analytic BPS result, which this dynamical bag approximates locally). Promoting it to the self-consistent F86/F110 flux-tube field (the condensate expelled *by* the flux it confines, closing the loop) is the deeper remaining step. **[Closed by F139, 2026-06-11]:** the self-consistent dual-Ginzburg–Landau back-reaction is built — the confined colour-electric flux melts the condensate via $\partial_\tau f\supset-f\lVert\mathbf D\rVert^2/\varepsilon_c^2$, the two fields solved to mutual consistency; the tube stays connected and linear past the $2\lambda$ pinch (`findings/F139-self-consistent-dual-gl-backreaction.md`). Scale separation (F134 §6) still gates physical fm/eV — U4.

**Caveat — the bag self-traps a single charge (audit 2026-06-12).** The bag mass $S(x)=M_\text{bag}f^2(x)$ is sourced by the quarks' *own* colour density, so it is a self-attracting scalar well: it traps **any** colour-charge blob, including a single isolated quark (a lone charge digs its own well and self-traps to RMS $\approx2.2$ vs free dispersal $\approx8.2$ — check B4). The binding is therefore *generic self-trapping*, not enforcement of colour-singlet confinement — a free isolated colour charge should not exist as a finite object, yet this mean-field bag holds one. Two consequences: (i) the "proton holds together" result is the MIT-bag self-trapping mechanism, not a derivation of $\mathbb Z_3$ singlet selection (that remains F97/F99's centre-closure argument); (ii) the confinement **scale** is still imported — $M_\text{bag},\phi_0,\lambda$ here, $\sigma=2\pi v^2 n$ from F86 in F139 — not generated by the gauge sector. The open step is to feed a string tension *measured from the model's own SU(3) gauge dynamics* (the F70 area law, emergent $\sigma(\beta)=-\ln w(\beta)$, extended off 2D) into the bag, rather than positing the scale. See `docs/audits/2026-06-12-emergent-bound-states-vs-manufactured.md`.

## 6. Ledger

New `colour_bag` channel (`ColourBagChannel`) + `_gauss_smear` + the `confine.field` quark mode; scenario `proton_bag.yaml`; suite `tests/findings/test_F137_live_flux_tube.py` (4/4 — B4 single-charge self-trapping caveat added 2026-06-12). With U3 Parts 1–2 built, the proton is a real-space colour object confined by a live dielectric field. Exactness rows: Tier-3 #81 (live-bag binding vs free), #82 (connected flux tube + monotone linear-trend $E(R)$, F86 signature).
