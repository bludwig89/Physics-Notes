# Session prompt — two-loop precision: the (α/π)² term of a_e, two-loop running, and muon a_μ (lepton universality)

*Copy everything below into a fresh session in this project. It assumes `CLAUDE.md` and the compact indexes load automatically.*

---

## Task

Push the QED sector to **two-loop precision** and test **lepton universality**. Three deliverables:

1. The **two-loop electron anomalous moment** coefficient $A_2$ in $a_e=\tfrac{\alpha}{2\pi}+A_2\!\left(\tfrac{\alpha}{\pi}\right)^2+\dots$, target $A_2=-0.328478965\ldots$ (Sommerfield–Petermann).
2. The **two-loop running** of $\alpha$ (the next coefficient beyond the one-loop $b_0=4/3$ of F251).
3. The **muon** anomalous moment $a_\mu$ from the same vertex machinery (universality: the mass-independent QED part must match $a_e$'s, plus the mass-dependent vacuum-polarization insertions that make $a_\mu\neq a_e$).

## Why this is tractable now (read first)

- **F252** (`ca-simulation/ca_vertex_loop.py`) — the one-loop vertex and $a_e=\alpha/2\pi$ (the $A_1$ term); the two-loop diagrams are insertions into this vertex. Reuse its Feynman-parameter/γ machinery.
- **F251** (`ca-simulation/ca_vacuum_polarization.py`) — the vacuum-polarization $\Pi$; the mass-dependent two-loop $a_\ell$ diagrams are $\Pi$-insertions on the internal photon (the electron-loop VP insertion is the dominant source of $a_\mu>a_e$).
- **Prompt 1 (electron self-energy, F258)** — its $\{\delta m, Z_2\}$ are renormalization inputs for the two-loop subdivergence subtraction; wait for it or reproduce the needed pieces.
- **F120/F121** — the lepton mass anchors ($m_e, m_\mu, m_\tau$) for the mass-dependent pieces.

## What to build

1. **Two-loop $a_e$ ($A_2$) — quantitative, high-precision.** The seven two-loop vertex diagrams (including the VP insertion with an internal electron loop, and the two-loop vertex/ladder graphs). Reproduce $A_2=-0.328478965\ldots$ Use the model's own one-loop $\Pi$ (F251) for the VP-insertion piece so it is model-derived, not imported. Quote $a_e$ through $O((\alpha/\pi)^2)$ vs measured.
2. **Two-loop $\beta$-function coefficient — algebraic gate.** The QED running at two loops adds the $\tfrac{\alpha}{4\pi^2}$-order term; extract it (sympy where possible) and compare to the known QED two-loop coefficient. State honestly which pieces are leptonic vs deferred.
3. **Muon $a_\mu$ — quantitative + universality gate.** (a) The mass-independent QED part equals the electron's $A_1,A_2$ (universality — an exact gate: same numbers). (b) The mass-dependent VP-insertion part (electron loop inside the muon vertex, $\propto\ln(m_\mu/m_e)$) is the leading source of $a_\mu-a_e$; compute it from F251's $\Pi$. Quote the QED contribution to $a_\mu$; state clearly that the hadronic and electroweak contributions are **out of scope** (hadronic → QCD sector F151/F152; EW → weak sector), so the full SM $a_\mu$ and any experiment comparison is not this session's claim.

## Method + hygiene

- Exactness ladder: universality (electron $A_1,A_2$ = muon mass-independent QED part) as an exact identity; $A_2$ and the two-loop $\beta$ quantitatively vs known values; $a_\mu$ QED part quantitative with explicit scope. Record in `docs/status/exactness-inventory.md`.
- Two-loop subdivergences need the one-loop counterterms $\{Z_1,Z_2,Z_3,\delta m\}$ (F251, F252, Prompt 1) — assemble the subtraction consistently; this is the first real test of the renormalization program (ties to Prompt 7).
- No `eig` on chiral matrices; build the two-loop BZ/Feynman integrals explicitly. Sandbox timeouts likely at production precision → provide a `tests/runners/run_*` script emitting JSON for Claude to read (per CLAUDE.md).
- **Muon g-2 caveat:** do NOT assert a resolution of the experimental $a_\mu$ anomaly — the SM prediction and its data comparison are an active, moving area (Theory Initiative white papers 2020 and 2025; hadronic VP tension). Reference the framework; claim only the QED piece.
- Deliverables: `ca-simulation/ca_twoloop_ae.py` (+ `ca_amu.py` if cleaner), tests, JSON, finding. `grep` the true max first (suggested F261). Regen indexes, changelog, exactness-inventory.

## Definition of done

$A_2=-0.328479\ldots$ reproduced (with the VP-insertion piece taken from the model's own F251 $\Pi$); the two-loop QED $\beta$ coefficient extracted; muon universality shown (electron and muon mass-independent QED coefficients identical) and the mass-dependent $a_\mu-a_e$ leading log computed — with hadronic/EW contributions explicitly deferred.

## External references

- C. M. Sommerfield, *Phys. Rev.* 107, 328 (1957); A. Petermann, *Helv. Phys. Acta* 30, 407 (1957) — the two-loop coefficient $A_2=-0.328478965\ldots$
- S. Laporta & E. Remiddi, *Phys. Lett. B* 379, 283 (1996) — analytic higher-order $a_e$ (context/technique).
- T. Aoyama, M. Hayakawa, T. Kinoshita & M. Nio, *Phys. Rev. D* 91, 033006 (2015) — QED $a_e$ through tenth order (coefficient definitions $A_1,A_2,\dots$).
- T. Aoyama *et al.* (Muon g-2 Theory Initiative), *Phys. Rept.* 887, 1 (2020), arXiv:2006.04822 — SM prediction of $a_\mu$ (framework; note the 2025 update white paper and the active hadronic-VP situation).
- M. E. Peskin & D. V. Schroeder, *An Introduction to QFT* (1995), §6.3 and §10 (vertex, two-loop structure, renormalization).
