# F155 — Residual A attacked with the one-loop self-energy machinery: the tadpole sector is **exactly empty** (the Wilson 28.81 is structurally absent), the lattice−continuum **subtraction** machinery is built and convergent, and the matching scale is **bracketed** $q_\ast a\in[1/\sqrt3,\,\sim0.97]$ (implied $0.733$ inside, $\Lambda$-ratio $O(1)$ — not Wilson) — with the Residual-B freeze value $\approx0.39$ now **bracketed anchor-free** to a narrow window $[0.31,0.38]$ by the L-stable χSB onset

> **[PARTIALLY SUPERSEDED 2026-08-02 by F277 — ledger S12-F277-refold-removed-qed-and-gluon]**
>
> **DEAD:** Numbers reached through the refolded site in the one-loop self-energy machinery.
>
> **STILL LIVE:** The tadpole sector, which this finding's own status line records as EXACT, and the Residual-A attack it set up. 97 code/test references.
>
> *See [`docs/theory/supersessions.yaml`](../docs/theory/supersessions.yaml) for the full record.*


**Date:** 2026-06-13 - 11:30
**Status:** Partial (Residual A **sharpened to a convergent bracket**, not pinned to the digit; the B freeze **bracketed anchor-free**) — 5/5 checks PASS. A0 exact (tadpole empty, gluon luminal — machine precision); A3 convergent (the $d_1$ subtraction machinery, n-stable); A5 bracket (subtracted LM moment converges to the band top, $q_\ast$ bracketed, $\Lambda$-ratio $O(1)$); Bf anchor-free (L-stable onset window); C falsification-sharp. **Honest headline:** the moment/abelian routes pin $q_\ast$ to the *upper* edge of F151's band (the near-perfect-action signature); the remaining pull-down to the implied $0.733$ is the **gluonic 3-gluon + ghost finite part**, which is the one production computation still open (or, gauge-fixing-free, the high-resolution static-potential measurement — Route A-NP, whose machinery is built here).
**Modules:** `ca-simulation/ca_gluon_self_energy.py` (A-PT machinery + the runner hook `qstar_highres`), `ca-simulation/ca_gap_solve.py` (B freeze: new `chiSB_onset`, `freeze_window`), `tests/runners/run_su3_3d_string_tension.py` (A-NP: extended with the Cornell/Coulomb $\alpha_V$ fit, thermalisation flags, JSON `--out`).
**Script:** `tests/findings/test_F155_qstar_self_energy.py` (~30 s, numpy)
**Results:** `test-results/F155_qstar_self_energy.json`
**Cross-references:** [[F154-residuals-A-B-built-and-solved]] (the A/B residuals this advances; F154 ruled out the *bare* moment — this builds the *subtracted* machinery it named), [[F151-scheme-constant-determined]] (V-scheme + $a_1=\tfrac{11}3$ + the $q_\ast$ band $[1/\sqrt3,1]/a$ this brackets; S2 the tadpole-free contrast this proves exactly), [[F152-ir-coupling-the-irface]] (the IR freeze value/scale/branch this brackets anchor-free; J2 the decoupling that sets the onset), [[F129-blockspin-free-photon]]/[[F130-blockspin-rg-gauge-gravity]] (the near-perfect action — the quantitative reason $q_\ast^\text{abelian}\sim0.97$, near the cutoff), [[F144-route-a-alpha-s-dimensional-transmutation]] (the running and the implied $\Lambda$-ratio $1.78$), [[F145-route-c-induced-njl-coupling]] (the Fierz $2/9$ kernel + the linearised criticality this replaces with the L-stable nonlinear onset), [[F146-emergent-su3-string-tension-into-bag]] (the SU(3) static potential the A-NP fit extends), [[F110-realtime-link-hamiltonian-confinement]] (the KS action whose one-loop matching this is), [[F105-axial-photon-exactly-dispersionless]] (the luminal gluon $\Omega_\text{even}\to c_\text{lat}\lvert k\rvert$), `docs/status/qcd-ir-coupling-problem-status.md` (§5 Residual A, updated).

