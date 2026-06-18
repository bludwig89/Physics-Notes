# F153 — The diamagnetic Peierls contact is charge-blind (exact, machine precision): the electroweak channel splitting is **purely paramagnetic**, the small-$\tilde q$ ratio $R(m)$ is not cleanly extractable in the two-tick sea, the vector stiffness does **not** reduce to a clean 7- or 8-fold channel count, and the physical condensate coupling is $O(1)$ — so the on-shell $\sin^2\theta_W=2/9$ stands as exact algebra independent of any perturbative $R(m)$

**Date:** 2026-06-12 - 17:40
**Status:** One exact structural gain (charge-blind diamagnetic, $10^{-10}$) + three decisive negatives that, together, redirect the F49 $2:7$ derivation away from a perturbative proxy number. 5/5 checks PASS. Direction-setting: both live routes of F149 §5 (the condensate splitting function $R(m)$ and the geometric $8{:}7$ multiplicity) fail to deliver a *clean number* at the free-Dirac-proxy level; the $2/9$ on-shell statement is unaffected because it never depended on them.
**Module:** `ca-simulation/ca_induced_stiffness.py` (new diamagnetic section: `dirac_seagull4`, `dirac_d2_transfer0`, `dirac_chi_diamagnetic`)
**Script:** `tests/findings/test_F153_diamagnetic_chargeblind_multiplicity.py` (5/5, ~25 s)
**Results:** `test-results/F153_diamagnetic_chargeblind_multiplicity.json`
**Cross-references:** [[F149-condensate-channel-splitting-content-nogo]] (the N6/N7 sign puzzle and the two open routes this finding tests), [[F147-walk-loop-rigidity-channel-equality]] (the massless lock and the $8/7$ it localized), [[F141-ws-cell-7axes-onshell-mass-counting]] (the $2/9$ on-shell counting that survives; U1/U3 multiplicity), [[F143-wrap-loop-stiffness-nogo]] ($E_g$ owns the stiffness), [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the $O(1)$ condensate the proxy must match), [[F46-pythagorean-lattice-mass]] (the Dirac mass convention), [[F150-eg-sextic-brake-from-architecture]] (the saturated-condensate regime).

---

## 1. Question

F149 left two live routes to the residual factor $8/7$ that separates the bare-content $t^2=1/4$ from F49's $2/7$: **(b)** the condensate splitting function $R(m)=\chi_\text{vec}/\chi_\text{stag}$ with $t^2=\tfrac14 R$ (so $2/7\Leftrightarrow R=8/7$), and **(a)** the geometric multiplicity $8\text{ hops}:7\text{ WS facet axes}$. F149 flagged a sharp obstacle: the paramagnetic-only momentum-space PT (N7, staggered-enhanced, $R<1$) and the full $L=6$ brute response (N6, vector-enhanced at moderate $m$) **disagree in sign**. The missing ingredient is the diamagnetic (Peierls-contact) term. This finding adds it analytically, validates it, and then tests routes (a) and (b) directly, and matches the proxy mass to the F118 condensate.

## 2. The diamagnetic operator (built + validated)

For a real cos-wave gauge field $A(x)=\varepsilon\cos(\tilde q\cdot x)\,\hat e$ the $O(\varepsilon^2)$ transfer-0 piece of the two-tick Dirac walk $D_2$ contributes a first-order eigenphase shift $\delta\Omega_n=\mathrm{Re}\,[\,i\,e^{i\Omega_n}\langle n|\delta^2 D_2|n\rangle\,]$ summed over the filled set. Derived from the midpoint Peierls expansion (per-tick contact = DC of $\cos^2=\tfrac12$, plus the tick1$\times$tick2 cross term from $\pm\tilde q$ pairing):

$$\delta^2 D_2(q) \;=\; D(q)\,G_4(q) + G_4(q)\,D(q) \;+\; \tfrac14\big[\,V_4(q{+}\tilde q/2)^2 + V_4(q{-}\tilde q/2)^2\,\big],$$

with the per-tick contact $G_4=\mathrm{diag}(n\,G_A,\,n\,G_A^\dagger)$, $G_A(q)=-\tfrac14\sum_d(\hat e\cdot d)^2 e^{i d\cdot q}C_d$, and $V_4$ the existing hop vertex.

> **D1 (machine).** This analytic operator equals the dense gauged $D_2$ transfer-0 block to $7.8\times10^{-8}$ (extracted by plane-wave projection at small $\varepsilon$; the dense projector uses the conjugate convention, so the match is at base $-q$).

## 3. Result A (exact): the contact is **charge-blind** ⇒ the splitting is **purely paramagnetic**

> **D2 (exact, $1.1\times10^{-10}$).** The dense $\delta^2 D_2$ transfer-0 block is **identical** in the vector and staggered channels.

