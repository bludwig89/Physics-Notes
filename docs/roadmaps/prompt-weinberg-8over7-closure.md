# Session prompt — close the F49 8/7: diamagnetic-complete R(m), the 8-vs-7 multiplicity test, and the F118 matching

*2026-06-12 - 16:30. Handoff prompt for a fresh session. Paste everything below the line as the opening instruction.*

---

Continue the Weinberg-angle program. Read first: `findings/F147-walk-loop-rigidity-channel-equality.md`, `findings/F149-condensate-channel-splitting-content-nogo.md`, `findings/F141-ws-cell-7axes-onshell-mass-counting.md` §4–5, and `findings/F143-wrap-loop-stiffness-nogo.md` §1 (concurrent companion). Module: `ca-simulation/ca_induced_stiffness.py`. Working state: F147 proved the massless channel lock (hypercharge ≡ vector bubble, exact); F149 proved mass is the unique splitting agent (m² onset, kinematics locked), one-tick rigidity survives mass, and charge content cannot supply F49's 2/7 (bare needs ×8/7, F38-SM needs ×10/21 — exact no-gos). Two live routes remain, possibly combined: geometric multiplicity (8 hops : 7 WS facet axes = 8/7) and the condensate splitting function R(m) = χ_vec/χ_stag with t² = R/4, so 2/7 ⟺ R = 8/7.

Execute three tasks, in this order (each is independently publishable as a finding; stop and document if any produces a decisive negative):

**Task 1 — diamagnetic-complete momentum-space PT → the physical R(m) at small q̃.**
The module's `polarization`/`dirac_*` PT path is paramagnetic-only; the brute force (`brute_force_chi`, `dirac_brute_force_chi`) is complete but capped at L=6–8. Add the diamagnetic (Peierls-contact) term: expand the gauged W₂ (and Dirac D₂) to O(ε²); the transfer-0 part contributes a first-order eigenphase shift δΩ_n = Re[i e^{iΩ_n}⟨n|δ²W₂|n⟩] summed over the filled set. Derive δ²W₂ blocks analytically from the midpoint Peierls (per-tick −a²/2 diagonal terms plus tick1×tick2 cross terms at transfer 0 from ±q̃ pairing; for the staggered channel the parity charges square to 1, so the contact term is charge-blind — check whether this alone explains the F149 N6/N7 sign disagreement). Validate: PT_para + PT_dia must reproduce `brute_force_chi` at L=6, 8 (m=0 and m=0.2, both channels, rel < 1e-6; remember χ_bf = χ_PT/2 for the cos wave). Then sweep: L = 32–48, m_qt = 1..4, m ∈ {0.05..0.5}, extract R(m) = χ_vec/χ_stag at q̃→0. Success criterion: the sign of R−1 settled, and whether R(m) crosses 8/7 at some m\*. If it does, record m\* and the corresponding sin²θ_W chain.

**Task 2 — the 8-vs-7 multiplicity test (cheap, do even if Task 1 stalls).**
F147/F149 left the suggestive identity 8/7 = (NN hops):(WS facet axes). Test whether the vector stiffness decomposes per hop direction or per facet axis: decompose the vector vertex V = iΣ_d (d·ê)e^{id·q}C_d into single-hop contributions V_d and compute the 8×8 (or 7×7 axis-paired) channel matrix χ_dd′ = contributions of hop-pair (d,d′) to the full χ (brute force or diamagnetic-complete PT). Questions: (i) is χ_dd′ diagonal-dominant in the hop basis or the axis basis (d paired with −d)? (ii) do the 6 NNN/face-axis channels of the WS cell appear (they must, if the facet decomposition is physical — the two-tick composite hops include face-axis displacements)? (iii) does the staggered channel see a different effective channel count (the −1 relative tick sign kills/keeps different pairs)? Target statement: "χ_vec sums N_W equal channels and χ_stag sums N_Y equal channels with N_W:N_Y·(charge²) = 7:2" or its refutation. This is the direct test of F141-U1/U3.

**Task 3 — match the proxy m to the F118 condensate.**
The F149 Dirac m is a stand-in. Read `findings/F118-self-consistent-Wvc-and-C-Eg-self-interaction.md` (the (W,v,c) closure, κ_E≈−2.2, c≈1.1, v≈0.16) and F46 (`ca_dirac_bcc` mass conventions). Determine the model-correct constituent coupling: which m corresponds to the EWSB condensate's coupling to the sea (not the bare lepton mass — likely the wall-pinned y_τ=1 scale or the E_g amplitude at saturation). If Task 1 produced R(m), evaluate R(m_phys) and compare 8/7; quantify the implied sin²θ_W^os against 2/9 (PDG −0.44%) and m_Z/m_W = 3/√7 (−0.063%).

**Practices and pitfalls (hard-won this week, do not rediscover):**
- F-number collisions are routine: `ls findings/ | sed 's/F\([0-9]*\)-.*/\1/' | sort -n | tail -1` immediately before writing any finding file; current max is F149 as of this prompt.
- ω = π/2 cut-surface ties: use the golden-ratio grid offset (already in the module) for pointwise comparisons; the cot kernel vanishes at the cut so summed χ is safe.
- Γ-on-grid zero modes destabilize brute-force filling at L ≡ 0 mod 4: keep the BC `twist` parameter on (uncharged — outside the parity charge).
- Strong fields cause exact 2π quantized sea-energy jumps (cut crossings) — second differences at small ε are safe; energy *differences* at large ε are not.
- numpy eig on the 4×4 Dirac blocks is guarded by the analytic-dispersion cross-check (`dirac_bands` returns the residual; keep asserting < 1e-12 per CLAUDE.md numpy/chiral caveat).
- Sea conventions are physics: one-tick = rigid (zero response, exact); two-tick/stroboscopic = the physical one (F51 §3). State the convention in every result.
- All checks tiered: exact (fractions/integer) > machine > numeric-decisive; JSON to `test-results/`, finding to `findings/F{N}-name.md`, changelog one-paragraph entry, exactness-inventory rows (last used: #103), then `python3 tools/regen_indexes.py`.

**Falsification discipline:** if Task 1 gives R(m) monotone *below* 1 (staggered always enhanced in the physical response), then with bare content t² = R/4 < 1/4 moves *away* from 2/7 — that kills route (b) for the bare content and the result is a no-go finding pointing all remaining weight at Task 2's multiplicity route (or at combined content×dynamics). Negative results get findings too.