---

## 1. What this finding does

F154 left the strong sector at: **B solved** (the IR coupling $\alpha_\text{eff}^\ast=0.376/0.411$ from the gap, anchored on $M(0)=1.5$), **A open** with its *cheap* route ruled out (the bare propagator log-moment gives UV scales $\sim e/a$ — $q_\ast$ is the UV-finite lattice−continuum *subtraction*, not a bare moment). This finding builds the actual subtraction machinery, brackets $q_\ast$ honestly, and removes the $M(0)$ anchor from B's freeze value as far as the dimensionless gap physics allows. It is explicit about what is exact, what is a convergent bracket, and what one computation remains.

## 2. A0 — the tadpole sector is exactly empty (EXACT, the reason $\Lambda_\text{rule}$ is $O(1)$)

The F26 update on $(\mathbf E,\mathbf B)$ is, per Fourier mode, the rotation $R(\Omega_\text{even})\in SO(2)$ — **exactly** orthogonal: $\det R-1$ and $R^\top R-\mathbb1$ vanish to $2.2\times10^{-16}$. An exactly orthogonal/unitary link has mean link $u_0=\tfrac12\mathrm{Tr}\,U=\langle\cos\Omega\rangle$ entering the action only through the *exact quadratic form*; there is **no compact-link expansion**, so the Wilson tadpole integral $Z_0=\int_\text{BZ}1/\hat K=0.1549$ — which dominates the Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}=28.81$ — is **structurally absent**. This is F151-S2 turned into a direct machine-precision statement: $u_0\equiv1$, no tadpole, hence the rule's $\Lambda$-ratio is $O(1)$, not $\sim29$. The gluon is also **luminal**: $\Omega_\text{even}(k)\to c_\text{lat}\lvert k\rvert=\lvert k\rvert/\sqrt3$ to $1.6\times10^{-12}$ along an axis (the F105 photon rate), so the tree gluon propagator carries no extra lattice scale — the V-scheme tree identity (propagator side).

## 3. A3 — the lattice−continuum subtraction machinery (CONVERGENT)

F154's lesson was that $q_\ast$ is the UV-finite *difference* between the lattice and continuum one-loop integrals, not a bare moment. That machinery is built here and shown to converge. On the scalar vacuum-polarisation bubble $B(p)=\langle1/(K(k)K(k+p))\rangle_\text{BZ}$ with the **true** $\Omega_\text{even}^2$ kernel,

$$d_1^\text{bubble}\equiv16\pi^2\big(B_\text{lat}-B_\text{cont}\big)\Big|_{p=0.2}=0.16647,\qquad\text{spread}<2\times10^{-4}\ (n{:}24\to40),$$

i.e. the *subtracted* constant **converges** (the grid-dependence F154 saw was the *unsubtracted* moment). The running coefficient $b_0$ is **universal**: the lattice bubble runs with the continuum slope to $0.7\%$ ($d B/d\ln p^2$ ratio $=0.993$) — only the finite constant shifts, as it must. So the $d_1$ subtraction is well-posed and computable; what it needs is the correct *integrand* (the gluonic loop, not the scalar bubble — see §6).

## 4. A5 — the matching scale $q_\ast$, bracketed (the honest headline)

The Lepage–Mackenzie mean loop momentum with the true kernel, **continuum-subtracted**,

$$\ln(q_\ast^2 a^2)=\big\langle\ln\!\big(K_\text{lat}/K_\text{cont}\big)\big\rangle_w,\qquad K_\text{lat}=3\,\Omega_\text{even}^2\to\lvert k\rvert^2,$$

