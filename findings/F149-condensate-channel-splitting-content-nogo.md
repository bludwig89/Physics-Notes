# F149 — The condensate-sector response: mass is the unique channel-splitting agent (F147's lock breaks ∝ m² with kinematics still locked), the one-tick rigidity survives the mass, and charge content cannot supply the F49 ratio (exact no-go: bare ×8/7, F38-SM ×10/21)

**Date:** 2026-06-12 - 16:05
**Status:** Two exact structural results + a decisive no-go + the splitting mechanism measured; 8/8 checks PASS. Direction-setting: the F49 ratio 2 : 7 can now only be dynamical (condensate splitting) and/or geometric multiplicity — free-sea charge counting is eliminated.
**Module:** `ca-simulation/ca_induced_stiffness.py` (Dirac/condensate-proxy section added)
**Script:** `tests/findings/test_F149_condensate_channel_splitting.py` (8/8, ~60 s)
**Results:** `test-results/F149_condensate_channel_splitting.json`
**Cross-references:** [[F147-walk-loop-rigidity-channel-equality]] (the massless lock this breaks, and the 8/7 it localized), [[F141-ws-cell-7axes-onshell-mass-counting]] (hypothesis U — this is §4's condensate-sector programme executed at the proxy level), [[F38-fg1-anomaly-cancellation]] (the charge content tested in N8), [[F143-wrap-loop-stiffness-nogo]] (E_g owns the wrap stiffness — consistent with N4), [[F46-pythagorean-lattice-mass]] / `ca_dirac_bcc` (the exact Dirac construction used as the condensate proxy), [[F138-weinberg-gap-closure-4piv-matching]].

---

## 1. Question and method

F147 proved the massless lock: in the stroboscopic sea the F51 hypercharge bubble equals the vector bubble exactly, so the F49 assignment's missing factor (8/7 with bare charges) cannot come from loop dynamics of the *free* walk. Two suspects remained: **charge content** (F38 generation spectrum) and the **condensate sector**. This finding tests both.

Condensate proxy: the project's own exact Dirac construction (`ca_dirac_bcc`, Paper 1 Eq. 23) — $D(q)=\begin{pmatrix}n A(q) & im\\ im & n A^\dagger(q)\end{pmatrix}$, $n=\sqrt{1-m^2}$, $\cos\omega_m = n\,u(q)$ — with $m$ standing in for the constituent coupling to the EWSB condensate. Both gauge channels (vector / F51 parity-staggered) are gauged exactly as in F147 (hop Peierls; the on-site mass carries no phase — and the staggered two-tick prescription still telescopes exactly on pure gauges).

## 2. Exact structure: what the mass cannot break

- **N1 — the Dirac parity theorem.** $\omega_m(q{+}Q)=\pi-\omega_m(q)$ survives the mass for all $m$ (from $u(q{+}Q)=-u(q)$), with the exact operator form $D(q{+}Q) = -X\,D(q)\,X$, $X=\mathrm{diag}(I_2,-I_2)$ — the staggered symmetry of the massive theory is parity **combined with the chiral sign**. ($10^{-15}$.)
- **N2 — the bipartite closure generalizes.** $\{S, D_A\}=0$ with $S=\hat P\cdot\hat X$ for **arbitrary gauge fields** (exactly $0.0$ at $\varepsilon=0.3$, $m=0.4$): hops are $\hat P$-odd, the on-site mass is $\hat X$-odd, and Peierls phases can break neither.
- **N4 — one-tick rigidity survives the mass.** $\chi^{\text{one-tick}} = 0$ to $10^{-11}$ in both channels at $m=0.4$: even the condensate-dressed sea induces **no** static gauge stiffness at the one-tick level. F147's rigidity is robust; the induced stiffness is *irreducibly stroboscopic*. (Consistent with F143's conclusion from the wrap route.)

## 3. The splitting: what the mass does break

- **N3 (control).** At $m=0$ the 4×4 Dirac path reproduces F147's lock to machine precision (rel $\Delta T = 4\times10^{-15}$), and the batched eigendecomposition is validated against the analytic dispersion $\arccos(n\,u)$ to $1.8\times10^{-15}$ (the numpy-on-chiral guard).
- **N5 — the lock breaks for $m>0$, in the weights only.** Pointwise matrix-element split (relative): $0.075,\ 0.221,\ 0.487,\ 0.727$ at $m=0.05, 0.1, 0.2, 0.4$ — monotone — while the circle gaps stay equal to $3.6\times10^{-15}$ at **all** $m$ (the Dirac parity theorem locks the kinematics; only the transition weights split).
- **N6 — full response splits with an $m^2$ onset.** Brute-force (paramagnetic + diamagnetic, $L=6$): $\chi_\text{stag}-\chi_\text{vec} = -0.0055,\ -0.0206,\ -0.0638$ at $m=0.05, 0.1, 0.2$; the $m^2$-scaling ratio between the two smallest masses is $1.08$ ($1$ = exact $m^2$). The splitting turns on like the condensate density.
- **N7 — paramagnetic small-$\tilde q$ ratio.** $\chi_\text{vec}/\chi_\text{stag}$ drifts smoothly and monotonically from exactly $1$: $1.0000,\ 0.9831,\ 0.9533,\ 0.9154$ at $m=0,0.1,0.2,0.4$ ($L=20$, $\tilde q = 2\pi/20$). In the paramagnetic piece the staggered channel is *enhanced*; the $L=6$ full response at moderate $m$ has the vector channel enhanced — the **physical** small-$\tilde q$ full ratio is not determined here (it needs the diamagnetic term in the momentum-space PT, or large-$L$ full response; flagged open, §5).

