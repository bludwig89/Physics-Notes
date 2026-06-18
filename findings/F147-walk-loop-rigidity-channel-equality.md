# F147 — The Peierls-gauged walk loop: the one-tick sea is gauge-rigid (zero induced stiffness in every channel, exact), and in the stroboscopic sea the F51 hypercharge bubble equals the vector bubble pointwise — U2's dynamical ratio is exactly 1

**Date:** 2026-06-12 - 14:50
**Status:** Three exact structural results + decisive numerics; 10/10 checks PASS. Companion to [[F143-wrap-loop-stiffness-nogo]] (concurrent session, same F138 follow-up, complementary gauging route): both routes independently conclude the free fermion sector cannot own the gauge stiffness.
**Module:** `ca-simulation/ca_induced_stiffness.py`
**Script:** `tests/findings/test_F147_induced_stiffness_loop.py` (10/10, ~40 s)
**Results:** `test-results/F147_induced_stiffness_loop.json`
**Cross-references:** [[F138-weinberg-gap-closure-4piv-matching]] (the induced-$Y$-loop follow-up), [[F141-ws-cell-7axes-onshell-mass-counting]] (hypothesis U2 — this finding settles its dynamical half), [[F51-bipartite-sublattice-hypercharge]] (the parity carrier; its anticommutation theorem drives everything here), [[F143-wrap-loop-stiffness-nogo]] (the wrap-on-$U(x)$ route: transverse conjugation no-go, longitudinal per-mille — convergent conclusion), [[F45-sigma-tau-swap-weinberg-angle]], [[F49-bcc-finite-k-weinberg-angle]], [[F37-rs-bcc-chirality-helicity]].

---

## 1. Question and route

F138 left open: compute the induced $U(1)_Y$ kinetic term from a lattice fermion loop. F141 (U2) asked: is the induced stiffness quantum of the abelian (sublattice) channel equal to that of the link/vector channel? F143 (concurrent session) answered the first question on the **wrap route** — gauging $Y$ through the F42 Stueckelberg sandwich on $U(x)$ — finding a transverse conjugation no-go (exactly zero) and a per-mille longitudinal contact term.

This finding takes the **walk route**: gauge the fermion walk itself by Peierls substitution on its 8 body-diagonal hops and compute the static polarization of the sea, channel by channel:

- **vector channel** — ordinary Peierls phase per hop ($SU(2)_L$ Cartan bubble = $\tfrac14\sum_\text{branches}$ of this; $T_3=\pm\tfrac12$ on the branch index).
- **staggered channel** — the F51 hypercharge: parity charge $P=(-1)^{x+y+z}$, gauged consistently on the two-tick walk (tick 1 carries the source-site charge, tick 2 the target-site charge, so the composite hop $x\to x{+}d{+}d'$ carries exactly $P(x)\,A\cdot(d{+}d')$; pure-gauge configurations telescope **exactly** — Ward residual $0.0$, L4a).

Exact machinery built en route (all machine-verified): the 8-hop decomposition $A(q)=\sum_d e^{i d\cdot q}C_d$ (L1, $10^{-15}$); the **parity theorem** — from F51 S1, $\omega(q{+}Q)=\pi-\omega(q)$ and $\mathbf n(q{+}Q)=-\mathbf n(q)$, so every mode's staggered partner sits at opposite two-tick quasienergy with flipped helicity (L2, $10^{-15}$); and circle perturbation theory for unitaries — $\delta^2\Omega_n/\delta\varepsilon^2=\sum_m|K_{nm}|^2\cot\big(\tfrac{\Omega_n-\Omega_m}{2}\big)$ with $K=i\,\delta W_2\,W_2^\dagger$, the cut-free replacement for $\delta H_2$ matrix elements (L3, $2\times10^{-6}$).

Both channels share one midpoint vertex $V(q{+}\tilde q/2)$; the entire channel difference is algebraic:

$$\delta W_2^{\text{vec}} = W(q{+}\tilde q)\,V + V\,W(q), \qquad
\delta W_2^{\text{stag}} = W(q{+}\tilde q{+}Q)\,V - V\,W(q),$$

the relative minus being $e^{i d\cdot Q}=-1$ for every odd hop.

## 2. Result A — one-tick gauge rigidity (exact, all channels)

> **Theorem (numerically established, mechanism identified).** The half-filled one-tick sea ($-\omega$ band, the project-standard F46 sea) has **exactly zero** static response to any plane-wave gauge field in **either** channel — not small: zero to $10^{-12}$ at field strengths up to $\varepsilon=0.3$ (L6).