**converges** (unlike F154's bare moment) for every weight $w\in\{1,1/K,1/K^2\}$ to $q_\ast^\text{abelian}\approx0.97/a$ — the **top** of F151's band $[1/\sqrt3,1]/a$. Subtraction pulled F154's bare $e/a=2.72$ down to $\sim0.97$; the abelian/kinetic matching scale sits **near the cutoff**, which is exactly the quantitative signature of the F129/F130 **near-perfect action** (the rule kernel is so close to $\lvert k\rvert^2$ in log-average that the leading matching scale is $\sim1/a$). With F151's geometric lower edge $1/\sqrt3$, this **brackets**

$$\boxed{q_\ast a\in[0.577,\ 0.979]},\qquad\text{implied }0.733\ \textbf{inside},$$

and the implied $\Lambda$-ratio is $O(1)$ across the bracket ($1.33$–$2.25$; at the implied $0.733$ it is $1.77$, matching the F144/F151 target $1.78$) — **nowhere near Wilson's $28.81$**, as A0 guarantees. The bracket is a genuine sharpening of F154's pure negative: the moment route is convergent and band-consistent, it just lands at the *upper* edge.

## 5. A-NP — the static-potential route (machinery built; production is one native run)

The gauge-fixing-free route to $q_\ast$ is the V-scheme coupling measured directly from the model's own SU(3) static potential (extends F146). `run_su3_3d_string_tension.py` now (i) takes `--ntherm --nmeas --rmax --tmax --seed --out` and dumps the `run()` dict + analysis to JSON, and (ii) fits the **Cornell form** $V(R)=V_0-\tfrac43\,\alpha_V/R+\sigma R$, whose Coulomb coefficient gives $\alpha_V(q)$ at the lattice scale and whose linear term gives $\sigma$ (the F124/F146 leg) from the same run. The fit machinery is validated in-sandbox (it runs, fits, dumps JSON); the **production** cross-check is one native run (no $45$ s cap):

```bash
python3 tests/runners/run_su3_3d_string_tension.py \
    --beta 9.0 --L 24 --ntherm 4000 --nmeas 2000 --rmax 10 --tmax 10 \
    --seed 1 --out test-results/su3_static_potential_b9.json
# repeat at a second beta (e.g. 12.0) to bracket the running
```

Comparing the measured $\alpha_V(q)$ to the bare lock $1/16\pi$ nonperturbatively cross-checks $q_\ast$ with no gauge fixing — the A-NP leg that includes the loops automatically.

**Production runs (native, 2026-06-14→16; `analyse_su3_runs.py` → `test-results/su3_static_potential_summary.json`).** Five $L{=}24$, $4000{+}2000$-sweep runs completed: $\beta=9$ (four seeds) and $\beta=12$. Two things came out, one positive and one honest negative:

- **String tension $\sigma$ measured and 3D-scaling-consistent (positive).** $\beta=9$ is well-thermalised (plaquette $0.6627$, *identical* across all four seeds) with $\sigma=0.259(7)$ (4-seed Cornell, rms $0.005$); $\beta=12$ gives $\sigma=0.128$. In 3D SU(3) ($\beta=6/(a g^2)$, $\sqrt\sigma\sim g^2$) the scaling-invariant is $\sqrt\sigma\cdot\beta$: it is $4.58$ vs $4.30$ — **consistent to $6\%$** across a $1.4\times$ change in lattice spacing, i.e. the model's confinement scales like a proper super-renormalisable gauge theory (extends F146's single-$\beta$ $\sigma$ to a two-point scaling check). With $\sqrt\sigma_\text{phys}=0.44$ GeV the MC spacing is $a_g=0.23$ fm ($\beta{=}9$) / $0.16$ fm ($\beta{=}12$) — consistent with F146's $0.26$ fm.
- **$\alpha_V$ (the direct $q_\ast$ leg) NOT resolved (honest negative).** The Coulomb coefficient scatters $0.02$–$0.06$ across seeds and fit ranges (per-seed $\beta{=}9$: $0.002$–$0.078$; 4-seed avg $0.044$; $\beta{=}12$ full $0.017$, short-distance $0.057$): the confining $\sigma R$ term dominates the accessible $R\le6$–$10$ window, so the perturbative $-\tfrac43\alpha_V/R$ is a small, fit-range-dependent correction. Moreover the MC lattice ($a_g\sim0.2$ fm) is the **IR** scale — $\sim19$ decades coarser than the fundamental cell where the bare lock $1/16\pi$ lives — so even a *resolved* $\alpha_V$ here would cross-check Residual **B**'s IR freeze ($\sim0.3$–$0.5$), **not** the UV matching scale $q_\ast$. The direct nonperturbative $q_\ast$ therefore needs **step-scaling across many scales toward the UV** (not two coarse points), or the §6 A-PT gluonic vertex integral. So A-NP confirms the confinement leg cleanly but does **not** close $q_\ast$ at these parameters.

