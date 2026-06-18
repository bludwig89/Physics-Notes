# F145 — Route C: the NJL coupling as an induced coupling — exact Fierz $c=\tfrac29$ (all four chiral channels), a bare-coupling no-go, and χSB guaranteed by Route A's running

**Date:** 2026-06-12 - 13:05
**Status:** Confirmed (mechanism closed; magnitude bracketed) — 5/5 checks PASS. N1 machine-exact (the full Fierz + Fock identities); N2 machine (contact anchor); N3 a **decisive negative** (bare coupling subcritical); N4 a **structural positive** (running coupling supercritical — χSB forced); N5 the quantified residual.
**Module:** `ca-simulation/ca_njl_induced_coupling.py`
**Script:** `tests/findings/test_F145_route_c_induced_njl.py` (~60 s, numpy)
**Results:** `test-results/F145_route_c_induced_njl.json`
**Cross-references:** [[F116-njl-calibration-bz-cutoff-induced-G]] (NJ4 — the mechanism + order-of-magnitude this sharpens and partly corrects), [[F144-route-a-alpha-s-dimensional-transmutation]] ($g_s^2=\tfrac14$ derived; the running that makes χSB possible), [[F117-gap-coupled-dielectric-gluon-propagator]] (the gap-massive exchange kernel; the $\varepsilon_c$ variants), [[F88-colour-condensate-from-model]] (the measured $m_D=0.532$), [[F77-njl-gap-rpa-selfconsistent]] (the fitted targets $G/G_c=1.277$, $\hat g=2.10$), [[F124-sqrt-sigma-over-fpi-two-qcd-calibrations]] (the shared scale-setting residual), `docs/theory/qcd-calibration-derivation-routes.md` (Route C brief).

---

## 1. What this closes (and what it sharpens)

F116 NJ4 identified the mechanism — $G$ is induced by integrating out the dielectric/dual-Meissner gluon — but left "the full momentum-dependent Fierz reduction integrated against the lattice loop" as the open coefficient, quoting $G\sim\tfrac49 g_s^2/M_g^2$. This finding executes that computation exactly and finds the story is sharper than NJ4 assumed: the corrected coefficient and the momentum-resolved kernel make the **bare** coupling decisively *sub*critical, and chiral symmetry breaking exists **only because** the coupling runs — i.e. Route C *requires* Route A (F144). The two routes compose into a single statement: **asymptotic freedom run backwards is what switches on the chiral condensate.**

## 2. N1 — the exact Fierz: $c=\tfrac29$, and the F77 form is *forced*

Full operator algebra in the 24-dimensional one-quark space (Dirac₄ × colour₃ × flavour₂), no Fierz tables — the exchanged-pairing projection of $\sum_{\mu,a}(\gamma^\mu T^a)\otimes(\gamma_\mu T^a)$ computed directly:

$$\sum_{\mu,a}(\bar q\gamma^\mu T^aq)^2 \xrightarrow{\ \text{Fierz}\ } \tfrac29\Big[(\bar qq)^2+(\bar qi\gamma_5\vec\tau q)^2+(\bar q\vec\tau q)^2+(\bar qi\gamma_5q)^2\Big]+\dots$$

with $c=\tfrac29$ in **all four** chiral channels to $8\times10^{-17}$ (spread $6\times10^{-17}$). Two consequences:

1. **The induced interaction is exactly $U(2)_L\times U(2)_R$ symmetric** — the F77 NJL form is not a modelling choice; it is what one-gluon exchange Fierzes into. (The Goldstone pion's existence is thereby traced to the gauge sector's structure.)
2. **NJ4's $\tfrac49$ is corrected.** The decomposition is $\tfrac29=\underbrace{\tfrac49}_{\text{colour}}\times\underbrace{1}_{\text{Dirac }V\to S}\times\underbrace{\tfrac12}_{\text{flavour}}$, and with the second-order effective Lagrangian $\mathcal L=-\tfrac{g^2}{2}\,j\!\cdot\!D\!\cdot\!j$ the induced contact is $G=\tfrac29\cdot\tfrac{g^2}{2M_g^2}=\tfrac{g^2}{9M_g^2}$ — a factor 4 below NJ4's quote. The Fock-kernel identity $\sum\gamma^\mu T^a\,\mathbb 1\,\gamma_\mu T^a=4C_F\,\mathbb 1=\tfrac{16}{3}\mathbb 1$ is exact (off-diagonal $=0$).

## 3. N2 — the contact anchor (machine)

In the contact limit the induced gap equation reduces to the F116 NJ2 lattice-BZ machinery, with criticality eigenvalue $R\equiv G/G_c=g_\text{contact}\langle K^{-1/2}\rangle_\text{BZ}$: analytic value $=$ power-iteration eigenvalue to $5\times10^{-15}$. All later numbers use this verified operator.

## 4. N3 — the bare-coupling no-go (decisive)

With the **derived** bare coupling $g_s^2=\tfrac14$ (F144 A1) and the **measured** dual-Meissner mass ($m_D=0.532$ F88; $0.727$ F117), the momentum-resolved kernel $D(q)=1/(K(q)+M_g^2)$ — the F117 gap-massive propagator — gives

$$R_\text{resolved}=0.099\ (m_D{=}0.532)\,/\;0.075\ (m_V{=}0.727)\ \ll1.$$