Mechanism (all three sign sources cancel): the per-tick contact carries the parity charge squared, $P^2=1$, so it is charge-blind; and the cross term picks up exactly two compensating signs — the $-P$ on tick 2, and $V_4(\,\cdot+Q)=-V_4$ from $e^{i d\cdot Q}=-1$ on every (odd) body-diagonal hop — which cancel. Therefore

$$\chi_\text{stag}-\chi_\text{vec} \;=\; \big(\chi_\text{stag}-\chi_\text{vec}\big)_\text{paramagnetic}\qquad\text{(the seagull drops out of the difference).}$$

**This resolves the F149 N6/N7 puzzle.** The full response is a (channel-distinguishing) paramagnetic split sitting on top of a **large, shared, charge-blind contact**. The contact dominates the *absolute* value of each channel and changes sign with $L$ and $\tilde q$ direction; so which channel looks "enhanced" in $|\chi|$ flips between N6 ($L=6$) and N7 ($L=20$), even though the *difference* is a clean paramagnetic object. N6 and N7 were never in genuine contradiction.

## 4. Result B (decisive negative): $R(m)$ at small $\tilde q$ is not cleanly extractable in the two-tick sea

The two-tick (stroboscopic, F51-physical) sea has gapless cones ($\text{gap}\to4\tilde\omega$) and a second Fermi boundary at the cut $\Omega=\pm\pi$ ($\omega=\pi/2$). Every route to the small-$\tilde q$ coefficient is contaminated at reachable $L$:

> **N1 (numeric, negative).** At $L=6$, $\tilde q\parallel x$, the transverse responses for $\hat e=\hat y$ and $\hat e=\hat z$ — equal by cubic symmetry — differ by $0.148$ against a signal of $0.114$ (artifact $\gtrsim$ signal). The channel difference $\chi_\text{stag}-\chi_\text{vec}$ even **flips sign** with $\tilde q$ direction: $-0.064$ at $\hat q=[100]$, $+0.157$ at $\hat q=[111]$.

Independently confirmed off-text: (i) the cot-kernel paramagnetic PT does **not** linearly reconstruct the full brute response with any constant $(a,b)$ (max resid $0.09$ over 12 configs) — it is not a faithful representation of the degenerate two-tick sea-energy second order; (ii) an exact momentum-space ladder (all orders in $\varepsilon$, hence diamagnetic-complete) reproduces the longitudinal $L=6$ brute force but **blows up** to $\sim10^4$–$10^5$ at $L\ge8$ from cut/cone mis-filling. The clean isotropic $\tilde q\to0$ ratio $R(m)$ is therefore not determined at proxy level.

**Falsification verdict for route (b).** The only sign-stable channel difference available — the paramagnetic ratio of F149 N7, $\chi_\text{vec}/\chi_\text{stag}<1$, monotone decreasing in $m$ — points to $R<1$, i.e. $t^2=\tfrac14 R<\tfrac14$, moving *away* from $2/7$. There is **no evidence that $R(m)$ reaches $8/7$**; the cone/cut instability prevents establishing it cleanly, and the one robust signal runs the wrong way. Route (b), as a perturbative proxy number, is not supported.

## 5. Result C (negative): the vector stiffness has no clean 7- or 8-fold channel count

Decomposing the vector vertex into single-hop contributions $B_d=D(q{+}\tilde q)V_d+V_d D(q)$ and forming the $8\times8$ channel matrix $\chi_{dd'}=\sum_{\text{occ}\to\text{emp}}\mathrm{Tr}\,[M_d M_{d'}^\dagger]\cot(\Delta\Omega/2)$ ($L=16$):