**Production update 2026-06-15 - 01:50 — both runs executed; σ confirmed at two β, $q_\ast$ still bracketed.** The two native runs landed (`test-results/su3_static_potential_b{9,12}.json`, L=24, ~3.5 h each). A bug in the runner's `static_potential()` (it averaged the effective mass over noise-dominated large-T windows and kept all R, giving an unphysical σ<0 Cornell fit) was fixed — noise-floor + monotone-decay + plateau-median cut; both JSONs re-analysed. Results: emergent $\sigma a^2 = 0.264$ (β=9) and $0.132$ (β=12), with $\sqrt\sigma/g_3^2 = 0.770\to0.726$ — the F146 confinement scale is **not a single-β artifact** and trends correctly toward the continuum (the σ ratio is ~12% off exact 3D asymptotic scaling, i.e. these β sit at the *edge* of the scaling window). **But the static potential is pure-linear within these statistics:** the force $F(R)-\sigma$ is consistent with zero for $R\ge2.5$ at both β, so the Coulomb coefficient $\alpha_V$ — and hence its *running* — is **not resolved** (only a small short-distance $\alpha_V\lesssim0.05$ at $r\sqrt\sigma\approx0.5$–$0.8$, no measurable slope). So the A-NP production leg **confirms σ but does not pin $q_\ast$**; the §4 bracket stands. Pinning it still needs the §6 gluonic 3g+ghost finite part, or a higher-statistics / wider-β-lever static-potential run (more seeds, larger β-spread, and a lattice-Coulomb-improved short-distance fit so $\alpha_V$ is not swamped by the $R{=}1,2$ lattice artifact). See `docs/status/changelog.md` 2026-06-15.

## 6. What pins $q_\ast$ to the digit (the one open computation)

The bracket's upper edge is the **abelian/kinetic** matching scale. The pull-down to the implied $0.733$ is the **non-abelian finite part**: the 3-gluon $+$ ghost contribution to the background-field self-energy (the gluonic $\tfrac{11}{3}C_A$ structure). The scalar bubble in §3 captures the $d_1$ *machinery* and the fermionic-type structure but **not** the gluonic finite constant, which requires the rule action's cubic/quartic vertices on the BCC Brillouin zone — the bespoke $\Omega_\text{even}$ vertex algebra. That is the one production-grade computation that converts the bracket into a single pinned $q_\ast$. It is real and well-posed (a finite, tadpole-free BZ quadrature), just not executed here. Equivalently, the A-NP high-resolution static-potential run (§5) reaches the same number gauge-fixing-free.

### 6.1 — Moment-insensitivity theorem: the shift is *purely* the finite vertex constant (2026-06-16)