Mechanism (L5, both closures exact at $\varepsilon=0.3$): the gauged spectrum is closed under $\lambda\to-\lambda$ (i.e. $\theta\to\theta+\pi$; this is $\{P,W_A\}=0$, which holds for **any** gauge field because Peierls phases cannot break bipartiteness) **and** under $\lambda\to-\bar\lambda$ (i.e. $\theta\to\pi-\theta$). The composition pairs the filled half $\theta\in(-\pi,0)$ with itself, each pair summing to the constant $-\pi$ — the sea energy is rigid (constant modulo quantized $2\pi$ cut-crossings, observed as exact $2\pi$ jumps at large $\varepsilon$).

**Reading:** F41's "hypercharge has no lattice kinetic term" *generalizes and hardens*: at the one-tick level the free walk sea induces no kinetic term for **any** gauge channel — vector included. Combined with F143's transverse conjugation no-go on the wrap route, the conclusion is two-route convergent: **the gauge stiffness cannot come from the free fermion sector.** It must come from the condensate sector (F118), exactly where F141 §4 and F143 §5 both pointed.

A sharp corollary of the Ward block (L4b): the staggered pure-gauge invariance **fails** at the one-tick level (residual $9.2\times10^{-3}$) while it is **exact** stroboscopically ($0.0$) — the hypercharge gauge structure exists *only* on the two-tick lattice, quantifying F51 §3.

## 3. Result B — channel equality in the stroboscopic sea (U2's dynamical half)

In the two-tick sea (fill $\Omega\in(-\pi,0]$ of $H_2$ — the F51-physical convention, where the staggered transitions are gapless: gap $\to4\tilde\omega$ at the cones, $\tilde\omega=\min(\omega,\pi-\omega)$):

> **Theorem (proved pointwise + verified in the full response).** The staggered (hypercharge) bubble equals the vector bubble **identically**: matrix elements $|M_\text{stag}|=|M_\text{vec}|$ and circle gaps equal at every $q$ (L7, $10^{-14}$ on $8000$-point grids, face and body-diagonal $\tilde q$); the **full** brute-force response (paramagnetic + diamagnetic, dense gauged $W_2$, twisted BCs) is channel-equal to $10^{-12}$ at $L{=}6$ and $7\times10^{-8}$ at $L{=}8$ (L8).

Proof content: $W(q{+}Q)=-W(q)$ (F51 S1) makes $\delta W_2^{\text{stag}}=-\delta W_2^{\text{vec}}$ as blocks; $\tilde\omega$ is $Q$-invariant so the two-tick gaps match; and the parity theorem flips band assignment and helicity together, so the partner empty state is the same physical spinor up to phase. Equivalently: $\Pi_\text{stag}(\tilde q)=\Pi_\text{vec}(\tilde q{+}Q)=\Pi_\text{vec}(\tilde q)$ — **the staggering momentum $Q$ is a symmetry of the stroboscopic response.**

(Numerical care: the $\omega=\pi/2$ surface is the cut Fermi boundary where the band assignment is a knife edge; on symmetric grids $1.6\%$ of points land on it exactly and the tie-break convention, not physics, picks the partner — handled by an irrational golden-ratio grid offset. The $\cot$ kernel vanishes at the cut, so summed responses are unaffected either way.)

**Reading for F141-U2:** to the extent the gauge stiffness is fermion-loop-induced on the stroboscopic lattice, the per-unit-charge quantum of the abelian sublattice channel and the vector channel are **exactly equal** — U2's dynamical ratio is 1, as a theorem, not a computation. What U2 still needs (per Result A and F143) is the *condensate-sector* version of the same statement.

## 4. Result C — the bookkeeping residual is exactly 8/7

With equal per-charge quanta (Result B) and the bare walk charges ($q_P=\pm1$ on both branches, $T_3=\pm\tfrac12$):