**The bare rule coupling cannot break chiral symmetry.** NJ4's near-criticality ($G/G_c\approx1$) was an artifact of (contact approximation, ~10×) × (the $\tfrac49$ overcount, 4×): the contact value at the corrected coefficient is $R=1.14/0.61$, and resolving the momentum dependence collapses it. The F117 dielectric enhancement helps but cannot rescue it ($\varepsilon_c=0.52\Rightarrow R=0.14$; even $\varepsilon_c=\tfrac14\Rightarrow R=0.235$). This is the χSB mirror of F124's "bare rotor ≠ condensed vacuum" and exactly what asymptotic freedom demands: at the UV coupling, nothing condenses.

## 5. N4 — Route A × Route C: χSB is guaranteed by the running (structural)

Replacing $g^2\to g^2(\mu(q))$ with Route A's running at the exchange virtuality, $\mu(q)=\sqrt{K+M_g^2}\cdot(\Lambda_\text{NJL}/\pi)$ (IR-frozen, $\mu_\text{fr}\in[0.40,0.65]$ GeV scanned — the gap-massive propagator justifies freezing at/below the dual-Meissner scale; $\Lambda^{(3)}\in\{272\ \text{(F144 1-loop)},343\ \text{(FLAG)}\}$ MeV):

$$R_\text{running}=2.6\text{–}15\ \gg1\quad\text{at both measured }m_D.$$

Chiral symmetry breaking is **forced** by the RG growth F144 derived. The criticality condition is the clean derived inequality

$$\alpha_\text{eff}\ \ge\ \alpha_\text{crit}(M_g)=\frac{1}{4\pi R_0(M_g)}=0.200\ (m_D{=}0.532)\,/\;0.266\ (m_V{=}0.727),$$

with $R_0$ the pure kernel-geometry eigenvalue. The model's $\alpha_s$ passes through $\alpha_\text{crit}$ on its way to the chiral scale — the condensate switches on at a derived rung of the Route-A ladder, not by fiat.

## 6. N5 — the residual, quantified and bracketed

The F77 fit $G/G_c=1.277$ corresponds to $\alpha_\text{eff}=R_\text{fit}/(4\pi R_0)=0.256$ ($m_D{=}0.532$) / $0.340$ ($m_V{=}0.727$) — squarely inside the model's running band at the chiral scale, and bracketed:

$$\underbrace{0.075\text{–}0.10}_{\text{bare (no-go)}}\ <\ \underbrace{1.277}_{\text{fit}}\ <\ \underbrace{2.6\text{–}15}_{\text{running (frozen)}}.$$

What fixes the exact point is the **nonperturbative IR coupling** — the same single scale-setting object as F124 §5 and F144 A4 (there as a scheme constant, here as the IR freeze). One number now owns all three residuals.

## 7. Checks

| # | Check | Result | Tier |
|---|---|---|---|
| N1 | Fierz $c=\tfrac29$ all four chiral channels; Fock $=4C_F=\tfrac{16}3$ | $8\times10^{-17}$ / exact | machine-exact |
| N2 | contact anchor: analytic $R$ == power iteration | $5\times10^{-15}$ | machine |
| N3 | bare $g_s^2=\tfrac14$ resolved: $R=0.075$–$0.10\ll1$; $\varepsilon_c$ can't rescue | PASS | decisive negative |
| N4 | running coupling: $R=2.6$–$15\gg1$; $\alpha_\text{crit}=0.20$–$0.27$ | PASS | structural PREDICTION |
| N5 | fit bracketed; $\alpha_\text{eff}(\text{fit})=0.26$–$0.34$ in the running band | PASS | residual quantified |

## 8. Honest scope

- $m_D$ is measured at $\beta=1.8$ in the F88 3D compact-U(1) surrogate (its honest scope inherited); the F88-vs-F117 spread (0.532 vs 0.727) is MC/volume scatter and is carried through every row.
- The "running" kernel uses 1-loop $n_f{=}3$ $\overline{\rm MS}$ with a smooth IR freeze — a prescription, scanned, not derived; that prescription dependence *is* the N5 residual, deliberately surfaced rather than tuned away. The longitudinal (Proca $q^\mu q^\nu$) part of the massive propagator is dropped (current-conservation argument); it would only raise $R$, strengthening N4 without changing N3's verdict (it cannot supply ×10 at the bare coupling).
- The linearised criticality eigenvalue determines whether χSB occurs and the coupling ratio $G/G_c$; the full $M(k)$ self-consistent solve (and from it $m_c$, $f_\pi$ without the F77 fit) is the natural next build once the IR coupling is pinned.
- $\hat g$ in the $\Lambda$-convention: bare-resolved 0.12–0.16, running 4.3–25, fit 2.10 — same bracketing, $\Lambda$-convention inherited from F116.

## 9. Provenance

- New: the exact 24-dim Fierz projection (all channels) and Fock identity; the momentum-resolved induced gap kernel on the BZ with its criticality eigenvalue; the bare no-go; the running-coupling composition and $\alpha_\text{crit}$ inequality; the bracketed residual.
- Reused: F116 NJ2 gap machinery (anchor), F117 gap-massive propagator form + $\varepsilon_c$, F88 measured $m_D$, F144 lock + running, F77 fit targets.
- Verification: `tests/findings/test_F145_route_c_induced_njl.py` (2026-06-12, 5/5 PASS), results `test-results/F145_route_c_induced_njl.json`.