> **M1 (structural).** The matrix is **not** diagonal in the hop basis nor in the antipodal ($d,-d$) axis basis. Off-diagonals grouped by $\lvert d-d'\rvert^2$: the **face-axis** displacements $\lvert d-d'\rvert^2=4$ (the $(2,0,0)$-type NNN/square-facet axes of the WS cell) are present at fixed $\hat e$ but **cancel exactly** under the transverse $\hat e$-sum; the surviving couplings are face-diagonal ($\lvert d-d'\rvert^2=8\to0.63$) and antipodal ($=12\to0.33$). The $8$ eigenvalues form **4 anisotropic pairs** (within-pair $0.006\ll$ between-pair $0.081$), set by the $\tilde q$ axis — not a flat $7$- or $8$-fold degeneracy.

So the WS face-axis channels (F141-U1/U3) **do appear** in the bilinear — answering question (ii) affirmatively — but they do not organize into a clean integer channel count; the geometry is entangled with the $\tilde q$ direction. **Question (iii):** the $m>0$ splitting localizes in the **antipodal** ($\lvert d-d'\rvert^2=12$) group (vector $0.272$ vs staggered $0.315$ at $m=0.2$): the staggered $-1$ relative-tick sign is exactly what re-weights the $d\leftrightarrow-d$ channel. The multiplicity route is not refuted, but it does not yield "$N_W:N_Y\cdot q^2=7:2$" as a clean count at this level.

## 6. Result D: the physical condensate coupling is $O(1)$ — outside the perturbative regime

The F149 Dirac $m$ is a proxy for the constituent coupling to the EWSB/$E_g$ condensate. Matching to F118: at the lepton ground state $y=(1,\,0.2439,\,0.0170)$ (with $\tau$ wall-pinned, $y_\tau=1$), the $E_g$ order-parameter amplitude is $e=\lVert y-\bar y\rVert=0.728$ — and F118 finds *all* completion couplings $O(1)$ ($\kappa_E\approx-2.2,\ c\approx1.1,\ v\approx0.16$). 

> **P1 (algebraic).** The physical condensate sits at $O(1)$ coupling (saturated, the F150 regime), **not** in the small-$m$ region where a perturbative $R(m)$ expansion is valid. A small-$m$ proxy $R(m)$ was therefore never the right object for the physical angle. The on-shell statement that *does* hold is F141's exact algebra: $\sin^2\theta_W^\text{os}=2/9$, $m_Z/m_W=3/\sqrt7=1.133893$ vs PDG $1.134614$ ($-0.063\%$), $2/9$ vs $0.22305$ ($-0.44\%$) — independent of any $R(m)$ derivation.

## 7. What this settles and what it does not

**Settled:**
- The diamagnetic Peierls contact is charge-blind (exact, $10^{-10}$); the electroweak channel splitting is purely paramagnetic (Result A). This is the clean structural gain and it dissolves the N6/N7 sign puzzle.
- The analytic $\delta^2 D_2$ operator is built and validated against the dense response (D1); now available in the module.
- A clean isotropic $R(m)$ is **not** extractable in the two-tick sea at reachable $L$ (cone/cut artifacts); the one sign-stable channel signal ($R<1$) runs *away* from $8/7$ (Result B).
- The vector stiffness shows the WS face-axis channels but no clean $7$/$8$ channel count; the mass splitting lives in the antipodal channel via the staggered tick sign (Result C).
- The physical condensate coupling is $O(1)$, so a perturbative proxy $R(m)$ is the wrong tool; the on-shell $2/9$ is exact algebra regardless (Result D).

**Not settled (redirected):**
- Whether the **saturated** ($O(1)$, F118/F150) condensate response — not the small-$m$ proxy — supplies $8/7$. This now requires the non-perturbative condensate-sector stiffness computation (the same object F150's $\lambda_6$ solve and F143's $f_{E_g}$ need), not a free-Dirac bubble.
- The geometric multiplicity route (a) at the level of an explicit WS-facet flux quadratic form (F141-U3), which Result C shows is entangled with direction and not a bare count.

**Net:** of F149's two routes, the free-proxy versions are both eliminated as clean-number sources (B, C); combined with Result D this points all remaining weight at the saturated $E_g$ condensate sector — exactly where F143/F150 also point. The $2/9$ prediction is undisturbed.

## 8. Check summary (5/5)

| Check | Statement | Tier | Result |
|---|---|---|---|
| D1 | analytic $\delta^2 D_2$ = dense transfer-0 block | machine | $7.8\times10^{-8}$ |
| D2 | staggered $\delta^2 D_2$ = vector (charge-blind) | exact | $1.1\times10^{-10}$ |
| N1 | small-$\tilde q$ artifact-dominated ($\hat y$/$\hat z$ asym, sign flip) | numeric (neg.) | asym $0.148>$ sig $0.114$; sign flip |
| M1 | no clean channel count; face-axis cancels; antipodal splitting | structural | 4 pairs; $\Delta_{12}$ vec $0.272$/stag $0.315$ |
| P1 | physical coupling $O(1)$; on-shell $3/\sqrt7$ exact | algebraic | $e=0.728$; $-0.063\%$ |

## 9. Honest scope

- The $\chi_{dd'}$ decomposition (Result C) uses the cot-kernel paramagnetic vertex bilinear, which Result B shows is not the faithful full response; its *structure* (which hop-pairs couple, the transverse cancellation) is a vertex-geometry property and robust, but its *absolute* values are not the physical stiffness.
- $m$ is the proxy Dirac mass (F46 convention, $\Omega_\text{rest}=\arcsin m$); Result D's $O(1)$ statement is about the F118 amplitude, and the bridge between that amplitude and a Dirac-proxy $m$ is qualitative, not a calibrated map.
- Sea convention: all channel/splitting results are in the two-tick (stroboscopic, F51-physical) sea; the one-tick sea is rigid (F147/F149 N4) and irrelevant here.

## 10. Files

- `ca-simulation/ca_induced_stiffness.py` — diamagnetic section (`dirac_seagull4`, `dirac_d2_transfer0`, `dirac_chi_diamagnetic`)
- `tests/findings/test_F153_diamagnetic_chargeblind_multiplicity.py` — D1, D2, N1, M1, P1
- `test-results/F153_diamagnetic_chargeblind_multiplicity.json` — full output
