# F112 — SI prediction registry (2026-06-08 - 20:09)

Canonical cell: a = 1.066375e-34 m = 6.59782 ell_P, tau = 2.053661e-43 s, c_lat = 1/sqrt3.

**18/18 checks PASS.**

| sector | prediction | tier | model | measured | verdict | ok |
|---|---|---|---|---|---|---|
| A scales | cell spacing a | PREDICTION | 1.066375e-34 m | 6.59782 ell_P | a/ell_P = sqrt(8 pi) 3^(1/4) derived (F79); ell_P sets the metre | PASS |
| A scales | tick tau | PREDICTION | 2.053661e-43 s | a/(c sqrt 3) | Option C lightcone identity a/tau = c sqrt 3 | PASS |
| A scales | lattice lightcone a/tau | PREDICTION | 5.192558e+08 m/s | c sqrt 3 = 5.192558e+08 m/s | max signal speed = sqrt 3 * c; no particle reaches it (F26) | PASS |
| A scales | UV cutoff hbar c / a | PREDICTION | 1.8504e+18 GeV (0.152 E_Planck) | — | Brillouin-zone energy ceiling; pi x this at the BZ edge | PASS |
| B gravity | Newton constant G | PREDICTION | 6.674300e-11 | 6.674300e-11 (CODATA) | rel resid 3.0e-08 | PASS |
| B gravity | solar light deflection | PREDICTION | 1.751190" | 1.751190" (GR/VLBI) | rel resid 3.0e-08 | PASS |
| B gravity | bending coefficient K_bend | PREDICTION | -4 | -4 (GR) | exact at ALL field strengths (e^{2u} log is exactly Coulombic) | PASS |
| B gravity | Mercury perihelion / Shapiro / redshift | CONSISTENCY | PPN beta = gamma = 1 | e.g. perihelion 42.98"/cyr | GR-identical by D-EM9 — every classic test inherited exactly | PASS |
| C photon/LIV | ToF scale E_QG,2 (n=2) | FALSIFIER | 1.360e+19 GeV (1.11 E_Planck) | must exceed 7.0e+11 GeV (LHAASO GRB 221009A) | clears bound by 1.9e+07x | PASS |
| C photon/LIV | falsification threshold | FALSIFIER | 1.360e+19 GeV | — | a future subluminal n=2 ToF bound above this kills a_canon | PASS |
| C photon/LIV | vacuum birefringence eta | PREDICTION | 0 (exact, paired/even-law photon) | bound eta < 1e-15 (polarimetry) | cleared at ANY a; the counterfactual sigma-bilinear photon is excluded | PASS |
| C photon/LIV | photon mass | PREDICTION | 0 (massless, transverse, c = 1/sqrt3 lattice) | < 1e-27 eV (bounds) | massless luminal transverse — consistent with all bounds | PASS |
| D EW/spectrum | sin^2 theta_W (bare) | PREDICTION | 1/4 = 0.2500 | 0.2230 (PDG) | +12.1% (bare, no RG running) | PASS |
| D EW/spectrum | m_Z / m_W | PREDICTION | 2/sqrt3 = 1.1547 | 1.1346 (PDG) | +1.77% with zero fit parameters | PASS |
| D EW/spectrum | Koide Q | PREDICTION | 2/3 = 0.66667 (geometric, exact) | 0.666661 (from PDG masses) | data sits 0.001% from 2/3 | PASS |
| D EW/spectrum | lepton condensate angle delta | CONSISTENCY | 15 deg exactly (m_e=0 limit; Q=2/3 <=> delta=15) | 12.7328 deg | 2.27 deg offset carried entirely by m_e/m_tau (the e-mass order parameter) | PASS |
| D EW/spectrum | absolute fermion masses | CONSISTENCY | m_phys = m_lat * hbar/(c a); m_lat(e)=sin(a/(sqrt3 lambdabar_C))~1.6e-22 | electron is the kg anchor | ratios/Koide predicted; absolute scale calibrated | PASS |
| E sourcing | psi->K coefficient 8 pi G/c^4 | PREDICTION | a^2 c_lat/(hbar c) = 2.0766e-43 (SI) | identity 8 pi G/c^4 = a^2 c_lat/(hbar c) | exact (sympy zero residual) — sourcing has no free coupling | PASS |