**Mechanism statement.** In the model's fermion sector, the symmetry-breaking (mass/condensate) coupling is the **unique channel-splitting agent**: massless = locked exactly (F147 theorem), massive = split, onset $\propto m^2$. A dynamical origin for $g^2\neq$ (charge-count) $\times\, g'^2$ therefore *exists* and lives exactly where F141 §4, F143 and F118 put the stiffness.

## 4. The content no-go (exact rationals, N8)

With equal per-charge quanta (the F147 theorem) the free-sea ratio is pure charge algebra, $t^2 = \sum T_3^2 \big/ \sum (Y/2)^2$:

| Content | $\sum T_3^2$ | $\sum (Y/2)^2$ | $t^2$ | $\sin^2\theta_W$ | factor to reach $2/7$ |
|---|---|---|---|---|---|
| Bare walk ($q_P=\pm1$, $T_3=\pm\tfrac12$) | $\tfrac12$ | $2$ | $\tfrac14$ | $\tfrac15$ | $\times\tfrac87$ |
| F38 SM generation ($Y_L=-1$, $e_R\,{-2}$, $Q_L\,{+\tfrac13}$, $u_R\,{+\tfrac43}$, $d_R\,{-\tfrac23}$) | $2$ | $\tfrac{10}{3}$ | $\tfrac35$ | $\tfrac38$ | $\times\tfrac{10}{21}$ |

The SM-content value $3/8$ is the classic equal-quanta (GUT/induced-coupling) result — a sanity check that the bookkeeping is standard. **Neither charge set gives $2/7$**, and the two miss in *opposite directions* (bare needs the vector channel stiffness-enhanced by $8/7$; SM content needs the staggered channel enhanced by $21/10$). Free-sea charge counting is eliminated as the source of F49's ratio.

## 5. Where this leaves the F49 derivation

Eliminated: loop dynamics of the free sea (F147, ratio $\equiv1$); charge content alone (N8, exact). Established: a splitting mechanism with the right structure — condensate-driven, $\propto m^2$, kinematics-preserving — in the only sector that can own the stiffness at all (N4 + F143).

The remaining derivation therefore has exactly two live components, possibly combined: (a) **geometric multiplicity** (F141-U1/U3: the 7 WS facet axes vs the 8 hop directions — note $8/7$ is precisely hops:axes), and (b) **the condensate splitting function** $R(m)\equiv\chi_\text{vec}/\chi_\text{stag}$ evaluated in the physical (diamagnetic-complete, small-$\tilde q$) response at the model's own condensate strength: $t^2 = \tfrac14 R$ (bare content), so $2/7$ ⟺ $R = 8/7$. If route (b) is real, it converts F49's ratio into a *prediction relating the condensate scale to the Weinberg angle* — falsifiable against the F118 sector with no new knobs.

**Open (sharp):**
1. The diamagnetic term in the momentum-space PT (or CASIM-scale full response) → the physical $R(m)$ at small $\tilde q$; its sign decides between the N7 (staggered-enhanced) and N6-at-large-$m$ (vector-enhanced) directions.
2. Which $m$ to evaluate at: the proxy must be matched to the F118 condensate normalisation (constituent coupling, not the bare lepton mass).
3. The multiplicity route: a per-facet-axis decomposition of $\chi_\text{vec}$ (does the vector stiffness decompose as 8 hop channels or 7 facet channels?) — directly testable with the existing vertices.

## 6. Check summary (8/8)

| Check | Statement | Tier | Result |
|---|---|---|---|
| N1 | Dirac parity theorem (dispersion + operator $-XDX$) | exact | $1.3\times10^{-15}$ |
| N2 | $\{S,D_A\}=0$, $S=\hat P\hat X$, gauged, $m=0.4$ | exact | $0.0$ |
| N3 | $m=0$ lock recovered through 4×4 path; eig vs analytic | machine | $4\times10^{-15}$ / $1.8\times10^{-15}$ |
| N4 | one-tick rigidity at $m=0.4$, both channels | exact (to floor) | $2\times10^{-11}$ |
| N5 | split monotone in $m$; gaps equal at all $m$ | machine + numeric | $0.075\to0.727$; gaps $3.6\times10^{-15}$ |
| N6 | full-response split, $m^2$ onset | numeric (decisive) | scaling ratio $1.08$ |
| N7 | para ratio drifts smoothly from exactly 1 | numeric | $1.0000\to0.9154$ |
| N8 | content no-go: $t^2\in\{1/4, 3/5\}$, factors $8/7$, $10/21$ | exact rational | exact |

## 7. Honest scope

- $m$ is a **proxy** for the condensate coupling (the exact `ca_dirac_bcc` Dirac mass); the true EWSB condensate is the composite F118 sector. The structural results (N1/N2/N4, the existence and $m^2$ onset of splitting) are convention-clean; the *value* of the physical splitting is not computed here.
- N6 is at fixed $\tilde q = 2\pi/6$ on a small torus — onset scaling only, not a small-$\tilde q$ coupling extraction. N7 is paramagnetic-only. The two differ in sign at moderate $m$; resolving this is open item 1.
- The N8 sums treat the F38 generation as independent species in the sea with those charges; how composite/layered content (F51 §5) weights the loop is part of open item 3's bookkeeping.

## 8. Files

- `ca-simulation/ca_induced_stiffness.py` — Dirac/condensate-proxy section (matrix, vertices, bands with eig-vs-analytic guard, brute force, $S$-closure)
- `tests/findings/test_F149_condensate_channel_splitting.py` — N1–N8
- `test-results/F149_condensate_channel_splitting.json` — full output