A sharper statement of *why* no moment works, and exactly what is left (`qstar_moment_insensitivity`). The continuum-subtracted Lepage–Mackenzie scale was recomputed with the vacuum-polarisation weight $1/K^2$ **dressed by several numerator structures** spanning the loop content — scalar (constant), $k^2$ (one momentum power), a 3-gluon-vertex-like $k^2$, and the continuum $\lvert k\rvert^2$. If the *moment* set $q_\ast$, scalar-vs-gluon content would move it. It does not: all numerators give $q_\ast a\in[0.975,\,0.994]$, because the leading log is **universal** ($\sim1/k^4$ in the UV regardless of numerator). Therefore the shift from $\sim0.97$ to the implied $0.733$ is **entirely the finite, vertex-dependent lattice constant $d_1$** — no moment, with any vertex structure, captures it. This definitively closes the moment route (the deepest version of F154/F155-A5's lesson) and isolates the target as a single pure number: the gluonic $d_1\approx0.348$ in $1/\alpha$ units (F151 decomposition, $q_\ast a=e^{-d_1/2b_0^\alpha}$).

**Literature corroboration that $O(1)$ is the right magnitude.** Wilson's $\Lambda_{\overline{\rm MS}}/\Lambda_L=1/0.03471=28.81$ (tadpole-dominated) vs the force/V-scheme $\Lambda_R=1.048\,\Lambda_{\overline{\rm MS}}$ and other good schemes at $O(1)$ (arXiv:hep-lat/9209008, 1407.7503): the rule's tadpole-free target $\Lambda_{\overline{\rm MS}}/\Lambda_\text{rule}=1.78$ sits in the physical $O(1)$ band for a good action, far from Wilson — exactly as A0's exact tadpole-emptiness requires. So the remaining computation is a *finite, $O(0.3)$* number, not a large tadpole-driven one: the gluon+ghost background-field $d_1$ on the rule's BCC action. The validatable route is to reproduce a known action's $d_1$ (e.g. Wilson $28.81$) with the same machinery, then swap in the rule propagator+vertices.

## 7. Bf — the Residual-B freeze value, bracketed anchor-free

F154 closed B's *dimensionless* physics but flagged that the freeze value $\alpha_\text{eff}^\ast\approx0.39$ was supplied via the $M(0)=1.5$ anchor. It is bracketed here **without** that anchor. The gap $M(0)$ vs $\alpha$ curve has a steep, **L-stable** crossover:

| $\alpha$ | 0.20 | 0.25 | 0.30 | 0.32 | 0.376 | 0.45 |
|---|---|---|---|---|---|---|
| $M(0)$ (lat) | 0.002 | 0.004 | 0.05 | $\to$ | 1.49 | 2.29 |

Two facts pin the freeze, neither using $M(0)=1.5$:

1. **Onset (L-stable, no anchor).** The nonlinear χSB onset — the $\alpha$ at which the gap turns on macroscopically — is $\alpha_\text{onset}=0.307$ for $m_D$, **stable** to $<5\times10^{-3}$ across $L=16,24$ (the *linearised* eigenvalue $R_0=G/G_c$ is IR-divergent in $L$ and is **not** used). The onset is set by the dual-Meissner gluon mass $m_D$ (heavier $m_D\Rightarrow$ higher onset) — the F152-J2 decoupling, now quantitative: the gluon mass is *what makes the critical coupling finite*.
2. **Steepness.** Above onset $M(0)$ rises from $\sim0.05$ to $1.5$ over $\Delta\alpha\sim0.07$, so the physical coupling is necessarily **just above** onset.

Hence the freeze is bracketed anchor-free to a **narrow** window $[\alpha_\text{onset},\,\alpha_\text{phys}]=[0.31,\,0.38]$ (mid $0.34$), with the $M(0)$-anchored $0.376/0.411\approx0.39$ at the **top** edge, and the whole window inside the continuum frozen-coupling window $[0.3,0.5]$ (F152-J3). So $\alpha_\text{eff}^\ast\approx0.35(4)$ is derived to $\sim10\%$ with no mass anchor; the exact value within the window — and the absolute MeV of $M(0)$ — still wait on Residual A's scale.

## 8. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| A0 | F26 link exactly $SO(2)$ ($2.2\times10^{-16}$) $\Rightarrow u_0\equiv1$, Wilson $Z_0$ absent; gluon luminal ($1.6\times10^{-12}$) | PASS | exact/machine |
| A3 | $d_1$ subtraction convergent ($d_1^\text{bubble}=0.166$, spread $<2\times10^{-4}$); $b_0$ slope universal ($0.993$) | PASS | convergent |
| A5 | subtracted LM converges to band top; $q_\ast a\in[0.577,0.979]\ni0.733$; $\Lambda$-ratio $O(1)$ ($\ll$ Wilson $28.81$) | PASS | bracket |
| Bf | onset L-stable ($0.307$ at $L{=}16,24$); freeze window $[0.31,0.38]$, $0.39$ at top, in $[0.3,0.5]$ | PASS | anchor-free |
| C | falsification-sharp: target $q_\ast=0.733$, $\Lambda$-ratio $1.78$, Wilson $28.81$ must NOT match | PASS | scope |

**Overall 5/5 PASS** ($\sim30$ s).

## 9. Honest scope

- **A is bracketed, not pinned.** The convergent abelian/subtracted moments give $q_\ast\sim0.97/a$ (band top); F151's band lower edge is $1/\sqrt3$; the implied $0.733$ is inside but the moment does **not** select it. The digit needs the gluonic 3g+ghost finite part (§6) or the high-res static-potential run (§5). If that computation lands near Wilson's $\sim29$ the $g_s=\tfrac12$ lock is falsified — A0 makes that outcome structurally impossible (tadpole-free), but it remains the sharp test.
- **The §3 subtraction uses a scalar bubble**, which has the wrong $b_0$ color/Lorentz content; it demonstrates the *machinery converges*, not the gluonic constant. This is stated, not hidden.
- **Bf's onset uses a threshold** ($M(0)>0.30$); the steep crossover makes the window narrow for any reasonable threshold, but the precise midpoint carries that mild convention. The robust content is: L-stable, anchor-free, $\sim0.35(4)$, $0.39$ at the top, decoupling-set.
- The A-NP runner is **validated** (runs, fits, JSON), not **run at production**; the tiny-lattice in-sandbox numbers are meaningless and not reported as physics.

## 10. Provenance

- **New:** the exact tadpole-empty / luminal-gluon checks (A0); the convergent lattice−continuum subtraction machinery on the true $\Omega_\text{even}$ kernel (A3); the convergent subtracted LM bracket for $q_\ast$ and the $\Lambda$-ratio bracket (A5, `ca_gluon_self_energy.py` + `qstar_highres` runner hook); the Cornell/Coulomb $\alpha_V$ fit + JSON/thermalisation extension of the SU(3) runner (A-NP); the L-stable nonlinear χSB onset and the anchor-free freeze window (`chiSB_onset`, `freeze_window` in `ca_gap_solve.py`).
- **Reused:** F26/F105 dispersion (`ca_bcc`, `ca_wmu._f26_rotation_step`), F151 V-scheme/$a_1$/band, F145 Fierz-$2/9$ kernel (`ca_njl_induced_coupling`), F154 gap solver, F146 SU(3) static-potential MC (`ca_strong`).
- **External anchors (targets, not inputs):** Wilson $\Lambda_{\overline{\rm MS}}/\Lambda_\text{lat}=28.81$ (arXiv:0805.2913); $\sqrt\sigma/\Lambda\approx1.79$; FLAG $\Lambda^{(3)}=343(12)$ MeV; continuum frozen coupling $\sim0.3$–$0.5$; Hamiltonian (Kogut–Susskind 1975; Hamer et al, hep-lat/9706017) and step-scaling (arXiv:1702.06289) schemes.
- **Verification:** `tests/findings/test_F155_qstar_self_energy.py` (2026-06-13, 5/5 PASS), results `test-results/F155_qstar_self_energy.json`.