$$\frac{1}{g'^2}\propto \sum q_P^2\,\Pi_b = 2\Pi_b,\qquad
\frac{1}{g^2}\propto \sum T_3^2\,\Pi_b = \tfrac12\Pi_b
\;\Longrightarrow\;
t^2\equiv\frac{g'^2}{g^2}=\frac14,\quad \sin^2\theta_W^\text{free}=\frac15,$$

exact rationals (L9). The F49 target $t^2=2/7$ differs by **exactly $8/7$**:

$$\frac{2/7}{1/4}=\frac87.$$

The loop has therefore localized the entire remaining content of the F49 assignment in a single rational factor that must come from **charge content and channel multiplicity** (the F38 hypercharge spectrum layered on the F51 carrier, and/or the 7-axis WS-cell counting of F141-U1/U3) — *not* from loop dynamics, which is now fixed at ratio 1. Suggestively, $8/7$ is the ratio of NN hops to WS facet axes ($8:7$), i.e. precisely the kind of multiplicity factor F141-U1 concerns; flagged, not claimed.

## 5. What this settles and what it does not

**Settled here:**
- One-tick gauge rigidity: zero induced stiffness, every channel, exact, with mechanism ($\theta\to\pi-\theta$ closure + bipartiteness) — F41 hardened to a theorem and extended to all channels (A).
- Two-tick Ward exactness of the parity gauging; one-tick failure quantified — hypercharge gauge structure is stroboscopic-only (A/L4).
- Stroboscopic channel equality, pointwise and in the full response — U2's dynamical ratio $=1$ exactly (B).
- The free-sea Weinberg bookkeeping: $t^2=1/4$, $\sin^2\theta_W^\text{free}=1/5$ with bare charges; the F49 gap reduced to the exact factor $8/7$ of charge content/multiplicity (C).

**Not settled:**
- The condensate-sector counterpart (the actual owner of the stiffness per Result A + F143): whether the $E_g$/EWSB condensate response preserves the per-channel equality and supplies the $8/7$ — this is F141 §4's programme, now with both no-go pillars in place.
- The $8/7$ itself: content factor (F38 charges: lepton/quark $Y$ values on the two sublattices) vs multiplicity factor (8 hops : 7 axes) — distinguishable in principle by redoing Result C with the full F38 generation content.
- Absolute log-coefficient extraction in the stroboscopic sea (the momentum-space PT here is paramagnetic-only; the diamagnetic contact term is included only in the brute force — large-$L$ sweeps need the diamagnetic term added to the PT, a Phase-2 item).

## 6. Check summary (10/10)

| Check | Statement | Tier | Result |
|---|---|---|---|
| L1 | 8-hop decomposition, both branches | machine | $1.5\times10^{-15}$ |
| L2 | parity theorem $\omega$, $\mathbf n$ | machine | $1.0\times10^{-15}$ |
| L3 | circle-PT $\cot$ kernel, unit prefactor | numeric | $1.9\times10^{-6}$ |
| L4a | two-tick pure-gauge Ward, both channels | exact | $0.0$ |
| L4b | one-tick staggered Ward fails | structural | $9.2\times10^{-3}>10^{-3}$ |
| L5 | gauged spectral closures $\lambda\to-\lambda$, $\lambda\to-\bar\lambda$ at $\varepsilon=0.3$ | exact | $0.0$ |
| L6 | one-tick rigidity $\chi=0$, both channels | exact (to floor) | $<10^{-12}$ |
| L7 | pointwise channel equality, face+diag | machine | $1.0\times10^{-14}$ |
| L8 | full-response channel equality $L=6,8$ | numeric (decisive) | $0.0$ / $7.3\times10^{-8}$ |
| L9 | $t^2=1/4$, $s^2=1/5$, gap $=8/7$ | exact rational | exact |

## 7. Honest scope

- Sea conventions are physics here: results A (rigidity) and B (equality) hold in the one-tick and two-tick conventions respectively, and the contrast between them is itself a result (L4b). The two-tick convention is the F51-physical one.
- The momentum-space bubble omits the diamagnetic contact term (documented in-module); every quantitative claim above rests on either exact algebra or the brute-force **full** response.
- The bare-content $\sin^2\theta_W^\text{free}=1/5$ is **not** a prediction of the physical angle — it is the free-sea value with unit parity charge, stated only to localize the $8/7$. The physical chain remains F45/F138 (cap $1/4$ at $4\pi v$, running) and F141 (on-shell $2/9$ as mass counting).
- Result A's mechanism is established numerically (closures exact at strong field); a one-line algebraic proof of the $\lambda\to-\bar\lambda$ closure from the $C_d$ structure is expected but not written — flagged as a small follow-up.

## 8. Files

- `ca-simulation/ca_induced_stiffness.py` — module (gauged walk, vertices, circle PT, brute force, Ward)
- `tests/findings/test_F147_induced_stiffness_loop.py` — L1–L9
- `test-results/F147_induced_stiffness_loop.json` — full output
