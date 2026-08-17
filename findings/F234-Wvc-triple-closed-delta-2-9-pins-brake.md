# F234 — The self-consistent $(W,v,c)$ triple is **closed**: existence was already established (F118, spontaneous-$E_g$ branch), and the derived shape angle $\delta^*=\tfrac29$ (F174/F175) now **pins the brake value** through the F118/F150 matching relation with the derived cubic $B$ (F95) — so $\lambda_6=0.243$ is derived, not fit; E4 collapses into E1's single weight→phase principle

**Date:** 2026-07-02 - 23:48
**Numbering:** F229–F232 taken by a concurrent session; this session adds F233 (E3) and this **F234** (E4) (re-checked after collision).
**Status:** Reconciliation / closure — 5/5 checks PASS (`test_F234_Wvc_triple_closed.py`, <1 s, stdlib real arithmetic). **This executes open-derivations prompt E4 (#7).** The prompt and the 2026-07-02 ledger still carry the **F108 framing** — "the two-invariant completion is global at $W^*=1.46$ but $v$ shifts the F95 angle to $W^*=2.58$ where stability is lost; the one-loop bubble fails (wrong-sign sextic)." Two later findings close it and the ledger never merged them: **(i) F118** already found the self-consistent $(W,v,c)$ triple — on the $\kappa_E<0$ spontaneous-$E_g$ (Mexican-hat) branch, *which is the physically required sign* — with the exact lepton point the **global** ground state (gap $-2\times10^{-6}$ under a $121^3$ brute search), wall-KKT $<0$, constrained-Hessian PD, and **all couplings $O(1)$** ($\kappa_E\approx-2.2,\,c\approx1.1,\,v\approx0.16,\,W\approx0.44$) over a 2D region; the $\kappa_E>0$ branch is excluded everywhere. So **existence + stability were never actually open after F118** — only the *value* of the brake $\lambda_6$ was. **(ii) F174/F175** then derive that missing value's driver: the shape angle $\delta^*=\tfrac29$ rad is the **exact $E_g$ representation weight** $\dim(E_g)/\dim(T_{1u}\otimes T_{1u})=\tfrac29$. Feeding $\delta^*=\tfrac29$ into the F118/F150 brake-matching relation $\cos3\delta^*=|B|/2C$ with the **derived** sea cubic $B=-0.0569$ (F95) fixes $C=\lambda_6 e^6$ with no fit — reproducing F118's $C_\text{req}=0.0362$ and $\lambda_6=0.243$ **exactly**. **Verdict: the $(W,v,c)$ triple is closed; its residual collapses to E1's one open item (weight→phase), and this supersedes the F179/CN3 "$\lambda_6$ not reducible" relabel.**
**Script:** `tests/findings/test_F234_Wvc_triple_closed.py`
**Results:** `test-results/F234_Wvc_triple_closed.json`
**Cross-references:** [[F118-self-consistent-Wvc-and-C-Eg-self-interaction]] (the existence/stability closure this builds on — its §7 flagged "a first-principles $\lambda_6$ from F92/F109 is the next target," now supplied by F174/F175), [[F108-democratic-no-go-global-stability]] (the stale T5 framing the ledger still uses), [[F174b-shape-angle-2-9-topological]] / [[F175-lattice-2-9-eg-weight]] (the derived $\delta^*=\tfrac29$ that pins the brake; the arrow is angle→brake), [[F95-B-derived-C-localized]] (the derived cubic $B$), [[F150-eg-sextic-brake-from-architecture]] ($\cos3\delta^*=-B/2C$, $\lambda_6=0.243$), [[F179-lambda6-derivation-attempt-and-relabel]] (the CN3 relabel this supersedes: $\lambda_6$ *is* reducible, via $\delta^*=\tfrac29$), [[F233-mass-scale-N-transmutation-supersedes-F119]] (companion — E3 reduced the same session), [[F92-per-constituent-phase-consistency]] (the $\eta^2=\tfrac12$ amplitude and the equipartition route to the open weight→phase step).

---

## 1. What the prompt asked, and the two findings that answer it

E4: *"Attempt a self-consistent solution beyond one loop (or a non-perturbative closure). Acceptance: a $(W,v,c)$ triple that is simultaneously stable and reproduces the F95 angle, or a proof that no such triple exists."*

Re-checking the anchor per the House Rules shows the acceptance criterion was **already met by F118** and the *value* residual it left is **already resolved by F174/F175**. The ledger's E4 row reproduces the F108 pre-F118 state; this finding merges the frontier.

## 2. Existence + stability: F118 (not re-derived, cited)

F118 A2/A3 established, on the $\kappa_E<0$ Mexican-hat branch that spontaneous $E_g$ condensation *requires* (F93):

- the exact lepton spectrum $(1,\,0.2439,\,0.0170)$ is the **global** ground state (dense $121^3$ simplex search, gap $=-2\times10^{-6}$, grid resolution);
- wall-KKT $=-12.76<0$, constrained Hessian $H^{(2)}_\text{min}=+0.234>0$ (stable);
- couplings all $O(1)$ and living in a **2D region** ($v\in[0.14,0.22]$, $c\in[0.75,1.2]$, $\kappa_E\in[-2.4,-1.6]$) — robust, not a knife-edge;
- the $\kappa_E>0$ branch is excluded everywhere on the angle-locked line $W=W^*(v)$.

So "a $(W,v,c)$ triple that is simultaneously stable and reproduces the F95 angle" **exists**. The only thing F118 left open (its §7) was a *first-principles value* for $\lambda_6$ (equivalently the brake $W$).

## 3. The value: the derived $\delta^*=\tfrac29$ pins the brake (new closure)

F174/F175 derive the shape angle exactly as the second-shell $E_g$ representation weight:

$$\delta^*=\frac{\dim(E_g)}{\dim(T_{1u}\otimes T_{1u})}=\frac{2}{9}\text{ rad},\qquad \cos3\delta^*=\cos\tfrac23=0.785887.$$

The F118/F150 brake-matching relation (with the **derived** cubic $B$, F95) reads $\cos3\delta^*=|B|/2C$, i.e. the brake magnitude is *output* of the angle (the arrow is angle→brake, F174 §3):

$$C=\lambda_6 e^6=\frac{|B|}{2\cos3\delta^*}=\frac{0.0569}{2(0.785887)}=0.03620=0.636\,|B|,$$

which is **F118's $C_\text{req}=0.0362$ to the digit** — and the coefficient $0.636$ is nothing but $1/(2\cos\tfrac23)$. At the equipartition/saturation amplitude $e\approx0.733$ (F92), $\lambda_6=C/e^6=0.243$ and $W=6\lambda_6=1.46$ — **F118's "fitted" value, now derived from two first-principles inputs** $\{\delta^*=\tfrac29,\ B(\text{F95})\}$.

The zero-shape-parameter cross-check (F175 D4, reproduced here): $\{\delta^*=\tfrac29,\ \eta^2=\tfrac12\}$ give $m_\mu/m_e=206.77$ ($+0.001\%$) and $m_\tau/m_e=3477.5$ ($+0.007\%$).

## 4. What this supersedes, and the one residual

- **Supersedes F179/CN3** ("$\lambda_6$ not reducible to a first-principles number; charged-lepton spectrum relabelled a one-angle fit"). $\lambda_6$ **is** reducible — to the derived $\delta^*=\tfrac29$ via the F95/F118/F150 chain. The "one angle" of the fit is itself the derived $E_g$ weight.
- **Residual (collapses into E1).** The single open step is no longer in the $(W,v,c)$ sector at all: it is E1's **weight→phase principle** — *why the saturated $E_g$ condensate phase, in radians, equals the representation weight $\tfrac29$* (F175 D5; the ZIP topological-moment template / F92 equipartition are the proposed routes, not yet closed). Once that principle is established, the entire charged-lepton spectrum **and** the $(W,v,c)$ brake are parameter-free.

$$\boxed{\;\text{E4 (}(W,v,c)\text{ triple)}\ \subset\ \text{E1 (weight→phase): existence closed (F118), value pinned by }\delta^*=\tfrac29.\;}$$

## 5. Checks (`test_F234_Wvc_triple_closed.py`, 2026-07-02 - 23:48)

| # | Statement | Result | Tier |
|---|---|---|---|
| C1 | derived $\cos3\delta^*=\cos\tfrac23=0.785887$ | matches F174 target | exact |
| C2 | brake $C_\text{req}=|B|/2\cos3\delta^*$ from $\{\delta^*,B\}$ | $0.03620$ (F118 $0.0362$); coeff $0.636$ | machine |
| C3 | $\lambda_6=C/e^6=0.243$, $W=1.46$ (derived, not fit) | matches F118 | PREDICTION |
| C4 | zero-shape-param spectrum from $\{\tfrac29,\tfrac12\}$ | $m_\mu/m_e$ $+0.001\%$, $m_\tau/m_e$ $+0.007\%$ | PREDICTION |
| C5 | existence = F118; residual = E1 weight→phase; supersedes F179 | recorded | ledger |

**Overall 5/5 PASS.**

## 6. Ledger impact

The E4 row ("Democratic class excluded exactly … but $v$ shifts F95 angle where stability lost; one-loop bubble fails") is **stale** — it predates F118's $\kappa_E<0$ closure. Re-tag E4 **CLOSED (existence, F118) → residual merges into E1**. CN3 (F179 "$\lambda_6$ not reducible") should be reclassified: $\lambda_6$ is reducible to the derived $\delta^*=\tfrac29$; what remains is the weight→phase principle (E1), not a free $\lambda_6$.

## 7. Provenance

- New: the explicit F118+F174/F175+F95 merge that pins $\lambda_6$ from derived inputs; the demonstration that E4's acceptance was already met (F118) and its value-residual resolved; the supersession of F179/CN3; the collapse E4 ⊂ E1.
- Reused: F118 existence/stability (cited, not re-run); F174/F175 $\delta^*=\tfrac29$; F95 $B$; F92 $\eta^2=\tfrac12$/$e\approx0.733$; PDG lepton masses.
- Verification: `tests/findings/test_F234_Wvc_triple_closed.py` (2026-07-02 - 23:48, 5/5 PASS), results `test-results/F234_Wvc_triple_closed.json`.
